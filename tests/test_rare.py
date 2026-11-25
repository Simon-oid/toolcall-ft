import datetime as dt
import json
import os
import random
import re
from pathlib import Path

import pytest
from test_episodes import FS_MCP, INSPECT, _expected_output, _server_output, history_calls

from toolcall.episodes import SPLITS as MT_SPLITS
from toolcall.episodes import build as build_mt
from toolcall.judge import judge
from toolcall.rare import EXTRA, KINDS, SPLITS, DirTree, build, read_range
from toolcall.score import answer_ok, parse_expected, score

ROWS = build()
DATA = Path(__file__).resolve().parents[1] / "data"


def by_split(split):
    return [r for r in ROWS if r["split"] == split]


def episodes(rows=ROWS):
    out: dict[str, list[dict]] = {}
    for r in rows:
        out.setdefault(r["episode"], []).append(r)
    return {k: sorted(v, key=lambda r: r["step"]) for k, v in out.items()}


def scored_tools(steps):
    return [r["expected"]["name"] if r["expected"] else None for r in steps]


def of_kind(kind):
    eps = [s for s in episodes().values() if s[0]["intent"] == kind]
    assert eps, kind
    return eps


def last_history_call(context):
    return [c for c, _ in history_calls(context)][-1]


# ---- the same guarantees as episodes.py ----

def test_build_is_deterministic():
    assert build() == ROWS


def test_committed_files_are_what_the_generator_writes():
    for split in SPLITS:
        committed = [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]
        assert by_split(split) == committed, split


def test_v5_v6_episodes_are_unchanged():
    # Own seed and own files: the episodes v5 and v6 were trained on stay byte-identical.
    mt = build_mt()
    for split in MT_SPLITS:
        committed = [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]
        assert [r for r in mt if r["split"] == split] == committed, split


def test_every_kind_is_in_every_split():
    for split in SPLITS:
        assert {r["intent"] for r in by_split(split)} == set(KINDS), split


def test_held_out_families_appear_only_in_test_ood():
    for r in ROWS:
        assert (r["family"] >= 6) == (r["split"] == "mt7_test_ood"), r["id"]


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


def test_every_final_reply_carries_a_value():
    # Grounded from the start (v6's lesson): every last turn has facts to check.
    for steps in episodes().values():
        assert steps[-1]["expected"] is None and steps[-1]["answer"], steps[-1]["id"]


def test_steps_of_an_episode_extend_one_conversation():
    for steps in episodes().values():
        assert [r["step"] for r in steps] == list(range(steps[0]["steps"]))
        for a, b in zip(steps, steps[1:], strict=False):
            assert b["context"][:len(a["context"])] == a["context"]
            turn = b["context"][len(a["context"])]
            if a["expected"] is not None:
                assert turn["tool_calls"][0]["function"] == a["call"]
            else:
                assert turn["content"] == a["reply"]


def test_evaluation_splits_never_repeat_a_step():
    for split in SPLITS[1:]:
        keys = [json.dumps(r["context"], sort_keys=True) for r in by_split(split)]
        assert len(keys) == len(set(keys)), split


def test_test_steps_never_appear_in_training():
    seen = {json.dumps(r["context"], sort_keys=True) for r in by_split("mt7_train")}
    for r in by_split("mt7_test_id") + by_split("mt7_test_ood"):
        assert json.dumps(r["context"], sort_keys=True) not in seen, r["id"]


def test_test_slot_values_are_unseen_in_training():
    train = json.dumps([r["context"] for r in by_split("mt7_train") + by_split("mt7_val")])
    test = EXTRA["test"]
    for value in [*test["subdirs"], *test["events"], *test["config"],
                  *(t for t, _ in test["absent"])]:
        assert value not in train, value


def _norm(text):
    return " ".join(text.lower().split())


MIN_WORDS = 5     # shorter messages ("How big is it?", "Thanks!") are generic, not content


def test_hand_written_requests_never_appear_in_training():
    # Counts only: a failure must not print a blind set's text.
    train = {_norm(m["content"]) for r in by_split("mt7_train") + by_split("mt7_val")
             for m in r["context"] if m["role"] == "user"}
    for name in ("test_hand6", "test_hand7", "test_hand8"):
        hand = {_norm(m["content"]) for line in (DATA / f"{name}.jsonl").read_text().splitlines()
                for m in json.loads(line)["context"] if m["role"] == "user"}
        hits = sum(1 for h in hand if len(h.split()) >= MIN_WORDS and h in train)
        assert hits == 0, f"{name}: {hits} user messages also in mt7 training"


# ---- what each family must teach ----

def test_drill_down_lists_every_level_then_reads():
    for steps in of_kind("drill_down"):
        tools = scored_tools(steps)
        assert tools[-2:] == ["fs_read", None] and len(tools) >= 4, tools
        assert set(tools[:-2]) == {"fs_list"}


def test_search_then_read_source_reads_the_file_the_chunk_came_from():
    for steps in of_kind("search_then_read_source"):
        assert scored_tools(steps) == ["crag_search", "fs_read", None]
        hit = steps[1]["context"][-1]["content"].split("\n", 1)[0].split("] ", 1)[1]
        assert steps[1]["call"]["arguments"]["path"] == hit


def test_a_missing_file_is_followed_by_a_listing_not_a_give_up():
    for steps in of_kind("read_miss_then_list"):
        assert scored_tools(steps) == ["fs_read", "fs_list", "fs_read", None]
        assert steps[1]["context"][-1]["content"] == "error: no such file or directory"


def test_a_dead_end_search_is_reported_not_repeated():
    for steps in of_kind("search_dead_end"):
        assert scored_tools(steps) == ["crag_search", None]
        assert steps[1]["context"][-1]["content"].startswith("(no ")


@pytest.mark.parametrize("kind", ["empty_then_asked", "missing_then_asked", "size_from_listing"])
def test_what_the_history_already_answers_gets_no_call(kind):
    for steps in of_kind(kind):
        assert scored_tools(steps) == [None], steps[0]["id"]


def test_size_from_listing_reports_the_size_the_listing_shows():
    for steps in of_kind("size_from_listing"):
        listing = last_history_call(steps[0]["context"])
        result = [r for c, r in history_calls(steps[0]["context"]) if c == listing][-1]
        assert listing["name"] == "fs_list"
        assert all(v in result for v in steps[0]["answer"]["all"])


def test_read_edit_write_keeps_the_rest_of_the_file():
    for steps in of_kind("read_edit_write"):
        assert scored_tools(steps) == ["fs_read", "fs_write", None]
        read, write = steps[0]["call"]["arguments"], steps[1]["call"]["arguments"]
        assert read["path"] == write["path"]
        old = steps[1]["context"][-1]["content"].splitlines()
        new = write["content"].splitlines()
        assert len(set(old) & set(new)) >= len(old) - 1 and new != old
        assert len(steps[1]["expected"]["arguments"]["content"]["contains_all"]) >= 2


def test_list_then_stat_stats_the_file_the_request_picks():
    for steps in of_kind("list_then_stat"):
        assert scored_tools(steps) == ["fs_list", "fs_stat", None]
        listing = steps[1]["context"][-1]["content"]
        sizes = {line.split()[2]: int(line.split()[1]) for line in listing.splitlines()}
        assert len(set(sizes.values())) == len(sizes)       # "the largest" is one file
        picked = steps[1]["call"]["arguments"]["path"].rsplit("/", 1)[1]
        assert sizes[picked] in (max(sizes.values()), min(sizes.values()))


def test_next_page_reads_from_the_line_after_the_last_one_shown():
    for steps in of_kind("read_next_page"):
        assert scored_tools(steps) == ["fs_read", None]
        before = last_history_call(steps[0]["context"])["arguments"]
        got = steps[0]["call"]["arguments"]
        assert got["offset"] == before["offset"] + before["limit"]
        assert got["path"] == before["path"]


def test_a_correction_changes_what_the_last_call_got_wrong():
    for steps in of_kind("user_corrects"):
        assert scored_tools(steps) in (["fs_read", None], ["fs_list", None])
        before = last_history_call(steps[0]["context"])
        assert before["name"] == steps[0]["call"]["name"]
        assert before["arguments"] != steps[0]["call"]["arguments"]


def test_write_then_check_reads_back_only_when_the_history_cannot_answer():
    shapes = set()
    for steps in of_kind("write_then_check"):
        tools = tuple(scored_tools(steps))
        shapes.add(tools)
        if tools == ("fs_read", None):
            write = last_history_call(steps[0]["context"])["arguments"]
            assert steps[0]["call"]["arguments"]["path"] == write["path"]
    assert shapes == {("fs_read", None), (None,)}


# ---- the tool results ----

def test_dir_tree_lists_subdirectories_and_reads_line_ranges():
    t = DirTree(random.Random(0))
    t.add("a/x.md", "one\n")
    t.add("a/b/y.md", "two\n")
    assert t.listing("a") == f"{'dir':<5}{4096:>12}  b\n{'file':<5}{4:>12}  x.md"
    assert read_range("1\n2\n3\n4\n", 2, 2) == "2\n3\n"
    assert read_range("1\n2\n", 5, 2) == "(no lines in the requested range)"


DIR_LINE = re.compile(r"^dir\s+\d+", re.M)


@pytest.mark.skipif(not (INSPECT.exists() and FS_MCP.exists()), reason="cMCP not built")
def test_fs_results_are_what_the_real_server_returns(tmp_path):
    # Directory sizes depend on the file system; every other byte must match.
    rng = random.Random(0)
    eps = [s[-1] for s in episodes().values()
           if any(c["name"].startswith("fs_") for c, _ in history_calls(s[-1]["context"]))]
    checked = 0
    for n, last in enumerate(rng.sample(eps, 80)):
        root = tmp_path / str(n)
        root.mkdir()
        for path, f in last["files"].items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f["content"])
            target.chmod(0o644)
            ts = dt.datetime.strptime(f["modified"], "%Y-%m-%dT%H:%M:%SZ") \
                .replace(tzinfo=dt.UTC).timestamp()
            os.utime(target, (ts, ts))
        for c, result in history_calls(last["context"]):
            if not c["name"].startswith("fs_"):
                continue
            if c["name"] == "fs_write":
                (root / c["arguments"]["path"]).parent.mkdir(parents=True, exist_ok=True)
            got = DIR_LINE.sub("dir N", _server_output(c["name"], c["arguments"], root))
            want = DIR_LINE.sub("dir N", _expected_output(result))
            assert got.rstrip("\n") == want.rstrip("\n"), (last["id"], c)
            checked += 1
    assert checked >= 80
