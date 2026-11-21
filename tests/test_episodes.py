import datetime as dt
import json
import os
import random
import subprocess
from pathlib import Path

import pytest

from toolcall.data import POOLS
from toolcall.data import build as build_single
from toolcall.episodes import KINDS, SPLITS, build
from toolcall.judge import judge
from toolcall.score import answer_ok, parse_expected, score

ROWS = build()
DATA = Path(__file__).resolve().parents[1] / "data"
CMCP = Path(os.environ.get("TOOLCALL_CMCP", Path(__file__).resolve().parents[2] / "cMCP"))
INSPECT = CMCP / "tools" / "cmcp-inspect" / "cmcp-inspect"
FS_MCP = CMCP / "tools" / "filesystem-mcp" / "filesystem-mcp"


def by_split(split):
    return [r for r in ROWS if r["split"] == split]


def episodes(rows=ROWS):
    out: dict[str, list[dict]] = {}
    for r in rows:
        out.setdefault(r["episode"], []).append(r)
    return out


def history_calls(context):
    """(call, result) for every call already in a context."""
    for m, nxt in zip(context, context[1:], strict=False):
        if m["role"] == "assistant" and m.get("tool_calls"):
            yield m["tool_calls"][0]["function"], nxt["content"]


def test_build_is_deterministic():
    assert build() == ROWS


def test_committed_files_are_what_the_generator_writes():
    for split in SPLITS:
        committed = [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]
        assert by_split(split) == committed, split


def test_every_kind_is_in_every_split():
    for split in SPLITS:
        assert {r["intent"] for r in by_split(split)} == set(KINDS), split


def test_held_out_families_appear_only_in_test_ood():
    for r in ROWS:
        assert (r["family"] >= 6) == (r["split"] == "mt_test_ood"), r["id"]


def test_every_expected_call_is_valid_and_the_training_call_satisfies_it():
    calls = [r for r in ROWS if r["expected"] is not None]
    verdicts = judge([json.dumps(r["call"]) for r in calls])
    for r, v in zip(calls, verdicts, strict=True):
        s = score(parse_expected(r["expected"]), json.dumps(r["call"]), v)
        assert all(s.levels.values()), (r["id"], r["call"], v)


def test_every_call_in_a_history_is_valid():
    texts = [json.dumps(c) for r in ROWS for c, _ in history_calls(r["context"])]
    for v in judge(texts):
        assert v["json"] and v["schema"], v


def test_no_call_steps_have_a_reply_that_passes_its_own_answer_check():
    for r in ROWS:
        if r["expected"] is None:
            assert r["reply"] and "call" not in r
            assert r["answer"] is None or answer_ok(r["reply"], r["answer"]), r["id"]


def test_steps_of_an_episode_extend_one_conversation():
    # Step i+1 sees exactly step i's context, then the model turn step i asks for.
    for steps in episodes().values():
        steps.sort(key=lambda r: r["step"])
        assert [r["step"] for r in steps] == list(range(steps[0]["steps"]))
        for a, b in zip(steps, steps[1:], strict=False):
            assert b["context"][:len(a["context"])] == a["context"]
            turn = b["context"][len(a["context"])]
            assert turn["role"] == "assistant"
            if a["expected"] is not None:
                assert turn["tool_calls"][0]["function"] == a["call"]
            else:
                assert turn["content"] == a["reply"]


def test_every_episode_ends_without_a_call():
    for steps in episodes().values():
        assert max(steps, key=lambda r: r["step"])["expected"] is None


def test_evaluation_splits_never_repeat_a_step():
    for split in ("mt_val", "mt_test_id", "mt_test_ood"):
        keys = [json.dumps(r["context"], sort_keys=True) for r in by_split(split)]
        assert len(keys) == len(set(keys)), split


def test_test_steps_never_appear_in_training():
    seen = {json.dumps(r["context"], sort_keys=True) for r in by_split("mt_train")}
    for r in by_split("mt_test_id") + by_split("mt_test_ood"):
        assert json.dumps(r["context"], sort_keys=True) not in seen, r["id"]


def test_test_slot_values_are_unseen_in_training():
    train = json.dumps([r["context"] for r in by_split("mt_train") + by_split("mt_val")])
    for name in POOLS["test"]["names"]:
        assert f"/{name}." not in train and f" {name}." not in train, name
    for phrase, _ in POOLS["test"]["topics"]:
        assert phrase not in train, phrase


def test_single_turn_data_is_unchanged():
    # The episodes have their own seed and files: v1-v4 data stay byte-identical.
    for split in ("train", "val", "test_id", "test_ood"):
        committed = [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]
        assert [r for r in build_single() if r["split"] == split] == committed, split


def test_followups_resolve_what_the_single_turn_data_calls_ambiguous():
    # "How big is it?" alone must be asked about; after a read it is a call.
    stat = [r for r in ROWS if r["intent"] == "followup_stat" and r["step"] == 0]
    assert stat and all(r["expected"]["name"] == "fs_stat" for r in stat)
    assert all(r["expected"] is None for r in ROWS if r["intent"] == "followup_ask")


def _server_output(name, arguments, root):
    out = subprocess.run([str(INSPECT), "-c", name, "-a", json.dumps(arguments), "--",
                          str(FS_MCP), "--root", str(root)],
                         capture_output=True, text=True, timeout=10, check=False)
    assert out.returncode == 0, out.stderr
    return out.stdout.split(f"Calling {name}:\n", 1)[1]


def _expected_output(result):
    if result.startswith("error: "):
        return "[tool-level error]\n" + result.removeprefix("error: ")
    return result


@pytest.mark.skipif(not (INSPECT.exists() and FS_MCP.exists()), reason="cMCP not built")
def test_fs_results_are_what_the_real_server_returns(tmp_path):
    rng = random.Random(0)
    eps = [max(s, key=lambda r: r["step"]) for s in episodes().values()]
    fs_eps = [r for r in eps if any(c["name"].startswith("fs_")
                                    for c, _ in history_calls(r["context"]))]
    checked = 0
    for n, last in enumerate(rng.sample(fs_eps, 60)):
        root = tmp_path / str(n)
        root.mkdir()
        for path, f in last["files"].items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f["content"])
            target.chmod(0o644)
            t = dt.datetime.strptime(f["modified"], "%Y-%m-%dT%H:%M:%SZ")
            ts = t.replace(tzinfo=dt.UTC).timestamp()
            os.utime(target, (ts, ts))
        for c, result in history_calls(last["context"]):
            if not c["name"].startswith("fs_"):
                continue
            if c["name"] == "fs_write":
                (root / c["arguments"]["path"]).parent.mkdir(parents=True, exist_ok=True)
            got = _server_output(c["name"], c["arguments"], root)
            assert got.rstrip("\n") == _expected_output(result).rstrip("\n"), (last["id"], c)
            checked += 1
    assert checked >= 60


def test_answer_ok_needs_every_fact_and_one_of_the_alternatives():
    assert answer_ok("It is 35 Bytes.", {"all": ["35 bytes"]})
    assert not answer_ok("It is big.", {"all": ["35 bytes"]})
    assert answer_ok("notes/a.md does not exist.", {"any": ["doesn't exist", "does not exist"]})
    assert not answer_ok("Here it is.", {"any": ["doesn't exist"]})


def test_case_messages_and_the_openai_wire_format():
    from toolcall.prompt import case_messages, messages, openai_messages
    step = next(r for r in ROWS if r["intent"] == "find_then_read" and r["step"] == 2)
    msgs = case_messages(step)
    assert msgs[0]["role"] == "system" and msgs[1:] == step["context"]
    assert case_messages({"request": "hi"}) == messages("hi")
    wire = openai_messages(msgs)
    calls = [m for m in wire if m.get("tool_calls")]
    results = [m for m in wire if m["role"] == "tool"]
    assert [c["tool_calls"][0]["id"] for c in calls] == [r["tool_call_id"] for r in results]
    assert all(isinstance(c["tool_calls"][0]["function"]["arguments"], str) for c in calls)


def test_episode_scoring_counts_an_episode_only_when_every_step_is_right():
    from toolcall.evaluate import episode_rates, score_cases
    ep = [r for r in by_split("mt_test_id") if r["intent"] == "check_then_read"][:3]
    ep = [r for r in ep if r["episode"] == ep[0]["episode"]]
    right = ["<tool_call>\n" + json.dumps(r["call"]) + "\n</tool_call>" if r["expected"]
             else r["reply"] for r in ep]
    rows = score_cases(ep, right)
    assert episode_rates(rows)["episode right"][0] == 1.0
    wrong = [*right[:-1], "Sure, done."]          # the final reply drops the fact
    assert episode_rates(score_cases(ep, wrong))["episode right"][0] == 0.0
