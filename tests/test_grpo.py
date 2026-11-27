import json
from pathlib import Path

from toolcall.grpo import PARTIAL, case_rewards, prompts_and_cases

DATA = Path(__file__).resolve().parents[1] / "data"


def first(split, pred):
    for x in (DATA / f"{split}.jsonl").read_text().splitlines():
        row = json.loads(x)
        if pred(row):
            return row
    raise AssertionError(f"no such row in {split}")


def call(name, **arguments):
    return "<tool_call>\n" + json.dumps({"name": name, "arguments": arguments}) + "\n</tool_call>"


CALL_CASE = first("train", lambda r: r["expected"] is not None
                  and r["expected"]["name"] == "crag_search")
NO_CALL_CASE = first("train", lambda r: r["expected"] is None)
FINAL_CASE = first("mt_train_g", lambda r: r.get("answer") is not None)


def test_right_call_scores_one():
    right = call(CALL_CASE["call"]["name"], **CALL_CASE["call"]["arguments"])
    assert case_rewards([CALL_CASE], [right]) == [1.0]


def test_valid_but_wrong_call_scores_partial():
    wrong = call("crag_search", query="something unrelated entirely")
    assert case_rewards([CALL_CASE], [wrong]) == [PARTIAL]


def test_broken_call_and_prose_score_zero():
    broken = "<tool_call>\n{\"name\": \"crag_search\", \"arguments\": \n</tool_call>"
    prose = "Sure, I can help with that."
    assert case_rewards([CALL_CASE, CALL_CASE], [broken, prose]) == [0.0, 0.0]


def test_no_call_turn_rewards_abstaining_only():
    assert case_rewards([NO_CALL_CASE, NO_CALL_CASE],
                        ["Hello! How can I help?", call("fs_list", path=".")]) == [1.0, 0.0]


def test_final_reply_needs_the_fact():
    rule = FINAL_CASE["answer"]
    facts = [*rule.get("all", ()), *rule.get("any", ())[:1]]
    got = case_rewards([FINAL_CASE, FINAL_CASE], [f"Done. It says: {'; '.join(facts)}", "Done."])
    assert got[0] == 1.0
    assert got[1] == 0.0


def test_dataset_rows_carry_their_case():
    rows = prompts_and_cases(["train"], limit=3)
    assert len(rows) == 3
    for r in rows:
        assert r["prompt"].rstrip().endswith("<|im_start|>assistant")
        assert json.loads(r["case"])["id"].startswith("train-")


def test_hard_from_keeps_only_turns_with_a_wrong_sample(tmp_path):
    rows = prompts_and_cases(["train"], limit=4)
    ids = [json.loads(r["case"])["id"] for r in rows]
    sampled = tmp_path / "results.jsonl"
    sampled.write_text("".join(json.dumps({"id": i, "reply": "x", "score": s}) + "\n"
                               for i, s in zip(ids, [
                                   {"levels": {"args": False}, "abstained_ok": None},
                                   {"levels": {"args": True}, "abstained_ok": None},
                                   {"levels": None, "abstained_ok": False},
                                   {"levels": None, "abstained_ok": True}], strict=True)))
    kept = prompts_and_cases(["train"], limit=4, hard_from=sampled)
    assert [json.loads(r["case"])["id"] for r in kept] == [ids[0], ids[2]]


def test_hard_from_ignores_server_garbage(tmp_path):
    rows = prompts_and_cases(["train"], limit=1)
    i = json.loads(rows[0]["case"])["id"]
    sampled = tmp_path / "results.jsonl"
    sampled.write_text(json.dumps({"id": i, "reply": "!" * 40,
                                   "score": {"levels": {"args": False}, "abstained_ok": None}}))
    assert prompts_and_cases(["train"], limit=1, hard_from=sampled) == []
