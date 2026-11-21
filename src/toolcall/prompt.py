"""The prompt every model sees: our system text, the six tools, the request.

Rendered by the model's own chat template (Hugging Face), so the tools
reach the model in the format it was trained on (Qwen 2.5: a <tools>
block in the system message and <tool_call> markup for calls), and the
same rendering serves training, evaluation and serving."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from .data import SYSTEM
from .judge import TOOLS


def load_tools(path: Path = TOOLS) -> list[dict]:
    return json.loads(path.read_text())["tools"]


def openai_tools(tools: list[dict]) -> list[dict]:
    """Tools in the function-calling format chat templates expect."""
    return [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                              "parameters": t["inputSchema"]}} for t in tools]


def messages(request: str) -> list[dict]:
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": request}]


def case_messages(case: dict) -> list[dict]:
    """Our system text, then the case's conversation: the request alone, or
    an episode's history up to the turn being scored (episodes.py)."""
    if "context" not in case:
        return messages(case["request"])
    return [{"role": "system", "content": SYSTEM}, *case["context"]]


def openai_messages(msgs: list[dict]) -> list[dict]:
    """The same conversation in the OpenAI wire format that /v1/chat/completions
    and hosted APIs take: call arguments as a JSON string, calls and results
    paired by id. (Hugging Face templates take the arguments as an object.)"""
    out: list[dict] = []
    n = 0
    for m in msgs:
        if m["role"] == "assistant" and m.get("tool_calls"):
            calls = []
            for c in m["tool_calls"]:
                n += 1
                calls.append({"id": f"call_{n}", "type": "function",
                              "function": {"name": c["function"]["name"],
                                           "arguments": json.dumps(c["function"]["arguments"])}})
            out.append({"role": "assistant", "content": m.get("content") or None,
                        "tool_calls": calls})
        elif m["role"] == "tool":
            out.append({"role": "tool", "tool_call_id": f"call_{n}", "content": m["content"]})
        else:
            out.append(dict(m))
    return out


@cache
def tokenizer(model: str):
    from transformers import AutoTokenizer  # heavy import, only where prompts are built
    return AutoTokenizer.from_pretrained(model)


def render_messages(msgs: list[dict], model: str, tools: list[dict]) -> str:
    """The prompt text up to the assistant's turn."""
    return tokenizer(model).apply_chat_template(
        msgs, tools=openai_tools(tools), add_generation_prompt=True, tokenize=False)


def render(request: str, model: str, tools: list[dict]) -> str:
    return render_messages(messages(request), model, tools)


def render_case(case: dict, model: str, tools: list[dict]) -> str:
    return render_messages(case_messages(case), model, tools)


def call_or_none_schema(tools: list[dict]) -> dict:
    """For constrained decoding: the reply must be a call to one of the
    tools, with arguments valid for its schema, or an explicit no-call
    {"name": "none", "reply": ...}, so abstaining stays possible."""
    calls = [{"type": "object", "additionalProperties": False, "required": ["name", "arguments"],
              "properties": {"name": {"const": t["name"]}, "arguments": t["inputSchema"]}}
             for t in tools]
    none = {"type": "object", "additionalProperties": False, "required": ["name", "reply"],
            "properties": {"name": {"const": "none"}, "reply": {"type": "string"}}}
    return {"oneOf": [*calls, none]}
