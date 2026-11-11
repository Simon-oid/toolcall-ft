#!/usr/bin/env python3
"""A terminal demo: the same requests to the base model and the fine-tuned
one, each reply judged by cMCP's validator. Made to be recorded.

    llama-server -hf Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q8_0 --port 8084 -ngl 99 -c 8192 -np 1 &
    llama-server -m models/ft-1.5b-v2-q8_0.gguf           --port 8083 -ngl 99 -c 8192 -np 1 &
    python scripts/demo.py                      # --pause 0 for no pauses

The requests are hand-written and in neither training nor test data.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from toolcall.backends import BackendError, LlamaCpp
from toolcall.evaluate import call_text
from toolcall.judge import judge
from toolcall.prompt import load_tools, render

MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
SCENES = [
    ("A call with arithmetic: lines 30 to 45 means offset 30, limit 16",
     "show me lines 30 to 45 of journal/week-12.md"),
    ("Two similar tools: the index's statistics, not a file's",
     "how many chunks does the document index hold?"),
    ("Small talk: no tool should be called",
     "haha nice, thanks for the help!"),
    ("An operation no tool performs: say so, do not improvise",
     "delete journal/week-11.md, it's outdated"),
    ("A request missing what the tool needs: ask, do not guess",
     "write that into the file"),
]
BOLD, DIM, GREEN, RED, OFF = "\033[1m", "\033[2m", "\033[32m", "\033[31m", "\033[0m"


def show(label: str, reply: str) -> None:
    text = call_text(reply)
    if text is None:
        print(f"  {label:11s} {DIM}no call:{OFF} {' '.join(reply.split())[:110]}")
        return
    v = judge([text])[0]
    ok = v["json"] and v["schema"]
    if v["error"]:
        reason = json.dumps(v["error"])              # the validator's own words
    else:
        reason = "unknown tool" if v["json"] else "not a call object"
    why = "" if ok else f"  {RED}{reason}{OFF}"
    mark = f"{GREEN}valid{OFF}" if ok else f"{RED}invalid{OFF}"
    print(f"  {label:11s} {' '.join(text.split())}  [{mark}]{why}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base-url", default="http://127.0.0.1:8084")
    ap.add_argument("--ft-url", default="http://127.0.0.1:8083")
    ap.add_argument("--pause", type=float, default=2.0)
    args = ap.parse_args()
    tools = load_tools()
    base, tuned = LlamaCpp(args.base_url), LlamaCpp(args.ft_url)
    try:
        base.props(), tuned.props()                  # fail early if a server is down
    except BackendError as e:
        print(f"{e}\nStart both servers first: see the top of this file.", file=sys.stderr)
        return 1
    print(f"{BOLD}Six MCP tools, one request each. Same prompt, greedy decoding.{OFF}")
    print(f"{DIM}base: Qwen2.5-1.5B    fine-tuned: the same model + LoRA{OFF}")
    for title, request in SCENES:
        time.sleep(args.pause)
        print(f"\n{BOLD}# {title}{OFF}\n  user        {request}")
        prompt = render(request, MODEL, tools)
        time.sleep(args.pause / 2)
        show("base", base.generate([prompt])[0])
        show("fine-tuned", tuned.generate([prompt])[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
