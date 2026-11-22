"""Grounded final replies: the episodes of episodes.py with final turns that
report the values the episode gathered (v6's targets, and DPO's "chosen").

v5 was trained on episodes whose final reply after a write only names the
file ("Saved to notes/a.md."), and whose reply after a stat-then-read
drops the size. It learned exactly that: on the hand-written test_hand6
it leaves out the value the user asked for. Here only those final turns
change:

  search_then_save, followup_save   "Saved to f. It says: <the passage>"
  list_then_write                   "Saved to f: a.md, b.txt."
  check_then_read (file present)    "f exists (35 bytes). Here it is: ..."

and each one's answer rule now asks for the values too (the fact or the
names written, the size), not only the file name. Every call, every
context and every other turn is unchanged, so a model's calls are scored
exactly as on the episodes, and the old replies fail the new rules.

    python -m toolcall.grounded   # -> data/mt_{train,val,test_id,test_ood}_g.jsonl
"""

from __future__ import annotations

import json
import re

from .data import ROOT, _pick
from .episodes import SPLITS

SAVED_SAYS = ("Saved to {f}. It says: {c}", "Done: {f} now holds this passage: {c}",
              "I wrote the passage to {f}: {c}", "It's in {f} now: {c}")
SAVED_NAMES = ("Saved to {f}: {c}.", "Done: {f} now lists {c}.", "I wrote {c} to {f}.",
               "It's in {f} now: {c}.")
EXISTS_READ = ("{f} exists ({n} bytes). Here it is:\n\n{c}",
               "Yes, {f} is there, {n} bytes. It says:\n\n{c}",
               "{f} exists and is {n} bytes long. Its contents:\n\n{c}",
               "Found {f} ({n} bytes):\n\n{c}")
SAVE_KINDS = ("search_then_save", "followup_save", "list_then_write")
SIZE = re.compile(r"^size:\s+(\d+)$", re.M)


def calls(context: list[dict]) -> list[tuple[dict, str]]:
    """(call, result) for every call in a context, in order."""
    return [(m["tool_calls"][0]["function"], nxt["content"])
            for m, nxt in zip(context, context[1:], strict=False)
            if m["role"] == "assistant" and m.get("tool_calls")]


def _last_step_was(before: dict | None, tool: str) -> bool:
    return before is not None and before["expected"] is not None \
        and before["expected"]["name"] == tool


def ground(row: dict, before: dict | None) -> dict:
    """The row with a grounded reply and answer rule, or the row unchanged.
    `before` is the step before it in the same episode (None for the first)."""
    if row["expected"] is not None:
        return row
    kind = row["intent"]
    if kind in SAVE_KINDS and _last_step_was(before, "fs_write"):
        assert before is not None
        write = calls(row["context"])[-1][0]["arguments"]
        f = write["path"]
        values = before["expected"]["arguments"]["content"]["contains_all"]
        if kind == "list_then_write":
            reply = _pick(SAVED_NAMES, f).format(f=f, c=", ".join(values))
        else:
            reply = _pick(SAVED_SAYS, f).format(f=f, c=write["content"])
        return {**row, "reply": reply, "answer": {"all": [f, *values]}}
    if kind == "check_then_read" and _last_step_was(before, "fs_read"):
        history = calls(row["context"])
        stat = next(result for c, result in history if c["name"] == "fs_stat")
        size = SIZE.search(stat)
        if size is None:
            raise ValueError(f"{row['id']}: no size in the fs_stat result")
        read, text = history[-1]
        f, n = read["arguments"]["path"], size.group(1)
        reply = _pick(EXISTS_READ, f).format(f=f, n=n, c=text.rstrip("\n"))
        return {**row, "reply": reply, "answer": {"all": [f"{n} bytes", *text.splitlines()]}}
    return row


def build(rows: list[dict]) -> list[dict]:
    """Every row, in order, with its final turn grounded, in a split named <split>_g."""
    out: list[dict] = []
    prev: dict | None = None
    for r in rows:
        before = prev if prev is not None and prev["episode"] == r["episode"] else None
        g = ground(r, before)
        split = r["split"] + "_g"
        out.append({**g, "split": split, "id": split + r["id"][len(r["split"]):]})
        prev = r
    return out


def main() -> int:
    data = ROOT / "data"
    changed = {}
    for split in SPLITS:
        rows = [json.loads(x) for x in (data / f"{split}.jsonl").read_text().splitlines()]
        g = build(rows)
        changed[split + "_g"] = sum(a["reply"] != b["reply"] for a, b in zip(rows, g,
                                                                             strict=True))
        (data / f"{split}_g.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in g))
    print("final turns grounded:", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
