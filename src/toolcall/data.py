"""The dataset: user requests paired with the tool call they need (or none).

Every case is generated from an intent, a phrasing *family* and slot
values (file names, folders, search topics, contents), with a fixed seed.
The expected call is built from the slots, so it is right by construction,
and every one is checked by cMCP's validator (tests/test_data.py).

Splits, so the test measures generalisation and not recall:

  train, val   phrasing families 0-5, slot values from the TRAIN pools
  test_id      families 0-5, slot values from the TEST pools: known wording,
               names and topics never seen in training
  test_ood     families 6-7 (held out) and TEST pools: wording and values
               both unseen

Requests that need no call come in three kinds, each its own intent:
  no_tool      answerable without tools (chit-chat, general knowledge)
  unsupported  asks for something no tool does (delete, email, weather)
  ambiguous    a tool fits but a required value is missing: ask, don't guess

    python -m toolcall.data            # -> data/{train,val,test_id,test_ood}.jsonl
"""

from __future__ import annotations

import json
import random
from collections.abc import Callable
from pathlib import Path

SEED = 20261110
ROOT = Path(__file__).resolve().parents[2]
TRAIN_FAMILIES = range(0, 6)
OOD_FAMILIES = (6, 7)
SPLITS = ("train", "val", "test_id", "test_ood")

SYSTEM = ("You are an assistant with tools for a document index (crag_*) and a sandboxed "
          "file tree (fs_*); paths are relative to the sandbox root. Call a tool when the "
          "request needs one. If a value the tool needs is missing, ask for it instead of "
          "guessing. If no tool fits, answer directly.")

# ---- slot pools: disjoint between train and test ------------------------

POOLS = {
    "train": {
        "dirs": ["notes", "docs", "src", "reports", "config", "meetings", "assets/img"],
        "names": ["plan", "todo", "setup", "summary", "budget", "changelog", "roadmap",
                  "minutes", "design", "release-notes", "index", "faq"],
        "exts": ["md", "txt", "c", "json", "yaml", "csv"],
        "topics": [
            ("BM25 parameters", ["bm25"]), ("reciprocal rank fusion", ["rank fusion"]),
            ("the relevance gate", ["relevance"]), ("embedding dimension", ["embedding"]),
            ("the stdio transport", ["stdio"]), ("JSON-RPC error codes", ["error code"]),
            ("schema validation", ["schema"]), ("the worker thread pool", ["thread pool"]),
            ("fuzzing harnesses", ["fuzz"]), ("SSE resumption", ["sse"]),
            ("chunking strategy", ["chunk"]), ("cosine similarity", ["cosine"]),
            ("the HTTP origin check", ["origin"]), ("protocol version negotiation", ["version"]),
            ("handler timeouts", ["timeout"]), ("the replay gate", ["replay"]),
            ("WAL mode in SQLite", ["wal"]), ("the Python binding", ["binding"]),
        ],
        "root_phrases": ["the root folder", "the top level"],
        "contents": ["buy milk and eggs", "meeting moved to Thursday", "TODO: fix the parser",
                     "version 0.3 released", "call the dentist", "deadline is March 3",
                     "draft one, do not share", "hello world"],
    },
    "test": {
        "dirs": ["drafts", "research", "scripts", "archive", "data/raw"],
        "names": ["proposal", "results", "notes-2026", "checklist", "outline", "invoice",
                  "agenda", "readme"],
        "exts": ["md", "txt", "py", "toml"],
        "topics": [
            ("the SSRF egress guard", ["ssrf"]), ("log redaction", ["redact"]),
            ("cancellation of requests", ["cancel"]), ("the HNSW index", ["hnsw"]),
            ("nDCG evaluation", ["ndcg"]), ("rate limiting at accept", ["rate limit"]),
            ("subscriptions", ["subscription"]), ("structured tool output", ["structured"]),
            ("the soak test", ["soak"]),
        ],
        "root_phrases": ["the sandbox root", "the base directory"],
        "contents": ["pick up the parcel", "budget approved", "lunch at noon on Friday",
                     "rerun the benchmark", "all tests passing"],
    },
}


class Slots:
    """Random slot values from one pool."""

    def __init__(self, rng: random.Random, pool: dict):
        self.rng, self.p = rng, pool

    def dir(self) -> str:
        return self.rng.choice(self.p["dirs"])

    def file(self) -> str:
        return f"{self.dir()}/{self.rng.choice(self.p['names'])}.{self.rng.choice(self.p['exts'])}"

    def topic(self) -> tuple[str, list[str]]:
        return self.rng.choice(self.p["topics"])

    def content(self) -> str:
        return self.rng.choice(self.p["contents"])


def path_rule(path: str) -> dict:
    """A relative path, with or without a leading ./ (the server takes both)."""
    return {"any_of": [path, f"./{path}"]}


def dir_rule(d: str) -> dict:
    return {"any_of": [d, f"{d}/", f"./{d}"]}


# ---- intents: families of phrasings -> (request, expected call, reply) ----
# Each family is one way of asking; 0-5 train, 6-7 are held out for test_ood.

Gen = Callable[..., tuple[str, dict | None, str | None]]


def crag_search(s: Slots, fam: int):
    topic, words = s.topic()
    t = ["Search the docs for {t}.", "Can you look up {t} in the documentation?",
         "Find me the passages about {t}.", "What does the index say about {t}?",
         "I need info on {t}; check the knowledge base.",
         "Look through the indexed docs for anything on {t}.",
         "Pull up whatever the corpus has regarding {t}.",
         "Run a retrieval on {t}, please."][fam].format(t=topic)
    args: dict = {"query": {"contains_all": words}, "k": 5}
    optional = ["k"]
    if s.rng.random() < 0.35:
        k = s.rng.choice([1, 2, 3, 8, 10])
        t += " Just the single best hit." if k == 1 else \
            [" Just the top {k} hits.", " Give me {k} results.", " Limit it to {k}."][fam % 3] \
            .format(k=k)
        args["k"], optional = k, []
    return t, {"name": "crag_search", "arguments": args, "optional": optional}, None


def crag_stats(s: Slots, fam: int):
    t = ["How many chunks are in the index?", "Is the search index empty?",
         "Show me the index statistics.", "What embedding dimension does the index use?",
         "How many files have been indexed?", "Give me diagnostics on the retrieval database.",
         "Report the size of the document index.", "Is anything actually indexed right now?"]
    return t[fam], {"name": "crag_stats", "arguments": {}}, None


def fs_list(s: Slots, fam: int):
    if s.rng.random() < 0.2:
        where = s.rng.choice(s.p["root_phrases"])
        arguments, optional = {"path": {"any_of": ["", "."]}}, ["path"]
    else:
        d = s.dir()
        where, arguments, optional = d, {"path": dir_rule(d)}, []
    t = ["List the files in {w}.", "What's inside {w}?", "Show me the contents of {w}.",
         "ls {w}", "Which files are under {w}?", "Enumerate the entries of {w}.",
         "Give me a directory listing for {w}.", "What does {w} contain?"][fam].format(w=where)
    return t, {"name": "fs_list", "arguments": arguments, "optional": optional}, None


def fs_read(s: Slots, fam: int):
    f = s.file()
    mode = s.rng.choices(["whole", "head", "range", "from"], weights=[5, 2, 2, 1])[0]
    args: dict = {"path": path_rule(f)}
    optional: list[str] = []
    if mode == "whole":
        t = ["Open {f} and show it to me.", "Read {f}.", "What's in {f}?",
             "Print the contents of {f}.", "cat {f}", "Show me {f}.",
             "Display the file {f} for me.", "Let me see what {f} says."][fam].format(f=f)
    elif mode == "head":
        n = s.rng.choice([5, 10, 20, 50])
        t = ["Show the first {n} lines of {f}.", "Read just the first {n} lines of {f}.",
             "What are the first {n} lines in {f}?", "Print {f}, first {n} lines only.",
             "head -n {n} {f}", "Give me the top {n} lines of {f}.",
             "I only need the opening {n} lines of {f}.",
             "Peek at {f}: {n} lines from the start."][fam].format(n=n, f=f)
        args |= {"limit": n, "offset": 1}
        optional = ["offset"]
    elif mode == "range":
        a = s.rng.choice([3, 10, 25, 40])
        b = a + s.rng.choice([4, 9, 20])
        t = ["Read lines {a} to {b} of {f}.", "Show {f}, lines {a} through {b}.",
             "What's on lines {a}-{b} of {f}?", "Print lines {a} to {b} from {f}.",
             "I need lines {a} to {b} in {f}.", "Give me {f} from line {a} to line {b}.",
             "Extract lines {a}..{b} of {f}.",
             "Between lines {a} and {b} inclusive, what does {f} say?"][fam] \
            .format(a=a, b=b, f=f)
        args |= {"offset": a, "limit": b - a + 1}
    else:
        a = s.rng.choice([5, 12, 30, 100])
        t = ["Show {f} starting at line {a}.", "Read {f} from line {a} onwards.",
             "Print {f}, skipping the first {p} lines.", "Open {f} at line {a}.",
             "What does {f} say from line {a} to the end?", "Continue reading {f} at line {a}.",
             "Resume {f} from line {a}.", "Everything in {f} after line {p}, please."][fam] \
            .format(f=f, a=a, p=a - 1)
        args |= {"offset": a}
    return t, {"name": "fs_read", "arguments": args, "optional": optional}, None


def fs_stat(s: Slots, fam: int):
    f = s.file()
    t = ["How big is {f}?", "When was {f} last modified?", "What are the permissions on {f}?",
         "Is {f} a file or a directory?", "Get the metadata for {f}.", "stat {f}",
         "Check the size and modification time of {f}.", "Tell me the mode bits of {f}."][fam]
    return t.format(f=f), {"name": "fs_stat", "arguments": {"path": path_rule(f)}}, None


def fs_write(s: Slots, fam: int):
    f, c = s.file(), s.content()
    t = ["Create {f} containing: {c}", "Write \"{c}\" to {f}.", "Save the text '{c}' as {f}.",
         "Make a new file {f} with the content \"{c}\".", "Overwrite {f} with: {c}",
         "Put this in {f}: {c}", "Store the following in {f}: {c}",
         "Could you write {f}? It should say: {c}"][fam].format(f=f, c=c)
    return t, {"name": "fs_write", "arguments": {"path": path_rule(f), "content": c}}, None


NO_TOOL = {
    "train": ["Thanks, that's all for now.", "What's 17 times 23?",
              "Translate 'good morning' into Italian.", "Hi! How are you today?",
              "Write a haiku about autumn.", "What's the difference between TCP and UDP?",
              "Explain recursion in one sentence.", "Suggest a name for a black cat.",
              "Is a tomato a fruit or a vegetable?", "Convert 30 degrees Celsius to Fahrenheit.",
              "Give me a synonym for 'quick'.", "What year did the Berlin Wall fall?",
              "How do I say thank you in Japanese?", "Tell me a short joke.",
              "What does HTTP stand for?", "Rewrite this more politely: send me the file now.",
              "Spell 'necessary' backwards.", "What is the capital of Canada?",
              "Recommend a good habit for mornings.", "How many days are in a leap year?"],
    "test": ["Good night, talk tomorrow.", "What's 144 divided by 12?",
             "Translate 'see you soon' into French.", "Write a limerick about coffee.",
             "What's the difference between a list and a tuple in Python?",
             "Who wrote Pride and Prejudice?", "Give me an antonym for 'ancient'.",
             "How many minutes are in a day?", "Explain what an API is to a child.",
             "What's the boiling point of water at sea level?"],
}
UNSUPPORTED = {
    "train": [("Delete {f}.", "delete files"), ("Rename {f} to {g}.", "rename files"),
              ("Send an email to Marta saying I'm late.", "send email"),
              ("What's the weather in Rome tomorrow?", "check the weather"),
              ("Run the test suite.", "run commands"), ("Move {f} into the trash.", "delete files"),
              ("Book a table for two at 8pm.", "make bookings"),
              ("Reindex the documents.", "rebuild the index"),
              ("Change the permissions of {f} to 600.", "change permissions"),
              ("Download https://example.com/data.csv.", "download from the web")],
    "test": [("Remove {f} permanently.", "delete files"),
             ("Text my brother that dinner is at 7.", "send messages"),
             ("Copy {f} to {g}.", "copy files"), ("Restart the server.", "run commands"),
             ("Add the new PDFs to the search index.", "rebuild the index")],
}
TOOLS_SUMMARY = ("search and inspect the document index, and list, read, stat or write "
                 "files in the sandbox")
AMBIGUOUS = {
    "train": [("Read the file.", "Which file should I read?"),
              ("Search for it.", "What should I search the documentation for?"),
              ("Write that down.", "Which file should I write to, and what should it say?"),
              ("How big is that one?", "Which file do you mean?"),
              ("Create a file for my notes.", "What should the file be called, and what "
               "should it contain?"),
              ("Show me lines 10 to 20.", "Which file should I read those lines from?"),
              ("Save this in {f}.", "What text should I save in {f}?"),
              ("Look it up in the docs.", "What would you like me to look up?")],
    "test": [("Open it.", "Which file should I open?"),
             ("Put the summary in a file.", "Which file, and what summary should it contain?"),
             ("When was it changed?", "Which file do you mean?"),
             ("Find the part about that in the docs.", "Which topic should I search for?")],
}


def no_tool(s: Slots, fam: int, pool: str):
    return s.rng.choice(NO_TOOL[pool]), None, None          # reply distilled from the base model


def unsupported(s: Slots, fam: int, pool: str):
    t, what = s.rng.choice(UNSUPPORTED[pool])
    reply = f"I can't {what}: my tools can only {TOOLS_SUMMARY}."
    return t.format(f=s.file(), g=s.file()), None, reply


def ambiguous(s: Slots, fam: int, pool: str):
    t, ask = s.rng.choice(AMBIGUOUS[pool])
    f = s.file()
    return t.format(f=f), None, ask.format(f=f)


CALL_INTENTS: dict[str, tuple[Gen, int]] = {     # intent -> (generator, train+val cases)
    "crag_search": (crag_search, 300), "crag_stats": (crag_stats, 90),
    "fs_list": (fs_list, 190), "fs_read": (fs_read, 360), "fs_stat": (fs_stat, 150),
    "fs_write": (fs_write, 200),
}
NOCALL_INTENTS: dict[str, tuple[Gen, int]] = {
    "no_tool": (no_tool, 150), "unsupported": (unsupported, 110), "ambiguous": (ambiguous, 130)}
VAL_FRACTION = 0.1
TEST_ID_PER_INTENT = 20
TEST_OOD_PER_INTENT = 35


def canonical_call(expected: dict) -> dict:
    """One concrete call satisfying `expected`, to train on: the first
    alternative of each rule and optional arguments left out."""
    optional = set(expected.get("optional", ()))
    args = {}
    for k, rule in expected["arguments"].items():
        if k in optional:
            continue
        if isinstance(rule, dict) and "any_of" in rule:
            args[k] = rule["any_of"][0]
        elif isinstance(rule, dict) and "contains_all" in rule:
            raise ValueError("free-text arguments need the request's wording")
        else:
            args[k] = rule
    return {"name": expected["name"], "arguments": args}


def training_call(request: str, expected: dict) -> dict:
    """The concrete call a training example shows. A free-text query is the
    request's topic phrase as the user wrote it."""
    exp = {**expected, "arguments": dict(expected["arguments"])}
    q = exp["arguments"].get("query")
    if isinstance(q, dict) and "contains_all" in q:
        exp["arguments"]["query"] = _topic_phrase(request, q["contains_all"])
    return canonical_call(exp)


def _topic_phrase(request: str, words: list[str]) -> str:
    for pool in POOLS.values():
        for phrase, w in pool["topics"]:
            if w == words and phrase in request:
                return phrase
    raise ValueError(f"no topic phrase for {words} in {request!r}")


def build(seed: int = SEED) -> list[dict]:
    rng = random.Random(seed)
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()
    repeats_ok = ("no_tool", "crag_stats", "unsupported", "ambiguous")   # small fixed sets

    def add(split: str, intent: str, fam: int, pool: str, gen: Gen) -> None:
        for _ in range(50):              # avoid exact duplicate requests within a split
            s = Slots(rng, POOLS[pool])
            req, exp, reply = gen(s, fam) if intent in CALL_INTENTS else gen(s, fam, pool)
            if (split, req) not in seen or intent in repeats_ok:
                break
        seen.add((split, req))
        row = {"id": f"{split}-{len(rows):05d}", "split": split, "intent": intent,
               "family": fam, "request": req, "expected": exp, "reply": reply}
        if exp is not None:
            row["call"] = training_call(req, exp)
        rows.append(row)

    for intent, (gen, n) in {**CALL_INTENTS, **NOCALL_INTENTS}.items():
        for i in range(n):
            split = "val" if rng.random() < VAL_FRACTION else "train"
            add(split, intent, TRAIN_FAMILIES[i % len(TRAIN_FAMILIES)], "train", gen)
        for i in range(TEST_ID_PER_INTENT):
            add("test_id", intent, TRAIN_FAMILIES[i % len(TRAIN_FAMILIES)], "test", gen)
        for i in range(TEST_OOD_PER_INTENT):
            add("test_ood", intent, OOD_FAMILIES[i % len(OOD_FAMILIES)], "test", gen)
    return rows


def load(split: str, data: Path = ROOT / "data") -> list[dict]:
    return [json.loads(line) for line in (data / f"{split}.jsonl").read_text().splitlines()
            if line.strip()]


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
