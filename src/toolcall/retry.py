"""Retrying after a miss, and stopping when the history already answers (v8's data).

v7 retries after a miss only when the request says to ("if it's not there,
look in the folder"); otherwise it answers that the file does not exist, or
guesses another name, and after an empty search it gives up. rare.py teaches
stopping (search_dead_end, missing_then_asked) next to one retry kind with a
hint, so the reply wins. Here every retry kind but the last comes with a
twin of the same shape where the history already holds the answer, so the
cue is what the history contains, not the word "error":

  retry                                       stop (the twin)
  read_miss_list    read a missing file,      miss_listed_absent   the listing has no such
                    list its folder, read                          file: say it is not there
                    the one with that name
  list_into_subdir  the listing lacks the     subdir_exhausted     the subfolder lacks it
                    file but shows one                             too: say so
                    subfolder: list it
  search_reword     no match; the user gave   reword_exhausted     the other name matches
                    another name: search it                        nothing either: say so
  search_pointer    off-topic hits, one       offtopic_no_pointer  off-topic hits and no
                    names the topic the docs                       pointer: say nothing
                    file it under: search it                       covers it
  search_not_guess  a question the docs answer, no file named: crag_search, also after
                    a guessed fs_read has failed

The rule the kinds share: retry when the conversation holds a move not yet
tried (a folder to list, another name, a term from a result); stop when it
does not. Splits, families and pools as in rare.py, with aliases of their
own for the topics, disjoint between train and test. Own seed and own files.

    python -m toolcall.retry       # -> data/mt8_{train,val,test_id,test_ood}.jsonl
"""

from __future__ import annotations

import json

from .corpus import CORPUS, NO_SUCH_FILE, chunk_path, search_result
from .data import ROOT, frame, path_rule
from .episodes import (
    MISSING_ANSWER,
    MISSING_REPLIES,
    READ_REPLIES,
    Episode,
    Kind,
    call,
    contains,
    expect,
    found,
    generate,
    lines,
    one_of,
    reply,
    write,
)
from .rare import BELOW, DEAD_ANSWER, NO_MATCH, RSlots, _file_in, _list, _read, make

SEED = 20261128
SPLITS = ("mt8_train", "mt8_val", "mt8_test_id", "mt8_test_ood")
HISTORY_P = 0.4     # the miss happened in an earlier turn, and the user pushes back
SUFFIXES = ("_v2", "-final", "_2026", "-new", "_old")

# What a user might call a topic, and the words a search for that name must contain.
ALIAS: dict[str, tuple[str, list[str]]] = {
    # train topics
    "BM25 parameters": ("the keyword scoring knobs", ["keyword"]),
    "reciprocal rank fusion": ("how the two result lists get merged", ["merge"]),
    "the relevance gate": ("the score cutoff", ["cutoff"]),
    "embedding dimension": ("the vector size", ["vector size"]),
    "the stdio transport": ("the pipe protocol", ["pipe"]),
    "JSON-RPC error codes": ("the failure numbers", ["failure"]),
    "schema validation": ("argument checking", ["argument"]),
    "the worker thread pool": ("how many workers it spawns", ["workers"]),
    "fuzzing harnesses": ("the random-input tests", ["random"]),
    "SSE resumption": ("reconnecting a dropped stream", ["reconnect"]),
    "chunking strategy": ("how documents get split up", ["split"]),
    "cosine similarity": ("the vector match score", ["match score"]),
    "the HTTP origin check": ("the browser header check", ["browser"]),
    "protocol version negotiation": ("the handshake", ["handshake"]),
    "handler timeouts": ("slow tools getting killed", ["slow"]),
    "the replay gate": ("the recorded-response check", ["recorded"]),
    "WAL mode in SQLite": ("the journal setting", ["journal"]),
    "the Python binding": ("the py wrapper", ["wrapper"]),
    # test topics
    "the SSRF egress guard": ("the outbound address filter", ["outbound"]),
    "log redaction": ("token masking in logs", ["mask"]),
    "cancellation of requests": ("stopping a running call", ["stopping"]),
    "the HNSW index": ("the approximate neighbour search", ["approximate"]),
    "nDCG evaluation": ("the ranking score on SciFact", ["scifact"]),
    "rate limiting at accept": ("the connection throttle", ["throttle"]),
    "subscriptions": ("being told when a resource changes", ["resource"]),
    "structured tool output": ("machine-readable results", ["machine-readable"]),
    "the soak test": ("the long endurance run", ["endurance"]),
}
# Topics the docs do not cover (rare.py's EXTRA["absent"]), with an alias each.
ABSENT_ALIAS: dict[str, tuple[str, list[str]]] = {
    "quantum annealing": ("qubit optimisation", ["qubit"]),
    "the billing API": ("the invoicing endpoints", ["invoic"]),
    "Kubernetes autoscaling": ("scaling pods up and down", ["pods"]),
    "GraphQL federation": ("stitching the schemas together", ["stitch"]),
    "the mobile app": ("the phone client", ["phone"]),
    "OAuth refresh tokens": ("renewing login tokens", ["renew"]),
    "the payroll export": ("the salary spreadsheet", ["salary"]),
    "Bluetooth pairing": ("connecting a headset", ["headset"]),
    "the CDN cache": ("the edge cache", ["edge"]),
    "dark mode": ("the night theme", ["night"]),
}
NOT_FOUND = one_of(*MISSING_ANSWER["any"], "there's no", "couldn't find", "could not find",
                   "no such")


def _search(words: list[str]) -> dict:
    return expect("crag_search", ("k",), query={"contains_all": words},
                  k={"any_of": [1, 2, 3, 4, 5]})


def _topics(s: RSlots) -> list[str]:
    return [t for t, _ in s.p["topics"]]


def _hits(s: RSlots, topics: list[str], cos: tuple[float, float], note: str = "") -> str:
    """crag_search's answer with chunks of `topics`, the first with `note` appended."""
    items = []
    for rank, t in enumerate(topics):
        c = s.rng.uniform(*cos) - 0.03 * rank
        bm25, fusion = s.rng.uniform(1.0, 4.0) / (rank + 1), 2 / (61 + rank)
        body = CORPUS[t][0] + (f" {note}" if rank == 0 and note else "")
        items.append(f"[cos {c:.3f}  bm25 {bm25:.2f}  fusion {fusion:.3f}] "
                     f"{chunk_path(t)}\n{body}")
    return "\n\n".join(items)


def _others(s: RSlots, but: str, n: int = 2) -> list[str]:
    return s.rng.sample([t for t in _topics(s) if t != but], n)


def _absent(s: RSlots) -> tuple[str, str, list[str], list[str]]:
    topic, words = s.rng.choice(s.x["absent"])
    alias, alias_words = ABSENT_ALIAS[topic]
    return topic, alias, words, alias_words


def _name(path: str) -> str:
    return path.rsplit("/", 1)[1]


# ---- a missing file: list its folder ----

PLAIN_READ = ("Read {f}.", "What's in {f}?", "Show me {f}.", "Open {f} for me.", "Print {f}.",
              "I need the contents of {f}.", "Could you pull up {f}?", "Display {f}, please.")
LOOK = ("Look in the folder, it's in there somewhere.", "Check what's in {d} then.",
        "It's definitely in {d}. Find it.", "Have a look around {d}.",
        "Maybe it's named differently. Check {d}.", "It must be there under another name.",
        "Poke around {d} for it.", "Go and see what {d} actually has.")
FOUND_AS = ("There's no {w}, but {d} has {f}:\n\n{c}",
            "{w} doesn't exist; the file is {f}:\n\n{c}",
            "I listed {d} and found {f}. It says:\n\n{c}", "The file is called {f}:\n\n{c}")
ABSENT_FILE = ("There's no {w}, and {d} has no file like it: only {n}.",
               "{d} doesn't have it: there is no {w}, just {n}.",
               "No such file. {d} only contains {n}.",
               "I couldn't find it: {d} holds {n}, nothing named {t}.")
AGAIN = ("Try {f} again.", "Can you open {f}?", "So what's in {f}?", "Read {f} one more time.",
         "Just show me {f}.", "Have another go at {f}.", "Once more: {f}.", "Get me {f} please.")


def _variant(s: RSlots, d: str, target: str) -> tuple[str, str]:
    """The path the user names, and the one that exists (same name with
    another extension, sometimes a suffix too)."""
    real_ext, wrong_ext = s.rng.sample(s.p["exts"], 2)
    wrong = _file_in(s, d, target, wrong_ext)
    name = target + (s.rng.choice(SUFFIXES) if s.rng.random() < 0.5 else "")
    return wrong, _file_in(s, d, name, real_ext)


def _missed(ep: Episode, s: RSlots, fam: int, wrong: str, d: str) -> None:
    """The read that misses: this turn's scored call, or an earlier turn the
    user pushes back on."""
    if s.rng.random() < HISTORY_P:
        ep.user(s.rng.choice(PLAIN_READ).format(f=wrong))
        ep.call(call("fs_read", path=wrong), NO_SUCH_FILE)
        ep.say(reply(MISSING_REPLIES, wrong, f=wrong), scored=False)
        ep.user(LOOK[fam].format(d=d))
    else:
        ep.user(frame(s.rng, s.p, PLAIN_READ[fam].format(f=wrong)))
        ep.call(call("fs_read", path=wrong), NO_SUCH_FILE,
                expect("fs_read", path=path_rule(wrong)))


def read_miss_list(ep: Episode, s: RSlots, fam: int) -> None:
    d = s.dir()
    target, *others = s.rng.sample(s.p["names"], s.rng.randint(2, 4))
    wrong, right = _variant(s, d, target)
    ep.tree.add(right, lines(s))
    for n in others:
        ep.tree.add(_file_in(s, d, n), lines(s))
    _missed(ep, s, fam, wrong, d)
    _list(ep, d)
    text = _read(ep, right)
    ep.say(reply(FOUND_AS, right, w=wrong, d=d, f=right, c=text.rstrip("\n")),
           contains(_name(right), *text.splitlines()))


def miss_listed_absent(ep: Episode, s: RSlots, fam: int) -> None:
    d = s.dir()
    target, *others = s.rng.sample(s.p["names"], s.rng.randint(2, 4))
    wrong, _ = _variant(s, d, target)
    for n in others:
        ep.tree.add(_file_in(s, d, n), lines(s))
    names = ", ".join(sorted(_name(p) for p in ep.tree.files))
    said = reply(ABSENT_FILE, wrong, w=wrong, d=d, n=names, t=target)
    if s.rng.random() < HISTORY_P:
        # Missed and listed in an earlier turn; asked again, the history answers.
        ep.user(s.rng.choice(PLAIN_READ).format(f=wrong))
        ep.call(call("fs_read", path=wrong), NO_SUCH_FILE)
        ep.call(call("fs_list", path=d), ep.tree.listing(d))
        ep.say(said, scored=False)
        ep.user(AGAIN[fam].format(f=wrong))
        ep.say(reply(MISSING_REPLIES, wrong + str(fam), f=wrong), MISSING_ANSWER)
        return
    _missed(ep, s, fam, wrong, d)
    _list(ep, d)
    ep.say(said, NOT_FOUND)


# ---- a listing without the file: its one subfolder ----

FIND = ("Read the {n} file in {d}.", "Open {d}'s {n} file.", "Show me the {n} file from {d}.",
        "What does the {n} file in {d} say?", "Get me {n} out of {d}.",
        "I need the {n} document in {d}.", "Fetch the {n} file that's in {d}.",
        "Can you find {n} in {d} and show it?")
NOT_IN_EITHER = ("I couldn't find a {n} file in {d} or in {d}/{u}.",
                 "There's no {n} file: {d} and {d}/{u} don't have one.",
                 "{d} has no {n} file, and neither does {d}/{u}.",
                 "No {n} file in {d}, not even in {d}/{u}.")
NOT_IN_EITHER_ANSWER = one_of("couldn't find", "there's no", "has no", "not even")


def _subdir_tree(ep: Episode, s: RSlots, has_it: bool) -> tuple[str, str, str, str]:
    """A folder with some files and one subfolder; the target is in the
    subfolder when `has_it`."""
    d, sub = s.dir(), s.rng.choice(s.x["subdirs"])
    target, *others = s.rng.sample(s.p["names"], s.rng.randint(3, 5))
    k = s.rng.randint(1, len(others) - 1)
    for n in others[:k]:
        ep.tree.add(_file_in(s, d, n), lines(s))
    for n in others[k:]:
        ep.tree.add(_file_in(s, f"{d}/{sub}", n), lines(s))
    path = _file_in(s, f"{d}/{sub}", target)
    if has_it:
        ep.tree.add(path, lines(s))
    return d, sub, target, path


def _ask_subdir(ep: Episode, s: RSlots, fam: int, d: str, target: str) -> None:
    if s.rng.random() < HISTORY_P:
        wrong = _file_in(s, d, target)
        ep.user(frame(s.rng, s.p, PLAIN_READ[fam].format(f=wrong)))
        ep.call(call("fs_read", path=wrong), NO_SUCH_FILE,
                expect("fs_read", path=path_rule(wrong)))
    else:
        ep.user(frame(s.rng, s.p, FIND[fam].format(n=target, d=d)))
    _list(ep, d)


def list_into_subdir(ep: Episode, s: RSlots, fam: int) -> None:
    d, sub, target, path = _subdir_tree(ep, s, has_it=True)
    _ask_subdir(ep, s, fam, d, target)
    _list(ep, f"{d}/{sub}")
    text = _read(ep, path)
    ep.say(reply(READ_REPLIES, path, f=path, c=text.rstrip("\n")),
           contains(_name(path), *text.splitlines()))


def subdir_exhausted(ep: Episode, s: RSlots, fam: int) -> None:
    d, sub, target, _ = _subdir_tree(ep, s, has_it=False)
    _ask_subdir(ep, s, fam, d, target)
    _list(ep, f"{d}/{sub}")
    ep.say(reply(NOT_IN_EITHER, d + target, n=target, d=d, u=sub), NOT_IN_EITHER_ANSWER)


# ---- an empty search: the other name the user gave ----

TWO_NAMES = ("What do the docs say about {a}? They might call it {t}.",
             "Look up {a} in the docs, or {t}, whatever it's called there.",
             "Find the passage on {a} ({t}, officially).",
             "I want what the docs have on {a}. The proper term is {t}, I think.",
             "Search the docs for {a}; the official name is {t}.",
             "Anything in the index about {a}? Also known as {t}.",
             "Dig up {a} in the docs. The documentation may say {t}.",
             "Check the knowledge base on {a}, a.k.a. {t}.")
ONE_NAME = ("What do the docs say about {a}?", "Look up {a} in the docs.",
            "Find the passage on {a}.", "Anything in the index about {a}?",
            "Search the docs for {a}.", "What does the documentation have on {a}?",
            "Pull up whatever the docs say about {a}.", "Is {a} covered in the docs?")
OTHER_NAME = ("Try {t} instead.", "Maybe the docs call it {t}.", "It might be filed as {t}.",
              "Search for {t} then.", "The official name is {t}, try that.", "Try under {t}.",
              "Could be listed as {t}.", "Have a go with {t}.")
NOTHING_FOR = ("I found nothing on {a}.", "Nothing matched {a} in the docs.",
               "No results for {a}.", "The docs have nothing on {a}.")
NOTHING_EITHER = ("I searched for both {a} and {t}, and nothing matched.",
                  "I couldn't find anything under {a} or {t}.",
                  "No results under {a} or under {t}: the docs don't cover it.",
                  "I couldn't find anything on {t} either, so the docs don't seem to have it.")
STILL_NOTHING = ("So nothing at all on {a}?", "Nothing in the docs then?",
                 "Really nothing about {a}?", "So the docs don't cover {a}?",
                 "Nothing under either name?", "No luck at all?",
                 "So {a} isn't documented?", "The index has nothing on it, then?")


def _first_try(ep: Episode, s: RSlots, fam: int, alias: str, aw: list[str], topic: str) -> None:
    """The search under the user's own name for it, which matches nothing."""
    empty = s.rng.choice((NO_MATCH, BELOW))
    if s.rng.random() < HISTORY_P:
        ep.user(frame(s.rng, s.p, s.rng.choice(ONE_NAME).format(a=alias)))
        ep.call(call("crag_search", query=alias), empty)
        ep.say(reply(NOTHING_FOR, alias, a=alias), scored=False)
        ep.user(OTHER_NAME[fam].format(t=topic))
    else:
        ep.user(frame(s.rng, s.p, TWO_NAMES[fam].format(a=alias, t=topic)))
        ep.call(call("crag_search", query=alias), empty, _search(aw))


def search_reword(ep: Episode, s: RSlots, fam: int) -> None:
    topic, words = s.topic()
    alias, aw = ALIAS[topic]
    _first_try(ep, s, fam, alias, aw, topic)
    ep.call(call("crag_search", query=topic), search_result(s.rng, topic, _topics(s)),
            _search(words))
    text, fact = found(topic, alias)
    ep.say(text, fact)


def reword_exhausted(ep: Episode, s: RSlots, fam: int) -> None:
    topic, alias, words, aw = _absent(s)
    if s.rng.random() < HISTORY_P:
        ep.user(frame(s.rng, s.p, TWO_NAMES[fam].format(a=alias, t=topic)))
        ep.call(call("crag_search", query=alias), NO_MATCH)
        ep.call(call("crag_search", query=topic), s.rng.choice((NO_MATCH, BELOW)))
        ep.say(reply(NOTHING_EITHER, alias, a=alias, t=topic), scored=False)
        ep.user(STILL_NOTHING[fam].format(a=alias))
        ep.say(reply(NOTHING_EITHER, topic + str(fam), a=alias, t=topic), DEAD_ANSWER)
        return
    _first_try(ep, s, fam, alias, aw, topic)
    ep.call(call("crag_search", query=topic), s.rng.choice((NO_MATCH, BELOW)), _search(words))
    ep.say(reply(NOTHING_EITHER, alias, a=alias, t=topic), DEAD_ANSWER)


# ---- off-topic hits: the term one of them points to ----

POINTER = ("({A} is covered under {t}.)", "See {t} for {a}.", "For {a}, see the notes on {t}.",
           "{A} is described in the section on {t}.")
OFFTOPIC = ("Nothing on {a}: the closest hits are about {o} and {p}.",
            "The search found nothing about {a}, only passages on {o} and {p}.",
            "I couldn't find {a} in the docs; what came back is about {o} and {p}.",
            "No match for {a}. The results were on {o} and {p}, which is something else.")


def search_pointer(ep: Episode, s: RSlots, fam: int) -> None:
    topic, words = s.topic()
    alias, aw = ALIAS[topic]
    note = s.rng.choice(POINTER).format(A=alias[0].upper() + alias[1:], a=alias, t=topic)
    ep.user(frame(s.rng, s.p, ONE_NAME[fam].format(a=alias)))
    ep.call(call("crag_search", query=alias), _hits(s, _others(s, topic), (0.40, 0.50), note),
            _search(aw))
    ep.call(call("crag_search", query=topic), search_result(s.rng, topic, _topics(s)),
            _search(words))
    text, fact = found(topic, alias)
    ep.say(text, fact)


def offtopic_no_pointer(ep: Episode, s: RSlots, fam: int) -> None:
    _, alias, _, aw = _absent(s)
    o, p = _others(s, "")
    ep.user(frame(s.rng, s.p, ONE_NAME[fam].format(a=alias)))
    ep.call(call("crag_search", query=alias), _hits(s, [o, p], (0.38, 0.47)), _search(aw))
    ep.say(reply(OFFTOPIC, alias, a=alias, o=o, p=p),
           one_of(*DEAD_ANSWER["any"], "no match"))


# ---- a question the docs answer, and no file named ----

QUESTION = ("How does {t} work here?", "What's the story with {t}?",
            "Remind me how {t} is set up.", "What do we do about {t}?",
            "Tell me about {t} in this project.", "How is {t} handled?",
            "Explain {t} as this codebase does it.", "What's our approach to {t}?")
GUESS_EXTS = (".txt", ".rst", "-notes.md")


def search_not_guess(ep: Episode, s: RSlots, fam: int) -> None:
    topic, words = s.topic()
    ep.user(frame(s.rng, s.p, QUESTION[fam].format(t=topic)))
    if s.rng.random() < 0.5:
        # An earlier guess at a file name failed: the docs are still the place to look.
        guess = chunk_path(topic).replace(".md", s.rng.choice(GUESS_EXTS))
        ep.call(call("fs_read", path=guess), NO_SUCH_FILE)
    ep.call(call("crag_search", query=topic), search_result(s.rng, topic, _topics(s)),
            _search(words))
    text, fact = found(topic, topic)
    ep.say(text, fact)


KINDS: dict[str, Kind] = {
    "read_miss_list": read_miss_list, "miss_listed_absent": miss_listed_absent,
    "list_into_subdir": list_into_subdir, "subdir_exhausted": subdir_exhausted,
    "search_reword": search_reword, "reword_exhausted": reword_exhausted,
    "search_pointer": search_pointer, "offtopic_no_pointer": offtopic_no_pointer,
    "search_not_guess": search_not_guess,
}
RETRY = ("read_miss_list", "list_into_subdir", "search_reword", "search_pointer",
         "search_not_guess")


def build(seed: int = SEED) -> list[dict]:
    return generate(KINDS, SPLITS, seed, make)


def main() -> int:
    print(json.dumps(write(build(), ROOT / "data", SPLITS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
