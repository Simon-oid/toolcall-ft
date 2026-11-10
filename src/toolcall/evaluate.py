"""Evaluate a model on the test splits: generate, judge, score, report.

    python -m toolcall.evaluate --name base-1.5b --model Qwen/Qwen2.5-1.5B-Instruct
    python -m toolcall.evaluate --name lazy-1.5b --model ... --decoding lazy

Decoding:
  free    greedy, unconstrained (/completion on the rendered prompt)
  eager   the whole reply constrained to "a valid call, or {"name": "none"}"
  lazy    llama.cpp's tool path: the grammar applies only once the model
          starts a call, so deciding not to call stays free

The model is served by llama.cpp (see backends.py) at --url; --model names
the Hugging Face tokenizer whose chat template renders the prompt. Writes
results/<name>/results.jsonl (one line per case: request, raw reply, the
call extracted, the judge's verdict, the score) and report.md.

Rates are over the cases of a split, with percentile bootstrap 95%
intervals (10,000 resamples, fixed seed):
  call made    over cases that need a call: the model made one
  levels 1-4   over the same cases; no call counts as failing all four
  abstain      over cases that need none: the model made no call
  decision     over all cases: called when it should, abstained when not
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

from .backends import LlamaCpp, LlamaCppChat
from .data import ROOT, load
from .judge import judge
from .prompt import call_or_none_schema, load_tools, messages, openai_tools, render
from .score import LEVELS, extract_call, parse_expected, score

SPLITS = ("test_id", "test_ood")           # evaluated by default
REPORT_SPLITS = (*SPLITS, "test_hand")     # reported when present
DECODING = {"free": "free, greedy",
            "eager": "whole reply constrained to a valid call or {name: none} (eager)",
            "lazy": "llama.cpp tool grammar, applied once a call starts (lazy)"}
RESAMPLES = 10_000
SEED = 20261110


def bootstrap(xs: list[float], resamples: int = RESAMPLES, seed: int = SEED) -> tuple:
    if not xs:
        return (float("nan"),) * 3
    rng = random.Random(seed)
    n = len(xs)
    means = sorted(sum(rng.choices(xs, k=n)) / n for _ in range(resamples))
    return sum(xs) / n, means[int(0.025 * resamples)], means[int(0.975 * resamples) - 1]


def call_text(reply: str) -> str | None:
    """The call in a reply, None if it made none. Under constrained decoding
    the explicit no-call is {"name": "none", ...}; no tool has that name."""
    text = extract_call(reply)
    if text is not None:
        try:
            if json.loads(text).get("name") == "none":
                return None
        except (json.JSONDecodeError, AttributeError):
            pass                         # malformed: a failed call, judged as such
    return text


def score_cases(cases: list[dict], replies: list[str]) -> list[dict]:
    texts = [call_text(r) for r in replies]
    called = [t for t in texts if t is not None]
    verdicts = iter(judge(called)) if called else iter(())
    out = []
    for case, reply, text in zip(cases, replies, texts, strict=True):
        verdict = next(verdicts) if text is not None else None
        s = score(parse_expected(case["expected"]), text, verdict)
        out.append({**{k: case[k] for k in ("id", "split", "intent", "family", "request",
                                             "expected")},
                    "reply": reply, "call": text, "verdict": verdict, "score": asdict(s)})
    return out


def rates(rows: list[dict]) -> dict:
    calls = [r for r in rows if r["expected"] is not None]
    none = [r for r in rows if r["expected"] is None]
    out = {"call made": bootstrap([float(r["score"]["called"]) for r in calls])}
    out |= {f"L{i} {lvl}": bootstrap([float(r["score"]["levels"][lvl]) for r in calls])
            for i, lvl in enumerate(LEVELS, 1)}
    out["abstain"] = bootstrap([float(r["score"]["abstained_ok"]) for r in none])
    out["decision"] = bootstrap([float(r["score"]["called"] == (r["expected"] is not None))
                                 for r in rows])
    out["n"] = (len(calls), len(none))
    return out


def fmt(m: tuple) -> str:
    return f"{m[0]:.3f} [{m[1]:.3f}, {m[2]:.3f}]"


def per_intent(rows: list[dict]) -> list[str]:
    lines = ["| intent | n | right (L4, or abstained) |", "|---|---|---|"]
    for intent in sorted({r["intent"] for r in rows}):
        rs = [r for r in rows if r["intent"] == intent]
        ok = [float(r["score"]["levels"]["args"] if r["expected"] is not None
                    else r["score"]["abstained_ok"]) for r in rs]
        lines.append(f"| {intent} | {len(rs)} | {sum(ok) / len(ok):.2f} |")
    return lines


def failures(rows: list[dict], limit: int = 12) -> list[str]:
    out = []
    for r in rows:
        s = r["score"]
        if s["levels"] is not None and not s["levels"]["args"]:
            first = next(lvl for lvl in LEVELS if not s["levels"][lvl])
            why = (r["verdict"] or {}).get("error") or ("no call" if r["call"] is None else "")
            out.append(f"- `{r['id']}` {r['intent']}: fails {first} {why or ''} | "
                       f"{r['request']!r} -> {(r['call'] or r['reply'])[:140]!r}")
        elif s["abstained_ok"] is False:
            out.append(f"- `{r['id']}` {r['intent']}: called {r['call'][:120]!r} | "
                       f"{r['request']!r}")
        if len(out) >= limit:
            break
    return out


def report(rows: list[dict], meta: dict) -> str:
    lines = [f"# {meta['name']}", "", " · ".join(f"{k}: {v}" for k, v in meta.items()
                                                   if k != "name"), ""]
    for split in REPORT_SPLITS:
        rs = [r for r in rows if r["split"] == split]
        if not rs:
            continue
        m = rates(rs)
        lines += [f"## {split} ({m['n'][0]} need a call, {m['n'][1]} need none)", "",
                  "| metric | rate [95% CI] |", "|---|---|",
                  *[f"| {k} | {fmt(v)} |" for k, v in m.items() if k != "n"], "",
                  *per_intent(rs), "", "Failures (first 12):", "", *failures(rs), ""]
    return "\n".join(lines)


def git_rev() -> str:
    return subprocess.run(["git", "describe", "--always", "--dirty"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", required=True, help="HF tokenizer for the chat template")
    ap.add_argument("--url", default="http://127.0.0.1:8083")
    ap.add_argument("--decoding", choices=("free", "eager", "lazy"), default="free")
    ap.add_argument("--splits", default=",".join(SPLITS))
    ap.add_argument("--limit", type=int, help="first N cases per split (smoke runs)")
    args = ap.parse_args()
    tools = load_tools()
    cases = [c for s in args.splits.split(",") for c in load(s)[:args.limit]]
    if args.decoding == "lazy":
        backend = LlamaCppChat(args.url, tools=openai_tools(tools))
        props = backend.props()
        replies = backend.generate([messages(c["request"]) for c in cases])
    else:
        backend = LlamaCpp(args.url, json_schema=call_or_none_schema(tools)
                           if args.decoding == "eager" else None)
        props = backend.props()
        replies = backend.generate([render(c["request"], args.model, tools) for c in cases])
    rows = score_cases(cases, replies)
    meta = {"name": args.name, "model": args.model,
            "gguf": Path(props.get("model_path", "?")).name,
            "decoding": DECODING[args.decoding],
            "llama.cpp": props.get("build_info", "?"), "commit": git_rev(),
            "date": dt.date.today().isoformat(), "cases": len(rows)}
    out = ROOT / "results" / args.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out / "report.md").write_text(report(rows, meta))
    print((out / "report.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
