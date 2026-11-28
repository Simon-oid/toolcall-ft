import json

import pytest

from toolcall.data import load
from toolcall.evaluate import score_cases
from toolcall.rollout import (
    FS_MCP,
    INSPECT,
    MAX_DETOURS,
    NOT_JSON,
    Run,
    episodes,
    fs_server,
    materialize,
    server_answer,
)
from toolcall.score import answer_ok

SPLITS = ("test_hand6", "test_hand7", "test_hand8", "test_hand9",
          "mt_test_ood_g", "mt7_test_ood", "mt8_test_ood")
needs_cmcp = pytest.mark.skipif(not (INSPECT.exists() and FS_MCP.exists()),
                                reason="cMCP not built")


def as_call(call: dict) -> str:
    return f"<tool_call>\n{json.dumps(call)}\n</tool_call>"


def gold_reply(row: dict) -> str:
    """The transcript's turn: its call, its reply, or one built from the facts."""
    if row["expected"] is not None:
        return as_call(row["call"])
    if row.get("reply"):
        return row["reply"]
    answer = row.get("answer") or {}
    reply = " ".join([*answer.get("all", []), *answer.get("any", [])[:1]]) or "OK."
    assert answer_ok(reply, row["answer"]) if row.get("answer") else True
    return reply


def feed(run: Run, reply: str) -> None:
    run.feed(reply, score_cases([run.steps[run.k]], [reply])[0])


def first(split: str, intent: str | None = None) -> list[dict]:
    return next(e for e in episodes(load(split)) if intent in (None, e[0]["intent"]))


def test_each_step_extends_the_last_by_its_target_turn():
    for split in SPLITS:
        for steps in episodes(load(split)):
            for a, b in zip(steps, steps[1:], strict=False):
                assert b["context"][:len(a["context"])] == a["context"], a["id"]
                assert b["context"][len(a["context"])]["role"] == "assistant", a["id"]


def test_replaying_the_transcript_rebuilds_every_context_and_is_right():
    for split in SPLITS:
        for steps in episodes(load(split))[:25]:
            run = Run(steps)
            while run.outcome is None:
                assert run.history == steps[run.k]["context"], steps[run.k]["id"]
                feed(run, gold_reply(steps[run.k]))
            assert (run.outcome, run.detours) == ("right", 0), steps[0]["id"]


def test_server_errors_for_calls_no_server_would_run():
    bad = {"json": True, "name": "fs_read", "known": True, "schema": False,
           "error": {"path": "/bogus", "keyword": "additionalProperties",
                     "message": "unexpected property"}}
    assert server_answer("", bad, None) == ("error: Invalid arguments for tool 'fs_read': "
                                            "unexpected property (path: /bogus, keyword: "
                                            "additionalProperties)")
    unknown = {"json": True, "name": "bash", "known": False, "schema": False, "error": None}
    assert server_answer("", unknown, None) == 'error: Unknown tool {"name":"bash"}'
    assert server_answer("{x", {"json": False}, None) == NOT_JSON
    crag = {"json": True, "name": "crag_search", "known": True, "schema": True, "error": None}
    assert server_answer('{"name": "crag_search", "arguments": {"query": "x"}}', crag,
                         None) is None


@needs_cmcp
def test_the_schema_error_is_the_real_servers(tmp_path):
    text = fs_server("fs_read", {"path": "a.txt", "bogus": 1}, tmp_path)
    call = '{"name": "fs_read", "arguments": {"path": "a.txt", "bogus": 1}}'
    row = score_cases([{"expected": None}], [as_call(json.loads(call))])[0]
    assert server_answer(call, row["verdict"], None) == text


@needs_cmcp
def test_a_wrong_read_gets_the_servers_answer_and_the_episode_can_recover(tmp_path):
    steps = first("mt_test_ood_g", "find_then_read")
    materialize(steps[0]["files"], tmp_path)
    run = Run(steps, tmp_path)
    folder = steps[0]["call"]["arguments"]["path"]
    feed(run, as_call({"name": "fs_read", "arguments": {"path": f"{folder}/nope.txt"}}))
    assert run.history[-1] == {"role": "tool", "name": "fs_read",
                               "content": "error: no such file or directory"}
    while run.outcome is None:
        feed(run, gold_reply(steps[run.k]))
    assert (run.outcome, run.detours) == ("recovered", 1)


@needs_cmcp
def test_detours_are_capped(tmp_path):
    steps = first("mt_test_ood_g", "find_then_read")
    materialize(steps[0]["files"], tmp_path)
    run = Run(steps, tmp_path)
    for _ in range(MAX_DETOURS + 1):
        feed(run, as_call({"name": "fs_read", "arguments": {"path": "nope.txt"}}))
    assert run.outcome == "failed" and run.detours == MAX_DETOURS


def test_an_episode_stops_where_nothing_would_come_next():
    steps = first("test_hand9")
    run = Run(steps)
    feed(run, "I can't do that.")
    assert (run.outcome, run.reason) == ("failed", "replied where a call was due")
    run = Run(steps)                     # hand-written: no file tree, no server answer
    feed(run, as_call({"name": "fs_read", "arguments": {"path": "nope.txt"}}))
    assert (run.outcome, run.reason) == ("failed", "wrong fs_read call, answer unknown")
    run = Run(steps)                     # but an unknown tool is answered on any set
    feed(run, as_call({"name": "bash", "arguments": {"command": "ls"}}))
    assert run.outcome is None and run.history[-1]["content"].startswith("error: Unknown")
