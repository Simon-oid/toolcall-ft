"""Multi-step and multi-turn episodes: requests that need more than one call,
or that refer back to an earlier turn.

An episode is a conversation with the tools' answers written in (corpus.py
renders them as the servers do). Every model turn of it that we score is a
*step case*: the conversation up to that turn, and what the model should do
next - a call (scored on the four levels, like a single-turn case) or a
reply with no call (scored on abstaining, and on repeating the fact the
tool returned, when there is one). The history is always the right one
(teacher forcing), so a step measures one decision; an episode is right
when every step of it is.

Multi-step, one user turn:
  find_then_read     "open the plan in notes": list the folder, read the match
  check_then_read    "if f exists, read it": stat, then read or say it is missing
  search_then_save   search the docs, write the top chunk to a file
  list_then_write    list a folder, write the names to a file
  stats_then_search  check the index has chunks, then search or say it is empty

Multi-turn, the first turn done and in the history, the second one scored:
  followup_read      list a folder; "open the second one"
  followup_stat      read a file; "how big is it?"
  followup_save      search the docs; "save that to f"
  followup_ask       any first turn; "save that" with no file: ask which
  followup_thanks    any first turn; "thanks": answer, no call

The second turns of followup_read/stat/save are the requests data.py
labels ambiguous when they come alone ("How big is that one?"): with the
history they are not, and the model has to tell the two apart.

Splits as in data.py: families 0-5 and the TRAIN pools for mt_train and
mt_val, families 0-5 and TEST pools for mt_test_id, the held-out families
6-7 and TEST pools for mt_test_ood. Own seed and own files: the
single-turn data does not change.

    python -m toolcall.episodes        # -> data/mt_{train,val,test_id,test_ood}.jsonl
"""

from __future__ import annotations

import json
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from .corpus import CORPUS, Tree, chunk_path, search_result, stats_result
from .data import (
    ASK_FRAMES,
    FILE_ASKS,
    OOD_FAMILIES,
    POOLS,
    ROOT,
    TRAIN_FAMILIES,
    Slots,
    _pick,
    dir_rule,
    frame,
    path_rule,
)

SEED = 20261121
SPLITS = ("mt_train", "mt_val", "mt_test_id", "mt_test_ood")
EPISODES_TRAIN = 70        # per kind, train + val
EPISODES_TEST_ID = 12      # per kind
EPISODES_TEST_OOD = 20     # per kind
VAL_FRACTION = 0.1
MISSING_P = 0.35           # check_then_read: the file is not there
EMPTY_P = 0.3              # stats_then_search: the index is empty


@dataclass
class Episode:
    tree: Tree
    context: list[dict] = field(default_factory=list)
    steps: list[dict] = field(default_factory=list)

    def user(self, text: str) -> None:
        self.context.append({"role": "user", "content": text})

    def call(self, call: dict, result: str, expected: dict | None = None) -> None:
        """A call and its result. With `expected`, the call is a scored step."""
        if expected is not None:
            self.steps.append({"context": [*self.context], "expected": expected,
                               "call": call, "reply": None, "answer": None})
        self.context += [{"role": "assistant", "content": "",
                          "tool_calls": [{"type": "function", "function": call}]},
                         {"role": "tool", "name": call["name"], "content": result}]

    def say(self, reply: str, answer: dict | None = None, scored: bool = True) -> None:
        """A reply with no call: a scored step unless it is history."""
        if scored:
            self.steps.append({"context": [*self.context], "expected": None,
                               "call": None, "reply": reply, "answer": answer})
        self.context.append({"role": "assistant", "content": reply})


def call(name: str, **arguments: object) -> dict:
    return {"name": name, "arguments": arguments}


def expect(name: str, optional: tuple[str, ...] = (), **arguments: object) -> dict:
    return {"name": name, "arguments": arguments, "optional": list(optional)}


def contains(*facts: str) -> dict:
    return {"all": list(facts)}


def one_of(*phrases: str) -> dict:
    return {"any": list(phrases)}


def lines(s: Slots) -> str:
    """A small file: one or two lines from the pool, newline-terminated."""
    return "".join(x + "\n" for x in s.rng.sample(s.p["contents"], s.rng.randint(1, 2)))


def answer_lines(content: str) -> dict:
    return contains(*content.splitlines())


# ---- replies: several wordings, picked by a hash (as data.REFUSALS) ----

READ_REPLIES = ("Here is {f}:\n\n{c}", "{f} says:\n\n{c}", "The contents of {f}:\n\n{c}",
                "This is what {f} contains:\n\n{c}")
MISSING_REPLIES = ("{f} doesn't exist.", "There is no file at {f}: it does not exist.",
                   "I checked, and {f} does not exist.", "{f} isn't there: no such file.")
MISSING_ANSWER = one_of("doesn't exist", "does not exist", "no such file", "not found",
                        "isn't there", "is not there", "there is no")
SAVED_REPLIES = ("Done: I saved it to {f}.", "Saved to {f}.", "I wrote it to {f}.",
                 "It's in {f} now.")
FOUND_REPLIES = ("The docs say: {b}", "According to {p}: {b}", "From the index ({p}): {b}",
                 "Here's what I found in {p}: {b}")
EMPTY_REPLIES = ("The index is empty (0 chunks), so there is nothing to search.",
                 "There are no chunks in the index yet: it's empty.",
                 "Nothing is indexed: the index has 0 chunks.",
                 "The index is empty, so I didn't search.")
EMPTY_ANSWER = one_of("empty", "0 chunks", "no chunks", "nothing is indexed")
LISTED_REPLIES = ("{d} contains {n}.", "In {d}: {n}.", "{d} has these files: {n}.",
                  "I found these files in {d}: {n}.")
SIZE_REPLIES = ("{f} is {v} bytes.", "It's {v} bytes.", "The file is {v} bytes long.",
                "{f} takes {v} bytes.")
DATE_REPLIES = ("{f} was last modified on {v}.", "It was last changed on {v}.",
                "The last modification was on {v}.", "Last modified: {v}.")
MODE_REPLIES = ("Its mode is {v}.", "The permissions are {v}.", "{f} has mode {v}.",
                "The mode bits are {v}.")
THANKS_REPLIES = ("You're welcome!", "Glad I could help.", "Anytime!", "Happy to help.")


def reply(options: tuple[str, ...], key: str, **slots: object) -> str:
    return _pick(options, key).format(**slots)


def found(topic: str, key: str) -> tuple[str, dict]:
    """A grounded answer from the top chunk, and the fact it must carry."""
    body, fact = CORPUS[topic]
    return reply(FOUND_REPLIES, key, b=body, p=chunk_path(topic)), contains(fact)


def search(ep: Episode, s: Slots, topic: str, words: list[str], scored: bool) -> None:
    expected = expect("crag_search", ("k",), query={"contains_all": words},
                      k={"any_of": [1, 2, 3, 4, 5]})     # "the best passage": any small k
    result = search_result(s.rng, topic, [t for t, _ in s.p["topics"]])
    ep.call(call("crag_search", query=topic), result, expected if scored else None)


# ---- multi-step kinds: one user turn, every model turn scored ----

FIND_READ = ("Open the {n} file in {d}.", "Show me the {n} document that lives in {d}.",
             "There's a {n} file somewhere in {d}; read it to me.",
             "I don't remember the extension, but read the {n} file in {d}.",
             "Find the file called {n} in {d} and show me what it says.",
             "Read whatever {n} file is inside {d}.",
             "Can you track down the {n} file under {d} and print it?",
             "Somewhere in {d} there is a file named {n}. What does it say?")


def find_then_read(ep: Episode, s: Slots, fam: int) -> None:
    d = s.dir()
    names = s.rng.sample(s.p["names"], s.rng.randint(3, 4))
    files = [f"{n}.{s.rng.choice(s.p['exts'])}" for n in names]
    for f in files:
        ep.tree.add(f"{d}/{f}", lines(s))
    ep.user(frame(s.rng, s.p, FIND_READ[fam].format(n=names[0], d=d)))
    ep.call(call("fs_list", path=d), ep.tree.listing(d), expect("fs_list", path=dir_rule(d)))
    path = f"{d}/{files[0]}"
    text = ep.tree.read(path)
    ep.call(call("fs_read", path=path), text, expect("fs_read", path=path_rule(path)))
    ep.say(reply(READ_REPLIES, path, f=path, c=text.rstrip("\n")), answer_lines(text))


CHECK_READ = ("If {f} exists, show me what it says.",
              "Check whether {f} is there, and read it if it is.",
              "Does {f} exist? If so, print it.", "Make sure {f} exists first, then open it.",
              "See if there's a file at {f}; if there is, show it.",
              "Verify that {f} exists and then read it to me.",
              "Only if {f} is present, display its contents.",
              "Is there a {f}? Read it out if so.")


def check_then_read(ep: Episode, s: Slots, fam: int) -> None:
    f = s.file()
    present = s.rng.random() >= MISSING_P
    if present:
        ep.tree.add(f, lines(s))
    ep.user(frame(s.rng, s.p, CHECK_READ[fam].format(f=f)))
    ep.call(call("fs_stat", path=f), ep.tree.stat(f), expect("fs_stat", path=path_rule(f)))
    if not present:
        ep.say(reply(MISSING_REPLIES, f, f=f), MISSING_ANSWER)
        return
    text = ep.tree.read(f)
    ep.call(call("fs_read", path=f), text, expect("fs_read", path=path_rule(f)))
    ep.say(reply(READ_REPLIES, f, f=f, c=text.rstrip("\n")), answer_lines(text))


SEARCH_SAVE = ("Search the docs for {t} and save the best passage to {f}.",
               "Look up {t} in the documentation and write the top result into {f}.",
               "Find the passage about {t} and store it in {f}.",
               "Get me the most relevant chunk on {t} from the index, then save it as {f}.",
               "Check the knowledge base for {t} and put the best hit in {f}.",
               "Pull the top passage on {t} out of the docs and write it to {f}.",
               "Grab whatever the corpus ranks first for {t} and file it under {f}.",
               "Query the index on {t}; the top chunk should end up in {f}.")


def search_then_save(ep: Episode, s: Slots, fam: int) -> None:
    (topic, words), f = s.topic(), s.file()
    ep.user(frame(s.rng, s.p, SEARCH_SAVE[fam].format(t=topic, f=f)))
    search(ep, s, topic, words, scored=True)
    body, fact = CORPUS[topic]
    ep.call(call("fs_write", path=f, content=body), Tree.write(f, body),
            expect("fs_write", path=path_rule(f), content={"contains_all": [fact]}))
    ep.say(reply(SAVED_REPLIES, f, f=f), contains(f))


LIST_WRITE = ("Write the list of files in {d} into {f}.", "Save a listing of {d} as {f}.",
              "Put the names of the files in {d} into {f}.",
              "Make {f} contain the file names from {d}.",
              "Record which files are in {d} in the file {f}.",
              "Create {f} listing every file in {d}.",
              "Catalogue the files under {d} and store the catalogue in {f}.",
              "I want {f} to hold an inventory of {d}.")


def list_then_write(ep: Episode, s: Slots, fam: int) -> None:
    d = s.dir()
    for n in s.rng.sample(s.p["names"], s.rng.randint(2, 4)):
        ep.tree.add(f"{d}/{n}.{s.rng.choice(s.p['exts'])}", lines(s))
    f = s.file()
    while f.startswith(d + "/"):
        f = s.file()
    ep.user(frame(s.rng, s.p, LIST_WRITE[fam].format(d=d, f=f)))
    ep.call(call("fs_list", path=d), ep.tree.listing(d), expect("fs_list", path=dir_rule(d)))
    names = ep.tree.entries(d)
    content = "".join(n + "\n" for n in names)
    ep.call(call("fs_write", path=f, content=content), Tree.write(f, content),
            expect("fs_write", path=path_rule(f), content={"contains_all": names}))
    ep.say(reply(SAVED_REPLIES, f, f=f), contains(f))


STATS_SEARCH = ("If the index isn't empty, search it for {t}.",
                "Check the index has something in it, then look up {t}.",
                "First make sure documents are indexed, then find {t}.",
                "Is anything indexed? If yes, search for {t}.",
                "Confirm the index has chunks and then search for {t}.",
                "See whether the index is populated; if so, look for {t}.",
                "Provided the corpus isn't empty, retrieve passages on {t}.",
                "Before searching for {t}, verify there are chunks in the index.")


def stats_then_search(ep: Episode, s: Slots, fam: int) -> None:
    topic, words = s.topic()
    request = frame(s.rng, s.p, STATS_SEARCH[fam].format(t=topic))
    ep.user(request)
    empty = s.rng.random() < EMPTY_P
    chunks, files = (0, 0) if empty else (s.rng.randint(40, 4000), s.rng.randint(3, 120))
    ep.call(call("crag_stats"), stats_result(chunks, files), expect("crag_stats"))
    if empty:
        ep.say(reply(EMPTY_REPLIES, request), EMPTY_ANSWER)
        return
    search(ep, s, topic, words, scored=True)
    ep.say(*found(topic, request))


# ---- multi-turn kinds: a finished first turn, the second one scored ----

T1_LIST = ("List the files in {d}.", "What's inside {d}?", "Show me the contents of {d}.")
T1_READ = ("Read {f}.", "What's in {f}?", "Show me {f}.")
T1_SEARCH = ("Search the docs for {t}.", "What does the index say about {t}?",
             "Look up {t} in the documentation.")


def t1_list(ep: Episode, s: Slots) -> tuple[str, list[str]]:
    d = s.dir()
    for n in s.rng.sample(s.p["names"], s.rng.randint(3, 4)):
        ep.tree.add(f"{d}/{n}.{s.rng.choice(s.p['exts'])}", lines(s))
    ep.user(s.rng.choice(T1_LIST).format(d=d))
    ep.call(call("fs_list", path=d), ep.tree.listing(d))
    names = ep.tree.entries(d)
    ep.say(reply(LISTED_REPLIES, d, d=d, n=", ".join(names)), scored=False)
    return d, names


def t1_read(ep: Episode, s: Slots) -> str:
    f = s.file()
    ep.tree.add(f, lines(s))
    ep.user(s.rng.choice(T1_READ).format(f=f))
    text = ep.tree.read(f)
    ep.call(call("fs_read", path=f), text)
    ep.say(reply(READ_REPLIES, f, f=f, c=text.rstrip("\n")), scored=False)
    return f


def t1_search(ep: Episode, s: Slots) -> str:
    topic, words = s.topic()
    ep.user(s.rng.choice(T1_SEARCH).format(t=topic))
    search(ep, s, topic, words, scored=False)
    ep.say(found(topic, topic)[0], scored=False)
    return topic


ORDINALS = ("first", "second", "third")
FOLLOW_READ = ("Open {n}.", "Read the {o} one.", "Show me {n}, please.",
               "What's in the {o} file?", "Now print {n}.", "Let's see the {o} one.",
               "Go ahead and open the {o} entry.", "And {n}, what does that say?")


def followup_read(ep: Episode, s: Slots, fam: int) -> None:
    d, names = t1_list(ep, s)
    i = s.rng.randrange(len(ORDINALS))
    ep.user(FOLLOW_READ[fam].format(n=names[i], o=ORDINALS[i]))
    path = f"{d}/{names[i]}"
    text = ep.tree.read(path)
    ep.call(call("fs_read", path=path), text, expect("fs_read", path=path_rule(path)))
    ep.say(reply(READ_REPLIES, path, f=path, c=text.rstrip("\n")), answer_lines(text))


FOLLOW_STAT = (("How big is it?", "size"), ("When was it last modified?", "date"),
               ("What are its permissions?", "mode"), ("Is that file large?", "size"),
               ("Get me its metadata.", "size"), ("And its size?", "size"),
               ("When did that one last change?", "date"), ("Tell me its mode bits.", "mode"))
STAT_REPLIES = {"size": SIZE_REPLIES, "date": DATE_REPLIES, "mode": MODE_REPLIES}


def followup_stat(ep: Episode, s: Slots, fam: int) -> None:
    f = t1_read(ep, s)
    request, what = FOLLOW_STAT[fam]
    ep.user(request)
    ep.call(call("fs_stat", path=f), ep.tree.stat(f), expect("fs_stat", path=path_rule(f)))
    value = {"size": str(ep.tree.size(f)), "date": ep.tree.files[f]["modified"][:10],
             "mode": "0644"}[what]
    ep.say(reply(STAT_REPLIES[what], f + what, f=f, v=value), contains(value))


FOLLOW_SAVE = ("Save that to {f}.", "Write the top passage into {f}.", "Put that answer in {f}.",
               "Store it as {f}.", "Note it down in {f}.", "Can you write that into {f}?",
               "File that away in {f}.", "Dump the best hit into {f}.")


def followup_save(ep: Episode, s: Slots, fam: int) -> None:
    topic = t1_search(ep, s)
    f = s.file()
    ep.user(FOLLOW_SAVE[fam].format(f=f))
    body, fact = CORPUS[topic]
    ep.call(call("fs_write", path=f, content=body), Tree.write(f, body),
            expect("fs_write", path=path_rule(f), content={"contains_all": [fact]}))
    ep.say(reply(SAVED_REPLIES, f, f=f), contains(f))


FOLLOW_ASK = ("Save that.", "Write it to a file.", "Put that in a file for me.",
              "Store the result.", "Keep that somewhere.", "Write the passage down.",
              "Persist that answer.", "Stash it in a file.")
FOLLOW_THANKS = ("Thanks!", "Great, that's all.", "Perfect, thank you.", "Cool, thanks a lot.",
                 "That's what I needed.", "Thanks, we're done.",
                 "Much obliged, that's everything.", "Brilliant, cheers.")


def any_first_turn(ep: Episode, s: Slots) -> None:
    s.rng.choice((t1_list, t1_read, t1_search))(ep, s)


def followup_ask(ep: Episode, s: Slots, fam: int) -> None:
    any_first_turn(ep, s)
    ep.user(FOLLOW_ASK[fam])
    key = json.dumps(ep.context)
    ep.say(_pick(ASK_FRAMES, key).format(ask=_pick(FILE_ASKS, "ask:" + key)))


def followup_thanks(ep: Episode, s: Slots, fam: int) -> None:
    any_first_turn(ep, s)
    ep.user(FOLLOW_THANKS[fam])
    ep.say(reply(THANKS_REPLIES, json.dumps(ep.context)))


KINDS: dict[str, Callable[[Episode, Slots, int], None]] = {
    "find_then_read": find_then_read, "check_then_read": check_then_read,
    "search_then_save": search_then_save, "list_then_write": list_then_write,
    "stats_then_search": stats_then_search, "followup_read": followup_read,
    "followup_stat": followup_stat, "followup_save": followup_save,
    "followup_ask": followup_ask, "followup_thanks": followup_thanks,
}


def _key(context: list[dict]) -> str:
    return json.dumps(context, sort_keys=True)


def build(seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    rows: list[dict] = []
    seen: dict[str, set[str]] = {s: set() for s in SPLITS}
    episodes = 0

    def add(split: str, kind: str, fam: int, pool: str) -> None:
        """An episode none of whose steps is already in the split. Evaluation
        splits never repeat a step (it would not be an independent case);
        training tolerates one after 50 tries."""
        nonlocal episodes
        for attempt in range(200):
            ep = Episode(Tree(rng))
            KINDS[kind](ep, Slots(rng, POOLS[pool]), fam)
            keys = [_key(st["context"]) for st in ep.steps]
            if not any(k in seen[split] for k in keys):
                break
            if split == "mt_train" and attempt >= 50:
                break
        else:
            return
        seen[split].update(keys)
        episode_id = f"{split}-ep{episodes:04d}"
        episodes += 1
        for i, st in enumerate(ep.steps):
            row = {"id": f"{split}-{len(rows):05d}", "split": split, "intent": kind,
                   "family": fam, "episode": episode_id, "step": i, "steps": len(ep.steps),
                   "request": next(m["content"] for m in reversed(st["context"])
                                   if m["role"] == "user"),
                   "context": st["context"], "expected": st["expected"],
                   "reply": st["reply"], "answer": st["answer"], "files": ep.tree.files}
            if st["call"] is not None:
                row["call"] = st["call"]
            rows.append(row)

    for kind in KINDS:
        for i in range(EPISODES_TRAIN):
            split = "mt_val" if rng.random() < VAL_FRACTION else "mt_train"
            add(split, kind, TRAIN_FAMILIES[i % len(TRAIN_FAMILIES)], "train")
        for i in range(EPISODES_TEST_ID):
            add("mt_test_id", kind, TRAIN_FAMILIES[i % len(TRAIN_FAMILIES)], "test")
        for i in range(EPISODES_TEST_OOD):
            add("mt_test_ood", kind, OOD_FAMILIES[i % len(OOD_FAMILIES)], "test")
    return rows


def write(rows: list[dict], out: Path) -> dict[str, int]:
    out.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for split in SPLITS:
        part = [r for r in rows if r["split"] == split]
        counts[split] = len(part)
        (out / f"{split}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                                    for r in part))
    return counts


def main() -> int:
    print(write(build(), ROOT / "data"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
