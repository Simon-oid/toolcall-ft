import json
from pathlib import Path

from toolcall.episodes import SPLITS
from toolcall.grounded import SAVE_KINDS, build
from toolcall.prefs import pairs
from toolcall.score import answer_ok

DATA = Path(__file__).resolve().parents[1] / "data"


def rows(split):
    return [json.loads(x) for x in (DATA / f"{split}.jsonl").read_text().splitlines()]


def changed(split):
    return [(a, b) for a, b in zip(rows(split), build(rows(split)), strict=True)
            if a["reply"] != b["reply"]]


def test_committed_grounded_files_are_what_the_builder_writes():
    for split in SPLITS:
        assert build(rows(split)) == rows(split + "_g"), split


def test_only_final_replies_and_answers_change():
    for split in SPLITS:
        for a, b in zip(rows(split), build(rows(split)), strict=True):
            assert b["split"] == split + "_g" and b["id"] == a["id"].replace(split, b["split"])
            assert {k: v for k, v in a.items() if k not in ("reply", "answer", "id", "split")} \
                == {k: v for k, v in b.items() if k not in ("reply", "answer", "id", "split")}
            if a["reply"] != b["reply"]:
                assert a["expected"] is None and a["step"] == a["steps"] - 1


def test_grounded_kinds_are_the_save_kinds_and_check_then_read():
    kinds = {b["intent"] for a, b in changed("mt_train")}
    assert kinds == {*SAVE_KINDS, "check_then_read"}


def test_grounded_replies_pass_their_rule_and_the_old_ones_fail_it():
    for split in SPLITS:
        for a, b in changed(split):
            assert answer_ok(b["reply"], b["answer"]), b["id"]
            assert not answer_ok(a["reply"], b["answer"]), b["id"]


def test_a_missing_file_keeps_its_reply():
    missing = [b for a, b in zip(rows("mt_train"), build(rows("mt_train")), strict=True)
               if b["intent"] == "check_then_read" and b["step"] == 1 and b["expected"] is None]
    assert missing and all(b["reply"] == a["reply"] for a, b in
                           zip(rows("mt_train"), build(rows("mt_train")), strict=True)
                           if b in missing)


def test_pairs_take_the_models_wrong_reply_as_rejected():
    g = [b for _, b in changed("mt_train")][:3]
    said = {b["id"].replace("_g", "", 1): {"reply": "Saved.", "call": None} for b in g}
    ps = pairs(g, said)
    assert [p["chosen"] for p in ps] == [b["reply"] for b in g]
    assert all(p["rejected"] == "Saved." for p in ps)


def test_pairs_skip_replies_that_are_already_grounded():
    g = [b for _, b in changed("mt_train")][:2]
    said = {g[0]["id"].replace("_g", "", 1): {"reply": g[0]["reply"] + " ", "call": None},
            g[1]["id"].replace("_g", "", 1): {"reply": "x", "call": '{"name": "fs_stat"}'}}
    ps = pairs(g, said)
    assert [p["id"] for p in ps] == [g[1]["id"]]        # a call is always wrong here
