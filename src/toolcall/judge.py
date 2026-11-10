"""Runs judge/judge (C, linked against cMCP) over a batch of call texts.

One process per batch, not per call: the judge reads the tool schemas
once and then one call per line, so a 500-case run is one exec."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JUDGE = Path(os.environ.get("TOOLCALL_JUDGE", ROOT / "judge" / "judge"))
TOOLS = ROOT / "data" / "tools.json"


class JudgeError(RuntimeError):
    pass


def judge(texts: list[str], tools: Path = TOOLS, binary: Path = JUDGE) -> list[dict]:
    """One verdict per text, in order."""
    if not binary.exists():
        raise JudgeError(f"{binary} not built: make -C judge")
    stdin = "".join(json.dumps(t) + "\n" for t in texts)
    proc = subprocess.run([str(binary), str(tools)], input=stdin, capture_output=True,
                          text=True, timeout=60)
    if proc.returncode != 0:
        raise JudgeError(f"judge exited {proc.returncode}: {proc.stderr.strip()}")
    verdicts = [json.loads(line) for line in proc.stdout.splitlines()]
    if len(verdicts) != len(texts):
        raise JudgeError(f"judge returned {len(verdicts)} verdicts for {len(texts)} calls")
    return verdicts
