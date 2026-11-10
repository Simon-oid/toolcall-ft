#!/usr/bin/env python3
"""Paired comparison of two runs over the same test cases.

    python scripts/compare.py BASE NEW            # e.g. 1.5b-free ft-1.5b-free

For each split and metric: the mean difference NEW - BASE with a paired
bootstrap 95% interval (cases resampled together, so each is compared
with itself), and the cases that changed in each direction, with an exact
two-sided McNemar p-value. A fine-tuning that fixes 40 cases and breaks 15
is not the same as one that fixes 25 and breaks none, even at equal means.

  right    L4 over cases that need a call
  abstain  over cases that need none
  decision called iff it should, over all
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

from toolcall.evaluate import REPORT_SPLITS

ROOT = Path(__file__).resolve().parent.parent
RESAMPLES = 10_000
SEED = 20261110


def outcome(r: dict, metric: str) -> float | None:
    s = r["score"]
    if metric == "right":
        return float(s["levels"]["args"]) if r["expected"] is not None else None
    if metric == "abstain":
        return float(s["abstained_ok"]) if r["expected"] is None else None
    return float(s["called"] == (r["expected"] is not None))


def mcnemar(fixed: int, broken: int) -> float:
    n = fixed + broken
    if n == 0:
        return 1.0
    k = min(fixed, broken)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def paired(base: dict, new: dict, ids: list[str], metric: str):
    pairs = [(outcome(base[i], metric), outcome(new[i], metric)) for i in ids]
    pairs = [(b, n) for b, n in pairs if b is not None]
    diffs = [n - b for b, n in pairs]
    rng = random.Random(SEED)
    means = sorted(sum(rng.choices(diffs, k=len(diffs))) / len(diffs) for _ in range(RESAMPLES))
    fixed = sum(1 for b, n in pairs if n > b)
    broken = sum(1 for b, n in pairs if n < b)
    return (len(pairs), sum(diffs) / len(diffs), means[int(0.025 * RESAMPLES)],
            means[int(0.975 * RESAMPLES) - 1], fixed, broken, mcnemar(fixed, broken))


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    runs = [{r["id"]: r for r in map(json.loads, (ROOT / "results" / n / "results.jsonl")
                                     .read_text().splitlines())} for n in sys.argv[1:]]
    base, new = runs
    if base.keys() != new.keys():
        print("the runs do not cover the same cases", file=sys.stderr)
        return 1
    print(f"# {sys.argv[2]} vs {sys.argv[1]}\n")
    for split in REPORT_SPLITS:
        ids = sorted(i for i in base if base[i]["split"] == split)
        if not ids:
            continue
        print(f"## {split}\n\n| metric | n | new - base [95% CI] | fixed | broken | McNemar p |")
        print("|---|---|---|---|---|---|")
        for metric in ("right", "abstain", "decision"):
            n, m, lo, hi, fx, br, p = paired(base, new, ids, metric)
            print(f"| {metric} | {n} | {m:+.3f} [{lo:+.3f}, {hi:+.3f}] | {fx} | {br} | {p:.2g} |")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
