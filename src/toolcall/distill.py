"""Training replies for the no_tool cases, written by the base model itself.

A chit-chat request is answered by the base model *without tools in the
prompt*, so the reply is in its own voice. Training on it teaches when not
to call a tool, without teaching a new way of talking (fixed or hand-written
replies would). Greedy, one request at a time: reproducible.

    python -m toolcall.distill --model Qwen/Qwen2.5-1.5B-Instruct   # llama.cpp at --url
    -> data/distilled_no_tool.jsonl  {"request": ..., "reply": ...}
"""

from __future__ import annotations

import argparse
import asyncio
import json

import httpx

from .backends import STOP
from .data import ROOT, load
from .prompt import tokenizer

OUT = ROOT / "data" / "distilled_no_tool.jsonl"
PLAIN_SYSTEM = "You are a helpful assistant."
MAX_TOKENS = 600


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True)
    ap.add_argument("--url", default="http://127.0.0.1:8083")
    args = ap.parse_args()
    requests = sorted({r["request"] for split in ("train", "val") for r in load(split)
                       if r["intent"] == "no_tool"})
    tok = tokenizer(args.model)
    prompts = [tok.apply_chat_template([{"role": "system", "content": PLAIN_SYSTEM},
                                        {"role": "user", "content": q}],
                                       add_generation_prompt=True, tokenize=False)
               for q in requests]
    out = asyncio.run(_generate(args.url, prompts))
    kept = [(q, text) for q, (text, stopped) in zip(requests, out, strict=True) if stopped]
    # A reply cut by the token limit would teach stopping mid-sentence: dropped.
    OUT.write_text("".join(json.dumps({"request": q, "reply": t.strip()}, ensure_ascii=False)
                           + "\n" for q, t in kept))
    print(f"{len(kept)} of {len(requests)} replies ended on their own -> {OUT}")
    return 0


async def _generate(url: str, prompts: list[str]) -> list[tuple[str, bool]]:
    """(text, whether the model stopped by itself rather than at the limit)."""
    out = []
    async with httpx.AsyncClient(timeout=300) as client:
        for p in prompts:
            r = await client.post(f"{url}/completion", json={
                "prompt": p, "n_predict": MAX_TOKENS, "temperature": 0.0, "top_k": 1,
                "seed": 0, "stop": STOP})
            r.raise_for_status()
            d = r.json()
            out.append((d["content"], not d.get("truncated") and d.get("stop_type") != "limit"))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
