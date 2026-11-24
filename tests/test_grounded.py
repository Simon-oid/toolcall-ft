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


def test_call_pairs_take_wrong_calls_only_with_the_training_target():
    from toolcall.prefs import call_pairs
    from toolcall.train import completion
    calls = [r for r in rows("mt_train") if r["expected"] is not None][:3]
    single = [r for r in rows("train") if r["expected"] is not None][:1]
    wrong = {"reply": "I can do that once I know more.", "call": None,
             "score": {"levels": {"args": False}}}
    right = {"reply": completion(calls[1], {}), "call": "x", "score": {"levels": {"args": True}}}
    junk = {"reply": "!" * 40, "call": None, "score": {"levels": {"args": False}}}
    said = {calls[0]["id"]: wrong, calls[1]["id"]: right, calls[2]["id"]: junk,
            single[0]["id"]: wrong}
    ps = call_pairs(calls + single, said)
    assert [p["id"] for p in ps] == [calls[0]["id"], single[0]["id"]]
    assert ps[0]["chosen"] == completion(calls[0], {}) and ps[0]["chosen"].startswith("<tool_call>")
    assert ps[0]["rejected"] == wrong["reply"]
    assert "context" in ps[0] and ps[1]["request"] == single[0]["request"]


def test_call_pairs_skip_final_turns():
    from toolcall.prefs import call_pairs
    final = [r for r in rows("mt_train") if r["expected"] is None][:2]
    said = {r["id"]: {"reply": "x", "call": None, "score": {"levels": {"args": False}}}
            for r in final}
    assert call_pairs(final, said) == []


def test_abstain_pairs_prefer_the_reply_to_an_unneeded_call():
    from toolcall.prefs import abstain_pairs
    from toolcall.train import completion
    single = [r for r in rows("train") if r["expected"] is None and r["intent"] != "no_tool"][:2]
    asked = [r for r in rows("mt_train")
             if r["expected"] is None and r["context"][-1]["role"] == "user"][:1]
    final = [r for r in rows("mt_train")
             if r["expected"] is None and r["context"][-1]["role"] == "tool"][:1]
    call = {"reply": '<tool_call>\n{"name": "crag_search"}\n</tool_call>', "call": {"name": "x"},
            "score": {"levels": {"args": False}, "abstained_ok": False}}
    ok = {"reply": "fine", "call": None, "score": {"levels": {"args": False}, "abstained_ok": True}}
    junk = {"reply": "!" * 40, "call": None,
            "score": {"levels": {"args": False}, "abstained_ok": False}}
    said = {single[0]["id"]: call, single[1]["id"]: ok, asked[0]["id"]: call, final[0]["id"]: call}
    ps = abstain_pairs(single + asked + final, said, {})
    assert [p["id"] for p in ps] == [single[0]["id"], asked[0]["id"]]
    assert ps[0]["kind"] == "abstain" and ps[0]["rejected"] == call["reply"]
    assert ps[0]["chosen"] == completion(single[0], {}) and ps[0]["request"] == single[0]["request"]
    assert "context" in ps[1]
    said[single[0]["id"]] = junk
    assert [p["id"] for p in abstain_pairs(single, said, {})] == []


def test_abstain_pairs_skip_no_tool_rows_without_a_distilled_reply():
    from toolcall.prefs import abstain_pairs
    nt = [r for r in rows("train") if r["intent"] == "no_tool"][:1]
    call = {"reply": "<tool_call>x</tool_call>", "call": {"name": "x"},
            "score": {"levels": {"args": False}, "abstained_ok": False}}
    assert abstain_pairs(nt, {nt[0]["id"]: call}, {}) == []
    got = abstain_pairs(nt, {nt[0]["id"]: call}, {nt[0]["request"]: "A cat named Soot."})
    assert got[0]["chosen"] == "A cat named Soot."
