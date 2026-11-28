import json
from pathlib import Path

from test_episodes import history_calls

from toolcall.judge import judge
from toolcall.retry import ABSENT_ALIAS, ALIAS, KINDS, RETRY, SPLITS, build
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


def of_kind(kind):
    eps = [s for s in episodes().values() if s[0]["intent"] == kind]
    assert eps, kind
    return eps


def scored_tools(steps):
    return [r["expected"]["name"] if r["expected"] else None for r in steps]


def test_committed_data_is_what_the_generator_makes():
    for split in SPLITS:
        committed = [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]
        assert by_split(split) == committed, split


def test_every_kind_is_in_every_split():
    for split in SPLITS:
        assert {r["intent"] for r in by_split(split)} == set(KINDS), split


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


def test_every_final_reply_passes_its_own_answer_check():
    for steps in episodes().values():
        last = steps[-1]
        assert last["expected"] is None and last["answer"], last["id"]
        assert answer_ok(last["reply"], last["answer"]), (last["id"], last["reply"])


def test_steps_of_an_episode_extend_one_conversation():
    for steps in episodes().values():
        assert [r["step"] for r in steps] == list(range(steps[0]["steps"]))
        for a, b in zip(steps, steps[1:], strict=False):
            assert b["context"][:len(a["context"])] == a["context"]


def test_retry_kinds_call_again_after_the_miss():
    for kind in RETRY:
        for steps in of_kind(kind):
            assert scored_tools(steps)[-2] is not None, steps[0]["id"]


def test_read_miss_list_lists_the_folder_then_reads_a_file_it_showed():
    for steps in of_kind("read_miss_list"):
        assert scored_tools(steps)[-3:] == ["fs_list", "fs_read", None], steps[0]["id"]
        listing = steps[-2]["context"][-1]["content"]
        assert steps[-2]["call"]["arguments"]["path"].rsplit("/", 1)[1] in listing


def test_list_into_subdir_lists_the_one_subfolder():
    for steps in of_kind("list_into_subdir"):
        first, second = (r for r in steps if r["expected"] and r["call"]["name"] == "fs_list")
        listing = second["context"][-1]["content"]
        dirs = [x.split()[-1] for x in listing.splitlines() if x.startswith("dir")]
        assert len(dirs) == 1
        parent = first["call"]["arguments"]["path"]
        assert second["call"]["arguments"]["path"] == f"{parent}/{dirs[0]}"


def test_a_reworded_search_uses_a_name_from_the_conversation():
    for kind in ("search_reword", "search_pointer"):
        for steps in of_kind(kind):
            retry = steps[-2]
            assert retry["call"]["name"] == "crag_search"
            words = retry["expected"]["arguments"]["query"]["contains_all"]
            said = json.dumps(retry["context"]).lower()
            assert all(w in said for w in words), retry["id"]
            first = [c for c, _ in history_calls(retry["context"])][-1]
            assert not all(w in first["arguments"]["query"].lower() for w in words)


def test_search_not_guess_searches_and_never_reads_on_a_guess():
    for steps in of_kind("search_not_guess"):
        assert [t for t in scored_tools(steps) if t] == ["crag_search"]


def test_test_aliases_never_appear_in_training():
    train = json.dumps([r["context"] for r in by_split("mt8_train") + by_split("mt8_val")])
    for topic in ("the SSRF egress guard", "log redaction", "the HNSW index", "the soak test"):
        assert ALIAS[topic][0] not in train
    for topic in ("the payroll export", "dark mode", "the CDN cache"):
        assert ABSENT_ALIAS[topic][0] not in train


def test_test_steps_never_appear_in_training():
    seen = {json.dumps(r["context"], sort_keys=True) for r in by_split("mt8_train")}
    for r in by_split("mt8_test_id") + by_split("mt8_test_ood"):
        assert json.dumps(r["context"], sort_keys=True) not in seen, r["id"]
