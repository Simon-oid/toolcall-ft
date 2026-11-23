from toolcall.sample import first_wrong


def s(reply, right):
    return {"reply": reply, "score": {"levels": {"args": right}}}


def test_first_wrong_takes_the_first_mistake():
    assert first_wrong([s("ok", True), s("talk", False), s("other", False)])["reply"] == "talk"


def test_first_wrong_skips_server_garbage():
    assert first_wrong([s("!" * 30, False), s("talk", False)])["reply"] == "talk"


def test_first_wrong_keeps_the_first_sample_when_all_are_right():
    assert first_wrong([s("a", True), s("b", True)])["reply"] == "a"
