"""Episode shapes episodes.py never produces (v7's added training data).

v6 is right on every seed on hand-written episodes close to episodes.py's ten
kinds, and wrong on every seed on whole families those kinds never show:
long chains, a retry after a miss, stopping when the history already
answers, editing a file, picking a file from a listing, paging through a
long file, a user who corrects the last call, checking a write. One or two
kinds per family, written from what the family asks of the model, not from
the hand-written episodes:

  drill_down               list a folder, then its subfolder (one or two levels), read the file
  search_then_read_source  search the docs, then read the file the top chunk came from
  read_miss_then_list      read a path that is not there, list the folder, read the real file
  search_dead_end          a search that matches nothing: say so, do not search again
  empty_then_asked         the index was found empty; asked to search it: say it is empty
  missing_then_asked       a file was found missing; asked about it again: say it is missing
  size_from_listing        after a listing, "how big is x?": the listing has the size
  read_edit_write          read a config file, write it back with one setting changed or added
  list_then_stat           the largest or smallest file of a folder: list, stat it, give the date
  read_next_page           after lines 1-n of a log, "next n": read from line n+1
  user_corrects            "no, I meant the one in d": the same call on the right path
  write_then_check         after a write: read it back, or answer from the write (bytes, text)

Every final reply carries the values the episode gathered, as v6's grounded
replies do. Splits, families and pools as in episodes.py, plus pools of their
own (subfolders, config settings, log events, topics the docs do not cover),
disjoint between train and test. Own seed and own files: the single-turn data
and the v5/v6 episodes do not change.

    python -m toolcall.rare        # -> data/mt7_{train,val,test_id,test_ood}.jsonl
"""

from __future__ import annotations

import json
import random

from .corpus import CORPUS, NO_SUCH_FILE, Tree, chunk_path, stats_result
from .data import POOLS, ROOT, Slots, dir_rule, frame, path_rule
from .episodes import (
    EMPTY_ANSWER,
    LISTED_REPLIES,
    MISSING_ANSWER,
    MISSING_REPLIES,
    READ_REPLIES,
    T1_LIST,
    T1_READ,
    T1_SEARCH,
    Episode,
    Kind,
    answer_lines,
    call,
    contains,
    expect,
    generate,
    lines,
    one_of,
    reply,
    search,
    t1_list,
    write,
)

SEED = 20261125
SPLITS = ("mt7_train", "mt7_val", "mt7_test_id", "mt7_test_ood")
DIR_SIZE = 4096            # what ext4 reports for a small directory
ADD_P = 0.4                # read_edit_write: add a setting instead of changing one
DEPTHS = (1, 2)            # drill_down: subfolder levels below the named folder
PAGES = (4, 5, 8, 10)      # read_next_page: lines per page (20 would pass --max-length 1536)
NO_MATCH = "(no matching chunks)"
BELOW = ("(no chunk cleared the relevance threshold — the index is non-empty but nothing "
         "matched this query)")
EMPTY_INDEX = ("(index is empty — 0 chunks; check the --db path / ingest, this is NOT a "
               "no-match result)")

EXTRA: dict[str, dict] = {
    "train": {
        "subdirs": ["old", "v1", "q3", "inbox", "team", "misc"],
        "events": ["cache warmed", "job queued", "disk check ok", "user login",
                   "backup started", "backup finished", "config reloaded", "worker restarted",
                   "port bound", "retry scheduled", "index rebuilt", "token refreshed"],
        "config": {"port": ["8080", "9000", "3000"], "timeout": ["30", "45", "90"],
                   "workers": ["2", "4", "8"], "log_level": ["info", "debug", "warn"],
                   "retries": ["3", "5", "7"], "host": ["localhost", "0.0.0.0"],
                   "cache_mb": ["64", "256", "512"]},
        "cfg_exts": ["ini", "conf"],
        "absent": [("quantum annealing", ["quantum"]), ("the billing API", ["billing"]),
                   ("Kubernetes autoscaling", ["autoscal"]),
                   ("GraphQL federation", ["graphql"]), ("the mobile app", ["mobile"]),
                   ("OAuth refresh tokens", ["oauth"])],
    },
    "test": {
        "subdirs": ["attic", "wip", "legacy", "stash"],
        "events": ["parcel scanned", "invoice sent", "sensor offline", "sync complete",
                   "quota exceeded", "cron tick", "lease renewed", "upload failed"],
        "config": {"max_conn": ["64", "128", "256"], "batch_size": ["16", "32", "48"],
                   "shard_count": ["2", "6", "12"], "verbosity": ["quiet", "loud"],
                   "region": ["eu-west", "us-east"]},
        "cfg_exts": ["cfg", "env"],
        "absent": [("the payroll export", ["payroll"]), ("Bluetooth pairing", ["bluetooth"]),
                   ("the CDN cache", ["cdn"]), ("dark mode", ["dark mode"])],
    },
}


class RSlots(Slots):
    """Slot values from a pool of data.py and its pool of extra values here."""

    def __init__(self, rng: random.Random, pool: str):
        super().__init__(rng, POOLS[pool])
        self.x = EXTRA[pool]


class DirTree(Tree):
    """A tree whose listings show subfolders too, as filesystem-mcp does."""

    def subdirs(self, d: str) -> list[str]:
        prefix = d + "/"
        return sorted({p[len(prefix):].split("/", 1)[0] for p in self.files
                       if p.startswith(prefix) and "/" in p[len(prefix):]})

    def listing(self, d: str) -> str:
        rows = [(n, "file", self.size(f"{d}/{n}")) for n in self.entries(d)]
        rows += [(n, "dir", DIR_SIZE) for n in self.subdirs(d)]
        if not rows:
            return "(empty directory)"
        return "\n".join(f"{t:<5}{size:>12}  {n}" for n, t, size in sorted(rows))


def read_range(text: str, offset: int, limit: int) -> str:
    """fs_read with offset (1-based) and limit, as filesystem-mcp answers it."""
    part = "".join(text.splitlines(keepends=True)[offset - 1:offset - 1 + limit])
    return part or "(no lines in the requested range)"


def make(rng: random.Random, pool: str) -> tuple[Tree, Slots]:
    return DirTree(rng), RSlots(rng, pool)


def _file_in(s: RSlots, d: str, name: str, ext: str | None = None) -> str:
    return f"{d}/{name}.{ext or s.rng.choice(s.p['exts'])}"


def _read(ep: Episode, path: str) -> str:
    text = ep.tree.read(path)
    ep.call(call("fs_read", path=path), text, expect("fs_read", path=path_rule(path)))
    return text


def _list(ep: Episode, d: str, scored: bool = True) -> None:
    ep.call(call("fs_list", path=d), ep.tree.listing(d),
            expect("fs_list", path=dir_rule(d)) if scored else None)


def _say_read(ep: Episode, path: str, text: str) -> None:
    ep.say(reply(READ_REPLIES, path, f=path, c=text.rstrip("\n")), answer_lines(text))


# ---- long chains ----

DRILL = ("The {n} file is a couple of folders down inside {d}. Find it and read it.",
         "Somewhere under {d}, in a subfolder, there's a {n} file. Open it.",
         "Dig through {d} until you find the {n} file, then show it to me.",
         "I put {n} in a nested folder under {d}; read it out.",
         "Browse into {d} and its subfolders to find {n}, and print what it says.",
         "Go down the folders in {d} until you hit the {n} file. What's in it?",
         "{n} is buried in {d} somewhere, not at the top. Fetch its contents.",
         "Walk the tree under {d}, locate {n}, and tell me what the file says.")


def drill_down(ep: Episode, s: RSlots, fam: int) -> None:
    d = s.dir()
    subs = s.rng.sample(s.x["subdirs"], s.rng.choice(DEPTHS))
    levels = [d, *("/".join([d, *subs[:i + 1]]) for i in range(len(subs)))]
    target, *decoys = s.rng.sample(s.p["names"], len(levels) + 1)
    path = _file_in(s, levels[-1], target)
    ep.tree.add(path, lines(s))
    for level, decoy in zip(levels, decoys, strict=True):
        ep.tree.add(_file_in(s, level, decoy), lines(s))
    ep.user(frame(s.rng, s.p, DRILL[fam].format(n=target, d=d)))
    for level in levels:
        _list(ep, level)
    _say_read(ep, path, _read(ep, path))


SOURCE = ("Search the docs for {t} and then open the file that passage comes from.",
          "Find what the documentation says about {t}, and show me the whole source file.",
          "Look up {t} in the index, then read the document the top hit is from.",
          "Which file covers {t}? Search for it and print that file.",
          "Get the top passage on {t} and then open its source document.",
          "I want the full file behind the best search hit for {t}.",
          "Track down {t} in the knowledge base and pull up the original file it lives in.",
          "Run a doc search on {t}; whichever file ranks first, read it to me in full.")


def search_then_read_source(ep: Episode, s: RSlots, fam: int) -> None:
    topic, words = s.topic()
    path, (body, fact), more = chunk_path(topic), CORPUS[topic], s.content()
    ep.tree.add(path, f"{body}\n{more}\n")
    ep.user(frame(s.rng, s.p, SOURCE[fam].format(t=topic)))
    search(ep, s, topic, words, scored=True)
    text = _read(ep, path)
    ep.say(reply(READ_REPLIES, path, f=path, c=text.rstrip("\n")), contains(fact, more))


# ---- a retry after a miss, and a dead end ----

MISS = ("Read {f}. I'm not sure about the extension, though.",
        "Open {f}, or whatever the {n} file in {d} is actually called.",
        "Show me {f}; if that's not the exact name, find the {n} file in {d}.",
        "I think the file is {f}, but it might have another extension. Read it.",
        "Print {f}. If it's not there, look in {d} for the {n} file.",
        "Can you read {f}? The name might be slightly off.",
        "Pull up {f} (could be a different extension, I forget).",
        "Get me the {n} file from {d}; try {f} first.")
MISSED_READ = ("There's no {w}, but {f} is there:\n\n{c}",
               "{w} doesn't exist; the file is {f}. It says:\n\n{c}",
               "No {w}, so I looked in the folder and found {f}:\n\n{c}",
               "The file is actually {f}:\n\n{c}")


def read_miss_then_list(ep: Episode, s: RSlots, fam: int) -> None:
    d = s.dir()
    target, *others = s.rng.sample(s.p["names"], s.rng.randint(2, 3))
    real_ext, wrong_ext = s.rng.sample(s.p["exts"], 2)
    right, wrong = _file_in(s, d, target, real_ext), _file_in(s, d, target, wrong_ext)
    ep.tree.add(right, lines(s))
    for n in others:
        ep.tree.add(_file_in(s, d, n), lines(s))
    ep.user(frame(s.rng, s.p, MISS[fam].format(f=wrong, n=target, d=d)))
    ep.call(call("fs_read", path=wrong), NO_SUCH_FILE, expect("fs_read", path=path_rule(wrong)))
    _list(ep, d)
    text = _read(ep, right)
    ep.say(reply(MISSED_READ, right, w=wrong, f=right, c=text.rstrip("\n")),
           contains(right, *text.splitlines()))


DEAD = ("What do the docs say about {t}?", "Look up {t} in the documentation.",
        "Find me the passage on {t}.", "Is there anything in the index about {t}?",
        "Search the knowledge base for {t}.", "Pull up whatever the docs have on {t}.",
        "Dig {t} out of the indexed docs for me.",
        "Query the corpus on {t} and tell me what comes back.")
DEAD_REPLIES = ("I searched the docs for {t}, but nothing matched.",
                "The index has nothing on {t}: no matching chunks.",
                "No results for {t} in the docs.",
                "I couldn't find anything about {t} in the index.")
DEAD_ANSWER = one_of("nothing", "no match", "no result", "couldn't find", "could not find",
                     "didn't find", "did not find")


def search_dead_end(ep: Episode, s: RSlots, fam: int) -> None:
    topic, words = s.rng.choice(s.x["absent"])
    request = frame(s.rng, s.p, DEAD[fam].format(t=topic))
    ep.user(request)
    ep.call(call("crag_search", query=topic), s.rng.choice((NO_MATCH, BELOW)),
            expect("crag_search", ("k",), query={"contains_all": words},
                   k={"any_of": [1, 2, 3, 4, 5]}))
    ep.say(reply(DEAD_REPLIES, request, t=topic), DEAD_ANSWER)


# ---- the history already answers ----

T1_STATS = ("How many chunks are indexed?", "Show me the index stats.",
            "Is the index populated?")
EMPTY_SAID = ("The index is empty: 0 chunks, 0 files.", "Nothing is indexed yet (0 chunks).",
              "The index has no chunks.")
AFTER_EMPTY = ("OK, search it for {t}.", "Then look up {t}.", "What does it say about {t}?",
               "Find the passage on {t} then.", "Can you check it for anything on {t}?",
               "So, anything about {t} in there?", "Right, and {t}? Search for that.",
               "Fine. Pull up {t} from it.")
EMPTY_AGAIN = ("The index is still empty (0 chunks), so there's nothing to search for {t}.",
               "There's nothing to search: the index has 0 chunks.",
               "I can't find {t}: the index is empty.",
               "The index has no chunks yet, so a search for {t} would return nothing.")


def empty_then_asked(ep: Episode, s: RSlots, fam: int) -> None:
    first, _ = s.topic()
    if s.rng.random() < 0.5:
        ep.user(s.rng.choice(T1_STATS))
        ep.call(call("crag_stats"), stats_result(0, 0))
    else:
        ep.user(s.rng.choice(T1_SEARCH).format(t=first))
        ep.call(call("crag_search", query=first), EMPTY_INDEX)
    ep.say(s.rng.choice(EMPTY_SAID), scored=False)
    topic, _ = s.topic()
    request = AFTER_EMPTY[fam].format(t=topic)
    ep.user(request)
    ep.say(reply(EMPTY_AGAIN, request, t=topic), EMPTY_ANSWER)


T1_EXISTS = ("Does {f} exist?", "Is there a file at {f}?", "Check {f} for me.")
AFTER_MISSING = ("How big is it?", "When was {f} last changed?", "OK, so what does it say?",
                 "Show me its first line then.", "What are its permissions?",
                 "Then read {f} to me.", "Just give me the contents of {f}.",
                 "And the size of that file?")
STILL_MISSING = ("{f} doesn't exist, as the last check showed.",
                 "There is no {f}: the server said no such file a moment ago.",
                 "{f} isn't there, so I can't do that.",
                 "That file does not exist: {f} came back as no such file.")


def missing_then_asked(ep: Episode, s: RSlots, fam: int) -> None:
    f = s.file()
    if s.rng.random() < 0.5:
        ep.user(s.rng.choice(T1_READ).format(f=f))
        ep.call(call("fs_read", path=f), NO_SUCH_FILE)
    else:
        ep.user(s.rng.choice(T1_EXISTS).format(f=f))
        ep.call(call("fs_stat", path=f), NO_SUCH_FILE)
    ep.say(reply(MISSING_REPLIES, f, f=f), scored=False)
    ep.user(AFTER_MISSING[fam].format(f=f))
    ep.say(reply(STILL_MISSING, f + str(fam), f=f), MISSING_ANSWER)


ORDINALS = ("first", "second", "third")
SIZE_LIST = ("How big is {n}?", "What's the size of {n}?", "And {n}, how many bytes?",
             "How large is the {o} one?", "Is {n} big?", "What does {n} weigh in bytes?",
             "Size of {n}, please.", "How many bytes is the {o} file?")
LISTED_SIZE = ("{n} is {v} bytes.", "The listing says {n} is {v} bytes.",
               "{n}: {v} bytes.", "It's {v} bytes, according to the listing.")


def size_from_listing(ep: Episode, s: RSlots, fam: int) -> None:
    d, names = t1_list(ep, s)
    i = s.rng.randrange(min(len(ORDINALS), len(names)))
    v = str(ep.tree.size(f"{d}/{names[i]}"))
    ep.user(SIZE_LIST[fam].format(n=names[i], o=ORDINALS[i]))
    ep.say(reply(LISTED_SIZE, d + names[i], n=names[i], v=v), contains(v))


# ---- read, edit, write ----

EDIT_SET = ("In {f}, set {k} to {v}.", "Change {k} to {v} in {f}.",
            "Update {f} so that {k} is {v}.", "{f} needs {k} = {v}; fix it.",
            "Edit {f}: {k} should be {v} now.", "Make {k} {v} in {f}.",
            "Bump {k} to {v} over in {f}.", "Could you flip {k} in {f} to {v}?")
EDIT_ADD = ("Add {k} = {v} to {f}.", "Append the setting {k} = {v} to {f}.",
            "Put a line {k} = {v} at the end of {f}.", "{f} is missing {k} = {v}; add it.",
            "Insert {k} = {v} into {f}.", "Extend {f} with {k} = {v}.",
            "Tack {k} = {v} onto {f}.", "Slip a new entry {k} = {v} into {f}.")
EDITED = ("Updated {f}: {k} is now {v}.", "Done. {f} now has {k} = {v}.",
          "{f} is saved with {k} set to {v}.", "I rewrote {f}; {k} = {v}.")


def _render(settings: dict[str, str]) -> str:
    return "".join(f"{k} = {v}\n" for k, v in settings.items())


def read_edit_write(ep: Episode, s: RSlots, fam: int) -> None:
    f = _file_in(s, s.dir(), s.rng.choice(s.p["names"]), s.rng.choice(s.x["cfg_exts"]))
    keys = s.rng.sample(sorted(s.x["config"]), s.rng.randint(3, 4))
    settings = {k: s.rng.choice(s.x["config"][k]) for k in keys[:-1]}
    if s.rng.random() < ADD_P:
        k, template = keys[-1], EDIT_ADD[fam]
        v = s.rng.choice(s.x["config"][k])
    else:
        k, template = s.rng.choice(keys[:-1]), EDIT_SET[fam]
        v = s.rng.choice([x for x in s.x["config"][k] if x != settings[k]])
    ep.tree.add(f, _render(settings))
    ep.user(frame(s.rng, s.p, template.format(f=f, k=k, v=v)))
    _read(ep, f)
    content = _render({**settings, k: v})
    kept = [x for x in settings if x != k]
    ep.call(call("fs_write", path=f, content=content), Tree.write(f, content),
            expect("fs_write", path=path_rule(f), content={"contains_all": [k, v, *kept]}))
    ep.say(reply(EDITED, f, f=f, k=k, v=v), contains(f, v))


# ---- a listing, then the metadata of the file it picks ----

LIST_STAT = ("When was the {w} file in {d} last modified?",
             "Find the {w} file in {d} and tell me when it last changed.",
             "What's the modification date of the {w} file in {d}?",
             "In {d}, which file is the {w}, and when was it last touched?",
             "Check {d}: when did its {w} file last change?",
             "Look in {d} and get me the last-modified date of the {w} file.",
             "Date stamp on the {w} thing in {d}?",
             "{d}: pick out the {w} file and give me its mtime.")
WHICH = {"largest": max, "biggest": max, "smallest": min}
PICKED = ("The {w} file is {n}, last modified on {v}.", "{n} is the {w}; it last changed on {v}.",
          "{n} ({w} in {d}) was modified on {v}.", "Last modified {v}: that's {n}, the {w} file.")


def list_then_stat(ep: Episode, s: RSlots, fam: int) -> None:
    d = s.dir()
    sizes: dict[str, int] = {}
    for n in s.rng.sample(s.p["names"], s.rng.randint(3, 4)):
        text = lines(s)
        while len(text.encode()) in sizes.values():
            text += s.content() + "\n"
        path = _file_in(s, d, n)
        ep.tree.add(path, text)
        sizes[path] = len(text.encode())
    w = s.rng.choice(sorted(WHICH))
    path = WHICH[w](sizes, key=sizes.__getitem__)
    ep.user(frame(s.rng, s.p, LIST_STAT[fam].format(w=w, d=d)))
    _list(ep, d)
    ep.call(call("fs_stat", path=path), ep.tree.stat(path), expect("fs_stat", path=path_rule(path)))
    name, date = path.rsplit("/", 1)[1], ep.tree.files[path]["modified"][:10]
    ep.say(reply(PICKED, path, w=w, n=name, v=date, d=d), contains(name, date))


# ---- a long file, page by page ----

T1_HEAD = ("Show me the first {n} lines of {f}.", "Print lines 1 to {n} of {f}.",
           "Read the top {n} lines of {f}.")
NEXT = (("Next {n}.", True), ("Show me the next {n} lines.", True),
        ("Keep going, {n} more.", True), ("And the following {n}?", True),
        ("Continue from where you stopped.", False), ("More, please.", False),
        ("Give me another {n} after those.", True), ("Carry on reading.", False))
PAGE_REPLIES = ("Lines {a}–{b} of {f}:\n\n{c}", "Here are lines {a} to {b}:\n\n{c}",
                "{f}, lines {a}-{b}:\n\n{c}", "This is {f} from line {a} to {b}:\n\n{c}")


def _log(s: RSlots, count: int) -> str:
    t = s.rng.randint(0, 20 * 3600)
    out = []
    for _ in range(count):
        t += s.rng.randint(1, 90)
        h, m, sec = t // 3600 % 24, t // 60 % 60, t % 60
        out.append(f"{h:02d}:{m:02d}:{sec:02d} {s.rng.choice(s.x['events'])}\n")
    return "".join(out)


def read_next_page(ep: Episode, s: RSlots, fam: int) -> None:
    f = _file_in(s, s.dir(), s.rng.choice(s.p["names"]), "log")
    n = s.rng.choice(PAGES)
    text = _log(s, s.rng.randint(2 * n + 1, 3 * n + 5))
    ep.tree.add(f, text)
    ep.user(s.rng.choice(T1_HEAD).format(n=n, f=f))
    first = read_range(text, 1, n)
    ep.call(call("fs_read", path=f, offset=1, limit=n), first)
    ep.say(reply(PAGE_REPLIES, f, a=1, b=n, f=f, c=first.rstrip("\n")), scored=False)
    request, numbered = NEXT[fam]
    ep.user(request.format(n=n))
    page = read_range(text, n + 1, n)
    ep.call(call("fs_read", path=f, offset=n + 1, limit=n), page,
            expect("fs_read", () if numbered else ("limit",), path=path_rule(f),
                   offset=n + 1, limit=n))
    shown = page.splitlines()
    ep.say(reply(PAGE_REPLIES, f + "+", a=n + 1, b=n + len(shown), f=f, c=page.rstrip("\n")),
           contains(shown[0], shown[-1]))


# ---- the user corrects the last call ----

CORRECT_READ = ("No, I meant the one in {d}.", "Wrong folder: the {n} file in {d}.",
                "Not that one, the copy under {d}.", "Sorry, I meant {d}/{f}.",
                "That's the old one; read the one in {d}.", "Hmm, no. Try {d} instead.",
                "Nope, other directory: {d}.", "I was thinking of {d}'s version, not that.")
CORRECT_LIST = ("No, I meant {d}.", "Wrong folder, list {d}.", "Not that one: {d}.",
                "Sorry, I meant the {d} folder.", "That's not it; show me {d}.",
                "Hmm, no. Try {d}.", "Nope, other directory: {d}.",
                "I was thinking of {d}, not that.")


def _correct_read(ep: Episode, s: RSlots, fam: int, d1: str, d2: str) -> None:
    name = s.rng.choice(s.p["names"])
    fname = f"{name}.{s.rng.choice(s.p['exts'])}"
    a, b = f"{d1}/{fname}", f"{d2}/{fname}"
    ep.tree.add(a, lines(s))
    text = lines(s)
    while text == ep.tree.read(a):
        text = lines(s)
    ep.tree.add(b, text)
    ep.user(s.rng.choice(T1_READ).format(f=a))
    ep.call(call("fs_read", path=a), ep.tree.read(a))
    ep.say(reply(READ_REPLIES, a, f=a, c=ep.tree.read(a).rstrip("\n")), scored=False)
    ep.user(CORRECT_READ[fam].format(d=d2, n=name, f=fname))
    _say_read(ep, b, _read(ep, b))


def _correct_list(ep: Episode, s: RSlots, fam: int, d1: str, d2: str) -> None:
    names = s.rng.sample(s.p["names"], 5)
    for n in names[:2]:
        ep.tree.add(_file_in(s, d1, n), lines(s))
    for n in names[2:]:
        ep.tree.add(_file_in(s, d2, n), lines(s))
    ep.user(s.rng.choice(T1_LIST).format(d=d1))
    _list(ep, d1, scored=False)
    ep.say(reply(LISTED_REPLIES, d1, d=d1, n=", ".join(ep.tree.entries(d1))), scored=False)
    ep.user(CORRECT_LIST[fam].format(d=d2))
    _list(ep, d2)
    found = ep.tree.entries(d2)
    ep.say(reply(LISTED_REPLIES, d2, d=d2, n=", ".join(found)), contains(*found))


def user_corrects(ep: Episode, s: RSlots, fam: int) -> None:
    d1, d2 = s.rng.sample(s.p["dirs"], 2)
    (_correct_read if s.rng.random() < 0.5 else _correct_list)(ep, s, fam, d1, d2)


# ---- checking a write ----

T1_WRITE = ("Write '{c}' to {f}.", "Save the text '{c}' in {f}.", "Create {f} containing: {c}")
SAVED = ("Saved to {f}.", "Done, it's in {f}.", "I wrote it to {f}.")
READBACK = ("Read it back from disk.", "Open the file again so I can check it saved right.",
            "Re-read {f} to confirm.", "Read the file back to me.", "Load {f} again and show me.",
            "Check the file by reading it back.", "Pull {f} up off the disk again.",
            "Verify by reading the file once more.")
BYTES = ("How many bytes did you write?", "How big did that write come out?",
         "What was the byte count of that write?", "What did that write come to, in bytes?",
         "Was that a big write? How many bytes?", "How large was what you wrote?",
         "Byte total on that save?", "Size of that write, in bytes?")
WHAT = ("Remind me what you wrote there.", "What text did you save?", "What did you put in it?",
        "Tell me what you wrote.", "What was the text again?", "What did I ask you to save?",
        "Recap what you just saved.", "Which words went into the file?")
BYTES_REPLIES = ("That write was {v} bytes.", "{f} came out at {v} bytes.",
                 "I wrote {v} bytes to {f}.", "It's {v} bytes.")
WHAT_REPLIES = ("I wrote '{c}' to {f}.", "{f} contains: {c}", "The text was: {c}",
                "I saved '{c}'.")


def write_then_check(ep: Episode, s: RSlots, fam: int) -> None:
    f, c = s.file(), s.content()
    ep.user(s.rng.choice(T1_WRITE).format(c=c, f=f))
    ep.call(call("fs_write", path=f, content=c), Tree.write(f, c))
    ep.say(reply(SAVED, f, f=f), scored=False)
    what = s.rng.choice(("read", "bytes", "what"))
    if what == "read":
        ep.user(READBACK[fam].format(f=f))
        ep.call(call("fs_read", path=f), c, expect("fs_read", path=path_rule(f)))
        ep.say(reply(READ_REPLIES, f, f=f, c=c), contains(c))
    elif what == "bytes":
        ep.user(BYTES[fam])
        v = str(len(c.encode()))
        ep.say(reply(BYTES_REPLIES, f, f=f, v=v), contains(v))
    else:
        ep.user(WHAT[fam])
        ep.say(reply(WHAT_REPLIES, f, f=f, c=c), contains(c))


KINDS: dict[str, Kind] = {
    "drill_down": drill_down, "search_then_read_source": search_then_read_source,
    "read_miss_then_list": read_miss_then_list, "search_dead_end": search_dead_end,
    "empty_then_asked": empty_then_asked, "missing_then_asked": missing_then_asked,
    "size_from_listing": size_from_listing, "read_edit_write": read_edit_write,
    "list_then_stat": list_then_stat, "read_next_page": read_next_page,
    "user_corrects": user_corrects, "write_then_check": write_then_check,
}


def build(seed: int = SEED) -> list[dict]:
    return generate(KINDS, SPLITS, seed, make)


def main() -> int:
    print(json.dumps(write(build(), ROOT / "data", SPLITS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
