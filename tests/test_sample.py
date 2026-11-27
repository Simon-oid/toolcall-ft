from toolcall.sample import first_wrong, right


def s(reply, right):
    return {"reply": reply, "score": {"levels": {"args": right}}}


def test_first_wrong_takes_the_first_mistake():
    assert first_wrong([s("ok", True), s("talk", False), s("other", False)])["reply"] == "talk"


def test_first_wrong_skips_server_garbage():
    assert first_wrong([s("!" * 30, False), s("talk", False)])["reply"] == "talk"


def test_first_wrong_keeps_the_first_sample_when_all_are_right():
    assert first_wrong([s("a", True), s("b", True)])["reply"] == "a"


def a(reply, ok):
    return {"reply": reply, "score": {"levels": {"args": False}, "abstained_ok": ok}}


def test_first_wrong_on_abstain_turns_takes_the_first_unneeded_call():
    picked = first_wrong([a("Sure, try this.", True), a("<tool_call>x</tool_call>", False)])
    assert picked["reply"] == "<tool_call>x</tool_call>"


def test_first_wrong_on_abstain_turns_keeps_the_first_when_all_abstain():
    assert first_wrong([a("one", True), a("two", True)])["reply"] == "one"


def f(reply, answered):
    return {"reply": reply, "score": {"levels": None, "abstained_ok": True, "answered": answered}}


def test_final_reply_without_the_fact_is_a_mistake():
    assert first_wrong([f("Done.", True), f("Saved.", False)])["reply"] == "Saved."


def test_abstain_turns_without_an_answer_rule_stay_right():
    assert right(f("Hello!", None))
