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


@cache
def tokenizer(model: str):
    from transformers import AutoTokenizer  # heavy import, only where prompts are built
    return AutoTokenizer.from_pretrained(model)


def render(request: str, model: str, tools: list[dict]) -> str:
    """The prompt text up to the assistant's turn."""
    return tokenizer(model).apply_chat_template(
        messages(request), tools=openai_tools(tools), add_generation_prompt=True, tokenize=False)


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
