import json
import os
import random
import subprocess
from pathlib import Path

import pytest

from toolcall.data import POOLS, build
from toolcall.judge import judge
from toolcall.score import parse_expected, score

ROWS = build()
CMCP = Path(os.environ.get("TOOLCALL_CMCP", Path(__file__).resolve().parents[2] / "cMCP"))
INSPECT = CMCP / "tools" / "cmcp-inspect" / "cmcp-inspect"
FS_MCP = CMCP / "tools" / "filesystem-mcp" / "filesystem-mcp"


def by_split(split):
    return [r for r in ROWS if r["split"] == split]


def test_build_is_deterministic():
    assert build() == ROWS


def test_every_training_call_is_valid_and_right():
    calls = [r for r in ROWS if r["expected"] is not None]
    verdicts = judge([json.dumps(r["call"]) for r in calls])
    for r, v in zip(calls, verdicts, strict=True):
        s = score(parse_expected(r["expected"]), json.dumps(r["call"]), v)
        assert all(s.levels.values()), (r["request"], r["call"], v)


def test_no_call_cases_have_no_call():
    for r in ROWS:
        if r["intent"] in ("no_tool", "unsupported", "ambiguous"):
            assert r["expected"] is None and "call" not in r
        if r["intent"] in ("unsupported", "ambiguous"):
            assert r["reply"]


def test_held_out_families_appear_only_in_test_ood():
    for r in ROWS:
        assert (r["family"] >= 6) == (r["split"] == "test_ood"), r


def test_test_requests_never_appear_in_training():
    seen = {r["request"] for r in ROWS if r["split"] in ("train", "val")}
    for r in by_split("test_id") + by_split("test_ood"):
        if r["intent"] != "crag_stats":     # a fixed phrase per family, no slots
            assert r["request"] not in seen, r["request"]


def test_test_slot_values_are_unseen_in_training():
    train_text = " ".join(r["request"] for r in by_split("train") + by_split("val"))
    for name in POOLS["test"]["names"]:
        assert f"/{name}." not in train_text
    for phrase, _ in POOLS["test"]["topics"]:
        assert phrase not in train_text


def test_every_intent_is_in_every_split():
    intents = {r["intent"] for r in ROWS}
    for split in ("train", "val", "test_id", "test_ood"):
        assert {r["intent"] for r in by_split(split)} == intents, split


@pytest.mark.skipif(not (INSPECT.exists() and FS_MCP.exists()), reason="cMCP not built")
def test_fs_calls_run_on_the_real_server(tmp_path):
    rng = random.Random(0)
    fs = [r for r in ROWS if r["expected"] and r["expected"]["name"].startswith("fs_")]
    for r in rng.sample(fs, 40):
        for p in [r["call"]["arguments"].get("path", "")]:
            target = tmp_path / p
            if r["call"]["name"] == "fs_list":
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                if r["call"]["name"] != "fs_write":
                    target.write_text("".join(f"line {i}\n" for i in range(1, 201)))
        out = subprocess.run([str(INSPECT), "-c", r["call"]["name"], "-a",
                              json.dumps(r["call"]["arguments"]), "--", str(FS_MCP),
                              "--root", str(tmp_path)], capture_output=True, text=True, timeout=10)
        assert out.returncode == 0 and "tool-level error" not in out.stdout, (r["call"], out.stdout)


def test_evaluation_splits_never_repeat_a_request():
    # Repeats are not independent cases: they would narrow the bootstrap intervals.
    for split in ("val", "test_id", "test_ood"):
        reqs = [r["request"] for r in by_split(split)]
        assert len(reqs) == len(set(reqs)), split


def test_framings_never_touch_written_content():
    for r in ROWS:
        if r["intent"] == "fs_write":
            assert r["call"]["arguments"]["content"] in r["request"]


HAND = [json.loads(x) for x in (Path(__file__).resolve().parents[1] / "data" / "test_hand.jsonl")
        .read_text().splitlines()]


def test_hand_written_labels_are_valid_calls():
    # A call satisfying each label: the first alternative, the label's words as the query.
    calls = []
    for r in HAND:
        if r["expected"] is None:
            continue
        args = {}
        for k, rule in r["expected"]["arguments"].items():
            if k in r["expected"].get("optional", []):
                continue
            if isinstance(rule, dict) and "any_of" in rule:
                args[k] = rule["any_of"][0]
            elif isinstance(rule, dict) and "contains_all" in rule:
                args[k] = " ".join(rule["contains_all"])
            else:
                args[k] = rule
        calls.append((r, json.dumps({"name": r["expected"]["name"], "arguments": args})))
    for (r, c), v in zip(calls, judge([c for _, c in calls]), strict=True):
        assert all(score(parse_expected(r["expected"]), c, v).levels.values()), (r["request"], v)


def test_hand_written_requests_are_not_in_training():
    seen = {r["request"] for r in ROWS}
    assert not [r["request"] for r in HAND if r["request"] in seen]
