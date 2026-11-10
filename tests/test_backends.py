import json

import httpx
import pytest

from toolcall.backends import BackendError, LlamaCpp, LlamaCppChat


def transport(handler):
    return httpx.MockTransport(handler)


def test_completion_sends_greedy_request_and_returns_raw_text():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(200, json={"content": "<tool_call>x</tool_call>"})

    out = LlamaCpp(transport=transport(handler)).generate(["p1", "p2"])
    assert out == ["<tool_call>x</tool_call>"] * 2
    assert [b["prompt"] for b in seen] == ["p1", "p2"]            # one at a time, in order
    assert seen[0]["temperature"] == 0.0 and "json_schema" not in seen[0]


def test_constrained_completion_sends_the_schema():
    seen = []

    def handler(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, json={"content": "{}"})

    LlamaCpp(json_schema={"type": "object"}, transport=transport(handler)).generate(["p"])
    assert seen[0]["json_schema"] == {"type": "object"}


def test_http_error_is_a_backend_error():
    backend = LlamaCpp(transport=transport(lambda r: httpx.Response(500, text="boom")))
    with pytest.raises(BackendError, match="500"):
        backend.generate(["p"])


def test_chat_rebuilds_the_call_with_the_models_raw_arguments():
    def handler(request):
        body = json.loads(request.content)
        assert body["tools"] == [{"type": "function"}] and body["temperature"] == 0.0
        return httpx.Response(200, json={"choices": [{"message": {"content": None, "tool_calls": [
            {"function": {"name": "fs_read", "arguments": '{"path": "a.md",  "limit": 5}'}}]}}]})

    out = LlamaCppChat(tools=[{"type": "function"}], transport=transport(handler)) \
        .generate([[{"role": "user", "content": "q"}]])
    assert out == ['<tool_call>\n{"name": "fs_read", "arguments": {"path": "a.md",  "limit": 5}}'
                   "\n</tool_call>"]


def test_chat_without_a_call_returns_the_text():
    def handler(request):
        return httpx.Response(200, json={"choices": [{"message": {"content": "Which file?"}}]})

    assert LlamaCppChat(tools=[], transport=transport(handler)).generate([[]]) == ["Which file?"]


def test_chat_http_error():
    backend = LlamaCppChat(tools=[], transport=transport(lambda r: httpx.Response(503)))
    with pytest.raises(BackendError):
        backend.generate([[]])
