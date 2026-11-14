"""A hosted model as a baseline: an OpenAI-compatible /chat/completions
endpoint with native `tools`, e.g. a free tier (Groq).

Unlike backends.py this is not llama.cpp, so a gap to the local rows is
the model *and* the runtime; the report says which. Calls are rebuilt in
the same `<tool_call>` text form LlamaCppChat produces, so the same
scorer and C judge grade them.

Free tiers cap tokens per minute: requests go one at a time, and a
rolling 60 s window holds each one back until its estimated tokens fit.
A 429 waits for Retry-After and retries.
"""

from __future__ import annotations

import json
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field

import httpx

from .backends import BackendError

TPM_WINDOW_S = 60.0
DEFAULT_RETRY_AFTER_S = 10.0


@dataclass
class TokenWindow:
    """Tokens spent in the last `window_s` seconds, against a budget."""
    budget: int
    window_s: float = TPM_WINDOW_S
    clock: Callable[[], float] = time.monotonic
    _spent: deque = field(default_factory=deque)

    def add(self, tokens: int) -> None:
        self._spent.append((self.clock(), tokens))

    def wait_for(self, tokens: int) -> float:
        """Seconds until `tokens` more fit in the window (0: now). A request
        larger than the whole budget is not held back: waiting cannot help."""
        now = self.clock()
        while self._spent and now - self._spent[0][0] >= self.window_s:
            self._spent.popleft()
        total = sum(t for _, t in self._spent) + tokens
        if total <= self.budget:
            return 0.0
        for ts, t in self._spent:              # oldest ages out first
            total -= t
            if total <= self.budget:
                return max(ts + self.window_s - now, 0.0)
        return 0.0


def as_call_text(name: str, arguments: str) -> str:
    return ('<tool_call>\n{"name": ' + json.dumps(name) + ', "arguments": '
            + arguments + "}\n</tool_call>")


def _failed_generation(body: object) -> str | None:
    """Groq's 400 for a call it could not validate (e.g. to a tool not in the
    request) carries the model's raw output: that output is the answer."""
    err = body.get("error") if isinstance(body, dict) else None
    if not isinstance(err, dict) or err.get("code") != "tool_use_failed":
        return None
    raw = err.get("failed_generation") or ""
    try:
        call = json.loads(raw)
        return as_call_text(call["name"], json.dumps(call.get("arguments", {})))
    except (json.JSONDecodeError, KeyError, TypeError):
        return raw


@dataclass
class ApiChat:
    base_url: str
    model: str
    api_key: str
    tools: list | None = None
    reasoning_effort: str | None = None   # gpt-oss: "low" | "medium" | "high"
    max_tokens: int = 256
    tokens_per_minute: int = 7500         # under the free tier's 8000, with margin
    est_tokens: int = 800                 # per request, before its usage is known
    max_retries: int = 6
    timeout_s: float = 120.0
    transport: httpx.BaseTransport | None = None
    sleep: Callable[[float], None] = time.sleep
    usage: list = field(default_factory=list)

    def _body(self, msgs: list[dict]) -> dict:
        body = {"model": self.model, "messages": msgs, "tools": self.tools,
                "max_tokens": self.max_tokens, "temperature": 0}
        if self.reasoning_effort:
            body["reasoning_effort"] = self.reasoning_effort
        return body

    def _record(self, u: dict) -> int:
        details = u.get("completion_tokens_details") or {}
        row = {"prompt": u.get("prompt_tokens", 0), "completion": u.get("completion_tokens", 0),
               "reasoning": details.get("reasoning_tokens", 0)}
        self.usage.append(row)
        return row["prompt"] + row["completion"]

    def _reply(self, r: httpx.Response, window: TokenWindow) -> str:
        if r.status_code == 400 and (raw := _failed_generation(r.json())) is not None:
            window.add(self.est_tokens)
            self.usage.append({"prompt": 0, "completion": 0, "reasoning": 0, "rejected": True})
            return raw
        if r.status_code != 200:
            raise BackendError(f"API HTTP {r.status_code}: {r.text[:200]}")
        j = r.json()
        window.add(self._record(j.get("usage") or {}))
        msg = j["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        if not calls:
            return msg.get("content") or ""
        f = calls[0]["function"]
        return as_call_text(f["name"], f["arguments"])

    def _one(self, client: httpx.Client, window: TokenWindow, msgs: list[dict]) -> str:
        for _ in range(self.max_retries + 1):
            if (w := window.wait_for(self.est_tokens)) > 0:
                self.sleep(w)
            r = client.post(f"{self.base_url}/chat/completions", json=self._body(msgs))
            if r.status_code != 429:
                return self._reply(r, window)
            self.sleep(float(r.headers.get("retry-after", DEFAULT_RETRY_AFTER_S)))
        raise BackendError(f"API HTTP 429: still rate-limited after {self.max_retries} retries")

    def generate(self, conversations: list[list[dict]]) -> list[str]:
        window = TokenWindow(self.tokens_per_minute)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=self.timeout_s, transport=self.transport,
                          headers=headers) as client:
            return [self._one(client, window, m) for m in conversations]

    def props(self) -> dict:
        effort = f", reasoning_effort {self.reasoning_effort}" if self.reasoning_effort else ""
        return {"model_path": self.model, "build_info": f"hosted API {self.base_url}{effort}"}
