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

Only final turns change in grounded.py, so only they give pairs of that
kind. DPO on those alone moved the call turns before them (it learned to
reply instead of calling), so `--calls-from` adds call pairs:

  chosen    the right call, written as training writes it
  rejected  what a model replied on that call turn when it got it wrong:
            the run of round-1 DPO on train,mt_train, whose mistakes are
            exactly the replies that should have been calls
"""

from __future__ import annotations

import argparse
import json
import re

from .data import ROOT
from .score import answer_ok
from .train import completion

GARBAGE = re.compile(r"^(.)\1{15}")     # llama.cpp on ROCm sometimes returns "!!!!..."


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


def call_pairs(rows: list[dict], onpolicy: dict[str, dict]) -> list[dict]:
    """One pair per call turn the model got wrong (not right at level 4):
    chosen = the right call, rejected = what the model wrote there."""
    out = []
    for r in rows:
        if r["expected"] is None:
            continue
        said = onpolicy.get(r["id"])
        if said is None or said["score"]["levels"]["args"] or GARBAGE.match(said["reply"]):
            continue
        pair = {"id": r["id"], "intent": r["intent"], "kind": "call",
                "chosen": completion(r, {}), "rejected": said["reply"]}
        pair |= {"context": r["context"]} if "context" in r else {"request": r["request"]}
        out.append(pair)
    return out


def load_rows(path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", default="onpolicy-v5")
    ap.add_argument("--split", default="mt_train_g")
    ap.add_argument("--out", default="data/prefs_v5.jsonl")
    ap.add_argument("--calls-from", help="a run on train,mt_train whose wrong calls add pairs")
    args = ap.parse_args()
    grounded = load_rows(ROOT / "data" / f"{args.split}.jsonl")
    results = load_rows(ROOT / "results" / args.run / "results.jsonl")
    ps = pairs(grounded, {r["id"]: r for r in results})
    n_reply = len(ps)
    if args.calls_from:
        said = {r["id"]: r for r in load_rows(ROOT / "results" / args.calls_from / "results.jsonl")}
        for split in ("train", "mt_train"):
            ps += call_pairs(load_rows(ROOT / "data" / f"{split}.jsonl"), said)
    (ROOT / args.out).write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in ps))
    print(f"{len(ps)} pairs ({n_reply} final replies, {len(ps) - n_reply} calls) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
