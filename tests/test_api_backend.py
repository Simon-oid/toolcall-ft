import json

import httpx
import pytest

from toolcall.api_backend import ApiChat, TokenWindow
from toolcall.backends import BackendError


def ok(name="crag_search", args='{"query":"x"}', usage=None):
    return httpx.Response(200, json={
        "choices": [{"message": {"tool_calls": [{"function": {"name": name, "arguments": args}}]}}],
        "usage": usage or {"prompt_tokens": 700, "completion_tokens": 40,
                           "completion_tokens_details": {"reasoning_tokens": 6}}})


def chat(handler, **kw):
    sleeps: list[float] = []
    c = ApiChat(base_url="https://api.test/v1", model="m", api_key="k", tools=[{"type": "x"}],
                transport=httpx.MockTransport(handler), sleep=sleeps.append, **kw)
    return c, sleeps


def test_sends_greedy_request_with_auth_tools_and_reasoning_effort():
    seen = []

    def handler(r: httpx.Request) -> httpx.Response:
        seen.append((r.url.path, r.headers["authorization"], json.loads(r.content)))
        return ok()

    c, _ = chat(handler, reasoning_effort="low")
    out = c.generate([[{"role": "user", "content": "q"}]])
    path, auth, body = seen[0]
    assert path == "/v1/chat/completions" and auth == "Bearer k"
    assert body["temperature"] == 0 and body["model"] == "m" and body["tools"] == [{"type": "x"}]
    assert body["reasoning_effort"] == "low"
    assert out == ['<tool_call>\n{"name": "crag_search", "arguments": {"query":"x"}}\n</tool_call>']
    assert c.usage == [{"prompt": 700, "completion": 40, "reasoning": 6}]


def test_no_reasoning_effort_field_unless_set():
    seen = []

    def handler(r):
        seen.append(json.loads(r.content))
        return ok()

    chat(handler)[0].generate([[]])
    assert "reasoning_effort" not in seen[0]


def test_text_reply_without_call_is_returned_as_is():
    c, _ = chat(lambda r: httpx.Response(200, json={
        "choices": [{"message": {"content": "Which file?"}}], "usage": {}}))
    assert c.generate([[]]) == ["Which file?"]


def test_rejected_tool_call_is_scored_from_the_failed_generation():
    # Groq refuses a call to a tool not in the request with a 400 that
    # carries the model's raw output: that output is the model's answer.
    def handler(r):
        return httpx.Response(400, json={"error": {
            "code": "tool_use_failed", "message": "tool call validation failed",
            "failed_generation": '{"name": "get_website", "arguments": {"url": "a"}}'}})

    out = chat(handler)[0].generate([[]])
    assert out == ['<tool_call>\n{"name": "get_website", "arguments": {"url": "a"}}\n</tool_call>']


def test_unparseable_failed_generation_is_kept_raw():
    def handler(r):
        return httpx.Response(400, json={"error": {"code": "tool_use_failed",
                                                   "failed_generation": "garbled"}})

    assert chat(handler)[0].generate([[]]) == ["garbled"]


def test_429_waits_retry_after_then_retries():
    calls = []

    def handler(r):
        calls.append(1)
        return httpx.Response(429, headers={"retry-after": "7"}) if len(calls) == 1 else ok()

    c, sleeps = chat(handler)
    assert c.generate([[]])[0].startswith("<tool_call>")
    assert sleeps == [7.0]


def test_gives_up_after_max_retries():
    c, _ = chat(lambda r: httpx.Response(429, headers={"retry-after": "1"}), max_retries=2)
    with pytest.raises(BackendError, match="429"):
        c.generate([[]])


def test_other_http_errors_raise():
    c, _ = chat(lambda r: httpx.Response(500, text="boom"))
    with pytest.raises(BackendError, match="500"):
        c.generate([[]])


def test_token_window_waits_until_budget_frees():
    now = [0.0]
    w = TokenWindow(budget=1000, window_s=60.0, clock=lambda: now[0])
    w.add(800)
    assert w.wait_for(100) == 0.0                 # 900 fits
    assert w.wait_for(300) == pytest.approx(60.0)  # 1100 does not: wait for the 800 to age out
    now[0] = 61.0
    assert w.wait_for(300) == 0.0
