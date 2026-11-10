"""Model backends. Every model is run the same way, through a llama.cpp
server (/completion): base and fine-tuned models alike, as GGUF, so a
difference between two rows of a report is the model or the constraint,
not the runtime. Text in, raw text out: we judge what the model wrote,
not what a server's tool-call parser made of it."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass

import httpx

STOP = ["<|im_end|>", "<|endoftext|>"]


class BackendError(RuntimeError):
    pass


@dataclass
class LlamaCpp:
    url: str = "http://127.0.0.1:8083"
    json_schema: dict | None = None      # set: constrained decoding
    max_tokens: int = 256
    # One request at a time: with parallel slots llama.cpp batches requests
    # together and greedy output stops being reproducible.
    concurrency: int = 1
    timeout_s: float = 120.0

    async def _one(self, client: httpx.AsyncClient, prompt: str, sem: asyncio.Semaphore) -> str:
        body = {"prompt": prompt, "n_predict": self.max_tokens, "temperature": 0.0,
                "top_k": 1, "seed": 0, "stop": STOP, "cache_prompt": True}
        if self.json_schema is not None:
            body["json_schema"] = self.json_schema
        async with sem:
            r = await client.post(f"{self.url}/completion", json=body)
        if r.status_code != 200:
            raise BackendError(f"llama.cpp HTTP {r.status_code}: {r.text[:200]}")
        return r.json()["content"]

    async def agenerate(self, prompts: list[str]) -> list[str]:
        sem = asyncio.Semaphore(self.concurrency)
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            return await asyncio.gather(*(self._one(client, p, sem) for p in prompts))

    def generate(self, prompts: list[str]) -> list[str]:
        return asyncio.run(self.agenerate(prompts))

    def props(self) -> dict:
        try:
            return httpx.get(f"{self.url}/props", timeout=10).json()
        except (httpx.HTTPError, json.JSONDecodeError) as e:
            raise BackendError(f"llama.cpp not answering at {self.url}: {e}") from e


@dataclass
class LlamaCppChat:
    """llama.cpp's own tool-calling path: /v1/chat/completions with `tools`.
    The server renders the model's template and applies a *lazy* grammar,
    built from the tools' schemas and activated only once the model emits
    its tool-call trigger (<tool_call> for Qwen 2.5): calls are constrained,
    the decision to call is not. The reply is rebuilt as text, with each
    call's arguments kept as the raw JSON string the model produced."""
    url: str = "http://127.0.0.1:8083"
    tools: list | None = None
    max_tokens: int = 256
    concurrency: int = 1
    timeout_s: float = 120.0

    async def _one(self, client: httpx.AsyncClient, msgs: list[dict],
                   sem: asyncio.Semaphore) -> str:
        body = {"messages": msgs, "tools": self.tools, "max_tokens": self.max_tokens,
                "temperature": 0.0, "top_k": 1, "seed": 0}
        async with sem:
            r = await client.post(f"{self.url}/v1/chat/completions", json=body)
        if r.status_code != 200:
            raise BackendError(f"llama.cpp HTTP {r.status_code}: {r.text[:200]}")
        msg = r.json()["choices"][0]["message"]
        calls = msg.get("tool_calls") or []
        if not calls:
            return msg.get("content") or ""
        f = calls[0]["function"]
        return ('<tool_call>\n{"name": ' + json.dumps(f["name"]) + ', "arguments": '
                + f["arguments"] + "}\n</tool_call>")

    async def agenerate(self, conversations: list[list[dict]]) -> list[str]:
        sem = asyncio.Semaphore(self.concurrency)
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            return await asyncio.gather(*(self._one(client, m, sem) for m in conversations))

    def generate(self, conversations: list[list[dict]]) -> list[str]:
        return asyncio.run(self.agenerate(conversations))

    def props(self) -> dict:
        return LlamaCpp(self.url).props()
