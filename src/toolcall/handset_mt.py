"""Convert a hand-written episode test set from its text form to JSONL, in
the step-case format of episodes.py (one row per scored model turn).

The text form (see data/test_hand6.txt), one message per line, a blank
line between episodes:

    E | kind                     starts an episode (a free label, e.g. find_then_read)
    U | message                  the user speaks
    c | tool arg="value" ...     history: a call already made (exact values)
    s | reply                    history: what the assistant already said
    C | tool arg=value ...       scored: the call the model should make now
    r | result                   what the tool returned (after every c and C; \\n = newline)
    A | fact; fact               scored: a reply with no call that contains every fact
    A | any: phrase; phrase      ... that contains at least one of the phrases
    A |                          ... with no call and no fact to check (ask, thank)

C uses test_hand5's argument rules (`a|b` any_of, `~=[w, w]` contains_all,
`?=` optional, paths expanded). After a scored C the history goes on with
one call that satisfies it (first alternative, words of a contains_all
joined, optional arguments left out), as in episodes.py: the model is
scored on each turn with the right history before it.

    python -m toolcall.handset_mt data/test_hand6.txt   # writes data/test_hand6.jsonl
"""

from __future__ import annotations

import sys
from pathlib import Path

from .handset import HandSetError, _expected, to_jsonl

TAGS = {"E", "U", "c", "s", "C", "r", "A"}


def concrete(expected: dict) -> dict:
    """One call satisfying `expected`: what the history shows after a scored C."""
    optional = set(expected.get("optional", ()))
    args: dict = {}
    for k, rule in expected["arguments"].items():
        if k in optional:
            continue
        if isinstance(rule, dict) and "any_of" in rule:
            args[k] = rule["any_of"][0]
        elif isinstance(rule, dict) and "contains_all" in rule:
            args[k] = " ".join(rule["contains_all"])
        else:
            args[k] = rule
    return {"name": expected["name"], "arguments": args}


def _answer(text: str) -> dict | None:
    if not text:
        return None
    key, body = ("any", text[4:]) if text.startswith("any:") else ("all", text)
    phrases = [p.strip() for p in body.split(";") if p.strip()]
    if not phrases:
        raise HandSetError("A has no facts after any:")
    return {key: phrases}


class _Episode:
    def __init__(self, kind: str):
        self.kind = kind
        self.context: list[dict] = []
        self.steps: list[dict] = []
        self.pending: dict | None = None        # a call waiting for its r line
        self.closed = False

    def add(self, tag: str, text: str) -> None:
        if self.closed:
            raise HandSetError("nothing may follow the scored A that ends an episode")
        if self.pending is not None and tag != "r":
            raise HandSetError("a call must be followed by its r line")
        if tag == "U":
            self.context.append({"role": "user", "content": text})
        elif tag == "s":
            self.context.append({"role": "assistant", "content": text})
        elif tag in ("c", "C"):
            expected = _expected(text)
            self.pending = concrete(expected)
            if tag == "C":
                self.steps.append({"context": [*self.context], "expected": expected,
                                   "call": self.pending, "answer": None})
        elif tag == "r":
            if self.pending is None:
                raise HandSetError("r without a call before it")
            self.context += [{"role": "assistant", "content": "", "tool_calls": [
                {"type": "function", "function": self.pending}]},
                {"role": "tool", "name": self.pending["name"],
                 "content": text.replace("\\n", "\n")}]
            self.pending = None
        elif tag == "A":
            self.steps.append({"context": [*self.context], "expected": None, "call": None,
                               "answer": _answer(text)})
            self.closed = True

    def check(self) -> None:
        if not any(m["role"] == "user" for m in self.context):
            raise HandSetError("an episode needs a U line")
        if not self.closed:
            raise HandSetError("an episode must end with a scored A line")


def _episodes(text: str) -> list[_Episode]:
    eps: list[_Episode] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tag, sep, body = line.partition(" |")
        body = body.strip()
        try:
            if not sep or tag not in TAGS:
                raise HandSetError(f"unknown line type {tag!r} (expected one of E U c s C r A)")
            if tag == "E":
                if eps:
                    eps[-1].check()
                eps.append(_Episode(body or "episode"))
            elif not eps:
                raise HandSetError("the first line of an episode is E | kind")
            else:
                eps[-1].add(tag, body)
        except HandSetError as e:
            raise HandSetError(f"line {number}: {e}") from None
    if eps:
        try:
            eps[-1].check()
        except HandSetError as e:
            raise HandSetError(f"last episode: {e}") from None
    return eps


def convert(text: str, split: str) -> list[dict]:
    rows: list[dict] = []
    for n, ep in enumerate(_episodes(text)):
        for i, st in enumerate(ep.steps):
            row = {"id": f"{split}-{len(rows):03d}", "split": split, "intent": ep.kind,
                   "family": -1, "episode": f"{split}-ep{n:03d}", "step": i,
                   "steps": len(ep.steps),
                   "request": next(m["content"] for m in reversed(st["context"])
                                   if m["role"] == "user"),
                   "context": st["context"], "expected": st["expected"], "reply": None,
                   "answer": st["answer"]}
            if st["call"] is not None:
                row["call"] = st["call"]
            rows.append(row)
    return rows


def main(argv: list[str]) -> None:
    if len(argv) != 1:
        raise SystemExit("usage: python -m toolcall.handset_mt data/<split>.txt")
    source = Path(argv[0])
    try:
        rows = convert(source.read_text(encoding="utf-8"), source.stem)
    except HandSetError as e:
        raise SystemExit(f"{source}: {e}") from None
    target = source.with_suffix(".jsonl")
    target.write_text(to_jsonl(rows), encoding="utf-8")
    episodes = len({r["episode"] for r in rows})
    print(f"{episodes} episodes, {len(rows)} scored steps -> {target}")


if __name__ == "__main__":
    main(sys.argv[1:])
