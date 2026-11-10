#!/usr/bin/env python3
"""results/*/results.jsonl -> results/summary.md: one row per run and split.

    python scripts/summarize.py [RUN ...]       # default: every run, in a fixed order
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from toolcall.evaluate import REPORT_SPLITS, rates

ROOT = Path(__file__).resolve().parent.parent
COLS = ("call made", "L2 schema", "L3 tool", "L4 args", "abstain", "decision")


def cell(m: tuple, ci: bool) -> str:
    return f"{m[0]:.2f} [{m[1]:.2f}, {m[2]:.2f}]" if ci else f"{m[0]:.2f}"


def main() -> int:
    runs = sys.argv[1:] or sorted(p.name for p in (ROOT / "results").iterdir()
                                  if (p / "results.jsonl").exists())
    lines = ["# Results", "",
             "Rates over the test cases; [95% bootstrap interval] on the metrics that decide.",
             "levels and *call made* over cases that need a call, *abstain* over those that",
             "need none, *decision* (called iff it should) over all.", ""]
    for split in REPORT_SPLITS:
        lines += [f"## {split}", "", "| run | " + " | ".join(COLS) + " |",
                  "|---|" + "---|" * len(COLS)]
        for run in runs:
            rows = [json.loads(x) for x in (ROOT / "results" / run / "results.jsonl")
                    .read_text().splitlines()]
            rows = [r for r in rows if r["split"] == split]
            if not rows:
                continue
            m = rates(rows)
            lines.append(f"| {run} | " + " | ".join(
                cell(m[c], c in ("L4 args", "abstain")) for c in COLS) + " |")
        lines.append("")
    (ROOT / "results" / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
