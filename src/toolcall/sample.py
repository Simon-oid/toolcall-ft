"""Sampled mistakes on call turns, for DPO's call pairs (prefs.py --calls-from),
or with --abstain on the turns that need no call (prefs.py --abstain-from).

    python -m toolcall.sample --name sampled-dpo-v5 --model Qwen/Qwen2.5-1.5B-Instruct
    python -m toolcall.sample --abstain --name sampled-abstain-dpo2-1.5b-v5 --model ...

Greedy, a DPO model is almost always right on its own training cases: it
remembers them, and its habit of replying instead of calling shows only on
new ones. Sampled at temperature 1, the same habit shows on training cases
too. For every call turn of --splits this asks the served model --n times
(seeds 0..n-1) and keeps the first reply that is not the right call, scored
by the same scorer and judge as evaluate.py. A turn with no wrong sample
keeps its first sample, which prefs.py then skips. With --abstain the turns
are those that need no call and are not a final reply after a tool result
(single requests, and episode turns where the user spoke last), and a
mistake is a reply that does not abstain. Writes results/<name>/results.jsonl
in evaluate's row format.
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


def right(row: dict) -> bool:
    """Right at level 4 on a call turn; abstained on a turn that needs no call."""
    s = row["score"]
    if s.get("abstained_ok") is not None:
        return bool(s["abstained_ok"])
    return bool(s["levels"]["args"])


def first_wrong(samples: list[dict]) -> dict:
    """The first sample that is not right (and not server garbage), else the
    first sample."""
    for s in samples:
        if not right(s) and not GARBAGE.match(s["reply"]):
            return s
    return samples[0]


def abstain_turn(row: dict) -> bool:
    """Needs no call, and is not the reply after a tool result (those are
    the final-reply pairs' turns)."""
    return row["expected"] is None and ("context" not in row
                                        or row["context"][-1]["role"] == "user")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", required=True, help="tokenizer whose chat template renders")
    ap.add_argument("--splits", default="train,mt_train")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--url", default="http://127.0.0.1:8083")
    ap.add_argument("--abstain", action="store_true", help="sample the turns that need no call")
    args = ap.parse_args()
    if args.temperature <= 0:
        raise SystemExit("--temperature must be > 0: greedy gives one answer per turn")
    tools = load_tools()
    keep = abstain_turn if args.abstain else (lambda r: r["expected"] is not None)
    cases = [r for s in args.splits.split(",") for r in load(s) if keep(r)]
    what = "no-call turns" if args.abstain else "call turns"
    prompts = [render_case(c, args.model, tools) for c in cases]
    per_seed = []
    for seed in range(args.n):
        backend = LlamaCpp(args.url, temperature=args.temperature, seed=seed)
        per_seed.append(score_cases(cases, backend.generate(prompts)))
        wrong = sum(not right(r) for r in per_seed[-1])
        print(f"seed {seed}: {wrong} of {len(cases)} {what} wrong", flush=True)
    rows = [first_wrong(list(s)) for s in zip(*per_seed, strict=True)]
    out = ROOT / "results" / args.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                               for r in rows))
    print(f"{sum(not right(r) for r in rows)} of {len(rows)} {what} "
          f"have a wrong sample -> {out / 'results.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
