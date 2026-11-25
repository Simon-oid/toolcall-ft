#!/usr/bin/env python3
"""Paired comparison of two model families, pooled over their seeds.

    python scripts/pooled.py ft-1.5b-v5 ft-1.5b-v6 [PREFIX:SPLIT ...]

For each set, each seed suffix ("", -s1, -s2) pairs run <prefix><a><sfx>-free
with <prefix><b><sfx>-free and counts the units b fixed and broke: calls
(right at level 4), abstentions, grounded final replies and, on episode
sets, whole episodes. The pooled counts sum the seeds; the p values are
exact McNemar per seed (pooling the seeds in one test would treat three
runs of the same cases as independent cases).
"""

from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path

from toolcall.evaluate import step_right

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ("", "-s1", "-s2")
SETS = ("hand8-:test_hand8", "mt7-:mt7_test_ood", "hand7-:test_hand7",
        "hand6-:test_hand6", "mtg-:mt_test_ood_g", "mt-:mt_test_ood",
        ":test_ood", ":test_id")


def load(run: str, split: str) -> list[dict]:
    path = ROOT / "results" / run / "results.jsonl"
    return [r for r in map(json.loads, path.read_text().splitlines()) if r["split"] == split]


def units(rows: list[dict], metric: str) -> dict[str, bool]:
    if metric == "call right":
        return {r["id"]: bool(r["score"]["levels"]["args"]) for r in rows if r["expected"]}
    if metric == "abstain":
        return {r["id"]: bool(r["score"]["abstained_ok"]) for r in rows if not r["expected"]}
    if metric == "grounded":
        return {r["id"]: bool(r["score"]["answered"]) for r in rows
                if r["score"].get("answered") is not None}
    eps: dict[str, list[dict]] = {}
    for r in rows:
        if "episode" in r:
            eps.setdefault(r["episode"], []).append(r)
    return {e: all(step_right(r) for r in steps) for e, steps in eps.items()}


def mcnemar(fixed: int, broken: int) -> float:
    n = fixed + broken
    tail = sum(comb(n, i) for i in range(min(fixed, broken) + 1))
    return min(1.0, 2 * tail / 2 ** n) if n else 1.0


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    a, b, sets = sys.argv[1], sys.argv[2], sys.argv[3:] or SETS
    for s in sets:
        prefix, split = s.split(":")
        print(f"## {prefix}{split}: {a} -> {b}\n")
        print("| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |")
        print("|---|---|---|---|---|")
        for metric in ("call right", "abstain", "grounded", "episode"):
            per = []
            for sfx in SEEDS:
                x = units(load(f"{prefix}{a}{sfx}-free", split), metric)
                y = units(load(f"{prefix}{b}{sfx}-free", split), metric)
                if x.keys() != y.keys():
                    raise SystemExit(f"{prefix}{a}{sfx} and {prefix}{b}{sfx}: different cases")
                per.append((sum(y[k] and not x[k] for k in x), sum(x[k] and not y[k] for k in x),
                            len(x)))
            if per[0][2] == 0:
                continue
            seeds = ", ".join(f"{f}/{k} ({mcnemar(f, k):.2g})" for f, k, _ in per)
            print(f"| {metric} | {per[0][2]} | {sum(p[0] for p in per)} | "
                  f"{sum(p[1] for p in per)} | {seeds} |")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
