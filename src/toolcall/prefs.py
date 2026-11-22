"""Preference pairs for DPO, on-policy: what the model said against what it
should have said, on its own training episodes.

    python -m toolcall.prefs --run onpolicy-v5   # -> data/prefs_v5.jsonl

The run is `evaluate --splits train,mt_train` of the model DPO starts from.
On its own training data v5 makes no mistake by the old targets (3376 of
3376 steps right), so pairs built from them would be empty. The pairs come
from the grounded targets (grounded.py) instead:

  chosen    the grounded final reply ("Saved to f. It says: ...")
  rejected  what the model actually replied there, when that reply fails
            the grounded answer rule (it calls, or leaves the value out)

Only final turns change in grounded.py, so only they give pairs.
"""

from __future__ import annotations

import argparse
import json

from .data import ROOT
from .score import answer_ok


def pairs(grounded: list[dict], onpolicy: dict[str, dict]) -> list[dict]:
    """One pair per grounded final turn the model got wrong. `onpolicy` maps
    the ungrounded case id (mt_train-NNNNN) to its result row."""
    out = []
    for g in grounded:
        if g["expected"] is not None or g["answer"] is None:
            continue
        said = onpolicy.get(g["id"].replace("_g", "", 1))
        if said is None or said["reply"] == g["reply"]:
            continue
        if said["call"] is None and answer_ok(said["reply"], g["answer"]):
            continue                      # already grounded: nothing to prefer
        out.append({"id": g["id"], "intent": g["intent"], "context": g["context"],
                    "chosen": g["reply"], "rejected": said["reply"]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", default="onpolicy-v5")
    ap.add_argument("--split", default="mt_train_g")
    ap.add_argument("--out", default="data/prefs_v5.jsonl")
    args = ap.parse_args()
    grounded = [json.loads(x) for x in (ROOT / "data" / f"{args.split}.jsonl")
                .read_text().splitlines()]
    results = [json.loads(x) for x in (ROOT / "results" / args.run / "results.jsonl")
               .read_text().splitlines()]
    ps = pairs(grounded, {r["id"]: r for r in results})
    (ROOT / args.out).write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in ps))
    print(f"{len(ps)} pairs -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
