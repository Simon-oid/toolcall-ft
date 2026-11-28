"""Closed-loop evaluation: episodes where the model sees its own turns.

    python -m toolcall.rollout --name cl-ft-v7 --model Qwen/Qwen2.5-1.5B-Instruct \\
        --splits test_hand9,mt8_test_ood --tf hand9-ft-v7-free,mt8-ft-v7-free

evaluate.py scores each turn of an episode with the right history before
it (teacher forcing). Here the history is the model's own: its calls and
its replies go into the conversation, and the episode goes on from there.

  * A right turn gets what the episode's transcript gives next: the tool's
    result after a call, the user's next message after a reply.
  * A wrong call is answered as the servers would answer it, where that
    answer is known, and the model gets another try at the same turn:
      - a tool no server has: the server's error ("Unknown tool ...");
      - arguments the schema rejects: the server's error, built from the
        judge's verdict (cMCP's own validator, same message format);
      - a reply that is not JSON: the host cannot dispatch it, and says so;
      - an fs_* call on a generated episode: the real filesystem-mcp,
        run on the episode's own file tree, answers it.
    At most MAX_DETOURS such answers per episode.
  * Otherwise the episode stops and fails: a reply where a call was due
    (nothing would come next), a final reply without the fact, or a wrong
    call whose answer is unknown (crag_* calls, fs_* calls on hand-written
    episodes, which have no file tree).

An episode is "right" when every turn was right at the first try, as with
teacher forcing but on the model's own history; "recovered" when it got
there after at least one detour. The route is strict, as in evaluate.py:
a detour that reaches the goal another way still has to come back to the
turn the episode expects.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .backends import LlamaCpp
from .data import ROOT, SYSTEM, load
from .evaluate import call_text, git_rev, score_cases, step_right
from .prompt import load_tools, render_messages

MAX_DETOURS = 3
CMCP = Path(os.environ.get("TOOLCALL_CMCP", ROOT.parent / "cMCP"))
INSPECT = CMCP / "tools" / "cmcp-inspect" / "cmcp-inspect"
FS_MCP = CMCP / "tools" / "filesystem-mcp" / "filesystem-mcp"
NOT_JSON = "error: the tool call is not valid JSON, so it was not run"


def fs_server(name: str, arguments: dict, root: Path) -> str:
    """One call to the real filesystem-mcp over `root`, as the model sees it."""
    out = subprocess.run([str(INSPECT), "-c", name, "-a", json.dumps(arguments), "--",
                          str(FS_MCP), "--root", str(root)],
                         capture_output=True, text=True, timeout=30, check=False)
    if out.returncode != 0:
        raise RuntimeError(f"filesystem-mcp: {out.stderr.strip()}")
    text = out.stdout.split(f"Calling {name}:\n", 1)[1].rstrip("\n")
    if text.startswith("[tool-level error]\n"):
        return "error: " + text.removeprefix("[tool-level error]\n")
    return text


def materialize(files: dict, root: Path) -> None:
    """Write an episode's file tree to disk, mtimes included."""
    for path, f in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f["content"])
        target.chmod(0o644)
        t = dt.datetime.strptime(f["modified"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC)
        os.utime(target, (t.timestamp(), t.timestamp()))


def server_answer(text: str, verdict: dict, root: Path | None) -> str | None:
    """What the servers answer to a wrong call, or None when it is not known."""
    if not verdict["json"]:
        return NOT_JSON
    if not verdict["known"]:
        return "error: Unknown tool " + json.dumps({"name": verdict["name"]},
                                                   separators=(",", ":"))
    if not verdict["schema"]:
        e = verdict["error"] or {}
        return (f"error: Invalid arguments for tool '{verdict['name']}': {e.get('message')} "
                f"(path: {e.get('path')}, keyword: {e.get('keyword')})")
    if root is not None and verdict["name"].startswith("fs_"):
        return fs_server(verdict["name"], json.loads(text)["arguments"], root)
    return None


def assistant_turn(reply: str, text: str | None) -> dict:
    """The model's turn as a message: its call, or its words."""
    if text is not None:
        try:
            c = json.loads(text)
            return {"role": "assistant", "content": "",
                    "tool_calls": [{"type": "function", "function": {
                        "name": c["name"], "arguments": c.get("arguments", {})}}]}
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            pass
    return {"role": "assistant", "content": reply}


@dataclass
class Run:
    """One episode, played turn by turn on the model's own history."""
    steps: list[dict]
    root: Path | None = None
    k: int = 0
    history: list[dict] = field(default_factory=list)
    detours: int = 0
    outcome: str | None = None
    reason: str = ""
    turns: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.history = list(self.steps[0]["context"])

    def messages(self) -> list[dict]:
        return [{"role": "system", "content": SYSTEM}, *self.history]

    def _next_gold(self) -> list[dict]:
        """What the transcript gives after turn k: the tool's result, or the user."""
        here, nxt = self.steps[self.k]["context"], self.steps[self.k + 1]["context"]
        return nxt[len(here) + 1:]

    def feed(self, reply: str, row: dict) -> None:
        text = call_text(reply)
        ok = step_right(row)
        self.turns.append({"step": self.k, "reply": reply, "right": ok})
        if ok:
            self._advance(reply, text, row)
        elif text is None:
            self._stop("replied where a call was due" if row["expected"] is not None
                       else "final reply without the fact")
        else:
            self._detour(reply, text, row)

    def _advance(self, reply: str, text: str | None, row: dict) -> None:
        if text is not None and self.root is not None and row["verdict"]["name"] == "fs_write":
            fs_server("fs_write", json.loads(text)["arguments"], self.root)  # later reads see it
        if self.k == len(self.steps) - 1:
            self.outcome = "recovered" if self.detours else "right"
            return
        self.history += [assistant_turn(reply, text), *self._next_gold()]
        self.k += 1

    def _detour(self, reply: str, text: str, row: dict) -> None:
        if self.detours == MAX_DETOURS:
            self._stop(f"still wrong after {MAX_DETOURS} detours")
            return
        answer = server_answer(text, row["verdict"], self.root)
        if answer is None:
            self._stop(f"wrong {row['verdict']['name']} call, answer unknown")
            return
        name = row["verdict"]["name"] if row["verdict"]["known"] else "unknown"
        self.history += [assistant_turn(reply, text),
                         {"role": "tool", "name": name, "content": answer}]
        self.turns[-1]["server"] = answer
        self.detours += 1

    def _stop(self, reason: str) -> None:
        self.outcome, self.reason = "failed", reason


def episodes(rows: list[dict]) -> list[list[dict]]:
    by: dict[tuple, list[dict]] = {}
    for r in rows:
        by.setdefault((r["split"], r["episode"]), []).append(r)
    return [sorted(v, key=lambda r: r["step"]) for v in by.values()]


def play(steps_list: list[list[dict]], backend, model: str, tools: list[dict]) -> list[Run]:
    """All episodes in lockstep: one batch of prompts per round."""
    with tempfile.TemporaryDirectory() as tmp:
        runs = []
        for n, steps in enumerate(steps_list):
            root = None
            if steps[0].get("files"):
                root = Path(tmp) / str(n)
                materialize(steps[0]["files"], root)
            runs.append(Run(steps, root))
        while active := [r for r in runs if r.outcome is None]:
            prompts = [render_messages(r.messages(), model, tools) for r in active]
            replies = backend.generate(prompts)
            rows = score_cases([r.steps[r.k] for r in active], replies)
            for run, reply, row in zip(active, replies, rows, strict=True):
                run.feed(reply, row)
    return runs


def teacher_forced(names: list[str]) -> dict[tuple, bool]:
    """Episode right under teacher forcing, from evaluate.py's results."""
    out: dict[tuple, bool] = {}
    for name in names:
        for line in (ROOT / "results" / name / "results.jsonl").read_text().splitlines():
            r = json.loads(line)
            key = (r["split"], r["episode"])
            out[key] = out.get(key, True) and step_right(r)
    return out


def split_line(split: str, runs: list[Run], tf: dict[tuple, bool]) -> str:
    keys = [(split, r.steps[0]["episode"]) for r in runs]
    closed = [r.outcome in ("right", "recovered") for r in runs]
    forced = [tf.get(k) for k in keys]
    n = len(runs)
    tf_cell = f"{sum(bool(x) for x in forced) / n:.2f}" if None not in forced else "–"
    lost = sum(1 for a, b in zip(forced, closed, strict=True) if a and not b)
    won = sum(1 for a, b in zip(forced, closed, strict=True) if a is False and b)
    return (f"| {split} | {n} | {tf_cell} | {sum(r.outcome == 'right' for r in runs) / n:.2f} | "
            f"{sum(r.outcome == 'recovered' for r in runs) / n:.2f} | {lost} | {won} |")


def report(runs: list[Run], tf: dict[tuple, bool], meta: dict) -> str:
    lines = [f"# {meta['name']}", "", " · ".join(f"{k}: {v}" for k, v in meta.items()
                                                   if k != "name"), "",
             "| split | episodes | teacher-forced right | right, own history | "
             "right after a detour | TF right, closed loop not | closed loop right, TF not |",
             "|---|---|---|---|---|---|---|"]
    reasons = []
    for split in dict.fromkeys(r.steps[0]["split"] for r in runs):
        rs = [r for r in runs if r.steps[0]["split"] == split]
        lines.append(split_line(split, rs, tf))
        c = Counter(r.reason for r in rs if r.outcome == "failed")
        reasons.append(f"- {split}: " + ("; ".join(f"{why} {n}" for why, n in c.most_common())
                                         or "none"))
    return "\n".join([*lines, "", "Why the failed episodes stopped:", "", *reasons]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--model", required=True, help="HF tokenizer for the chat template")
    ap.add_argument("--url", default="http://127.0.0.1:8083")
    ap.add_argument("--splits", required=True)
    ap.add_argument("--tf", default="", help="evaluate.py result names to compare with")
    ap.add_argument("--limit", type=int, help="first N episodes per split (smoke runs)")
    args = ap.parse_args()
    if not (INSPECT.exists() and FS_MCP.exists()):
        print(f"needs cMCP's cmcp-inspect and filesystem-mcp built under {CMCP}",
              file=sys.stderr)
        return 2
    steps_list = [e for s in args.splits.split(",") for e in episodes(load(s))[:args.limit]]
    backend = LlamaCpp(args.url)
    props = backend.props()
    runs = play(steps_list, backend, args.model, load_tools())
    tf = teacher_forced([n for n in args.tf.split(",") if n])
    meta = {"name": args.name, "model": args.model,
            "gguf": Path(props.get("model_path", "?")).name, "decoding": "free, greedy",
            "llama.cpp": props.get("build_info", "?"), "commit": git_rev(),
            "date": dt.date.today().isoformat(), "episodes": len(runs),
            "max detours": MAX_DETOURS}
    out = ROOT / "results" / args.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "rollout.jsonl").write_text("".join(json.dumps({
        "split": r.steps[0]["split"], "episode": r.steps[0]["episode"],
        "intent": r.steps[0]["intent"], "outcome": r.outcome, "reason": r.reason,
        "detours": r.detours, "turns": r.turns}) + "\n" for r in runs))
    (out / "report.md").write_text(report(runs, tf, meta))
    print((out / "report.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
