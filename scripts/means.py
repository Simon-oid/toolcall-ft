#!/usr/bin/env python3
"""Per-family rates on every set, over the three seeds.

    python scripts/means.py ft-1.5b-v5 ft-1.5b-v6 dpo-1.5b-v5 ...

For each set and metric (the units of pooled.py): mean ± sample sd over the
seeds ("", -s1, -s2), then the per-seed rates in brackets.
"""

from __future__ import annotations

import statistics as st
import sys

from pooled import SEEDS, SETS, load, units


def main() -> int:
    fams = sys.argv[1:]
    if not fams:
        print(__doc__)
        return 2
    print("| set | metric | " + " | ".join(fams) + " |")
    print("|---" * (len(fams) + 2) + "|")
    for s in SETS:
        prefix, split = s.split(":")
        for m in ("call right", "abstain", "grounded", "episode"):
            cells = []
            for f in fams:
                runs = (units(load(f"{prefix}{f}{x}-free", split), m) for x in SEEDS)
                vals = [sum(u.values()) / len(u) for u in runs if u]
                cells.append(f"{st.mean(vals):.2f} ± {st.stdev(vals):.2f} "
                             f"[{' '.join(f'{v:.2f}' for v in vals)}]" if vals else "")
            if any(cells):
                print(f"| {prefix}{split} | {m} | " + " | ".join(cells) + " |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
