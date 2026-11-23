"""Sampled mistakes on call turns, for DPO's call pairs (prefs.py --calls-from).

    python -m toolcall.sample --name sampled-dpo-v5 --model Qwen/Qwen2.5-1.5B-Instruct

Greedy, a DPO model is almost always right on its own training cases: it
remembers them, and its habit of replying instead of calling shows only on
new ones. Sampled at temperature 1, the same habit shows on training cases
too. For every call turn of --splits this asks the served model --n times
(seeds 0..n-1) and keeps the first reply that is not the right call, scored
by the same scorer and judge as evaluate.py. A turn with no wrong sample
keeps its first sample, which prefs.py then skips. Writes
results/<name>/results.jsonl in evaluate's row format.
"""

from __future__ import annotations

import argparse
import json
import sys

from .backends import LlamaCpp
from .data import ROOT, load
from .evaluate import score_cases
from .prefs import GARBAGE
from .prompt import load_tools, render_case


def first_wrong(samples: list[dict]) -> dict:
    """The first sample that is not the right call (and not server garbage),
    else the first sample."""
    for s in samples:
        if not s["score"]["levels"]["args"] and not GARBAGE.match(s["reply"]):
            return s
    return samples[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", required=True, help="tokenizer whose chat template renders")
    ap.add_argument("--splits", default="train,mt_train")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--url", default="http://127.0.0.1:8083")
    args = ap.parse_args()
    if args.temperature <= 0:
        raise SystemExit("--temperature must be > 0: greedy gives one answer per turn")
    tools = load_tools()
    cases = [r for s in args.splits.split(",") for r in load(s) if r["expected"] is not None]
    prompts = [render_case(c, args.model, tools) for c in cases]
    per_seed = []
    for seed in range(args.n):
        backend = LlamaCpp(args.url, temperature=args.temperature, seed=seed)
        per_seed.append(score_cases(cases, backend.generate(prompts)))
        wrong = sum(not r["score"]["levels"]["args"] for r in per_seed[-1])
        print(f"seed {seed}: {wrong} of {len(cases)} call turns wrong", flush=True)
    rows = [first_wrong(list(s)) for s in zip(*per_seed, strict=True)]
    out = ROOT / "results" / args.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                               for r in rows))
    print(f"{sum(not r['score']['levels']['args'] for r in rows)} of {len(rows)} call turns "
          f"have a wrong sample -> {out / 'results.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
