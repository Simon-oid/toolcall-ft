"""Scoring a model's tool call on four levels.

  1 json     the call parses to {"name": str, "arguments": object}
  2 schema   the tool exists and the arguments pass its inputSchema
  3 tool     it is the tool the case expects
  4 args     the arguments match the expected ones, argument by argument

Levels 1 and 2 are decided by cMCP's own parser and JSON Schema
validator (judge/judge, see judge.py): the code a real server runs on
tools/call, not a Python reimplementation that could disagree with it.
Levels 3 and 4 compare with the case's expected call. Each level counts
only if the ones before it passed, so level 4 is "the call is right".

A case may expect no call at all (chit-chat, or a request too ambiguous
to act on without asking): then the only question is whether the model
abstained, and the four levels do not apply.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# Hermes / Qwen 2.5 tool-call markup: <tool_call>{...}</tool_call>
_TOOL_CALL = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.S)
LEVELS = ("json", "schema", "tool", "args")


class CaseError(ValueError):
    pass


@dataclass(frozen=True)
class ArgRule:
    """How one expected argument is matched.

    exact         equal as JSON values (1 and 1.0 differ: the schema says integer)
    any_of        equal to one of `values`
    contains_all  a string containing every word of `values`, case-insensitive:
                  for free text such as a search query, which has no single
                  right spelling but must carry what the user asked about
    """
    kind: str
    values: tuple

    def matches(self, got: object) -> bool:
        if self.kind == "exact":
            return _same(got, self.values[0])
        if self.kind == "any_of":
            return any(_same(got, v) for v in self.values)
        if self.kind == "contains_all":
            return isinstance(got, str) and all(w.lower() in got.lower() for w in self.values)
        raise CaseError(f"unknown rule {self.kind}")


def _same(a: Any, b: Any) -> bool:
    """JSON equality that keeps bool, int and float apart (True == 1 in Python)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b, strict=True))
    return a == b


@dataclass(frozen=True)
class Expected:
    name: str
    args: dict[str, ArgRule]
    # Optional arguments the model may add or leave out: their absence is
    # never wrong (the server applies its default), a wrong value still is.
    optional: frozenset[str] = field(default_factory=frozenset)

    def args_match(self, got: dict) -> bool:
        required = self.args.keys() - self.optional
        if not required <= got.keys():
            return False
        if got.keys() - self.args.keys():
            return False              # an argument the request did not ask for
        return all(self.args[k].matches(v) for k, v in got.items())


def parse_rule(spec: object) -> ArgRule:
    """`5` / `"a.md"` -> exact; {"any_of": [...]} ; {"contains_all": [...]}."""
    if isinstance(spec, dict) and len(spec) == 1:
        (kind, values), = spec.items()
        if kind in ("any_of", "contains_all"):
            if not isinstance(values, list) or not values:
                raise CaseError(f"{kind} needs a non-empty list")
            return ArgRule(kind, tuple(values))
    return ArgRule("exact", (spec,))


def parse_expected(spec: dict | None) -> Expected | None:
    if spec is None:
        return None
    if not isinstance(spec.get("name"), str) or not isinstance(spec.get("arguments", {}), dict):
        raise CaseError(f"bad expected call: {spec!r}")
    args = {k: parse_rule(v) for k, v in spec.get("arguments", {}).items()}
    optional = frozenset(spec.get("optional", ()))
    if not optional <= args.keys():
        raise CaseError(f"optional names unknown arguments: {sorted(optional - args.keys())}")
    return Expected(spec["name"], args, optional)


def extract_call(text: str) -> str | None:
    """The call text a model emitted, or None if it made no call.

    The first <tool_call> block if there is one; otherwise the whole reply
    when it looks like a bare JSON call (some models skip the markup). A
    reply in prose is no call: that is how a model abstains or asks."""
    m = _TOOL_CALL.search(text)
    if m:
        return m.group(1)
    stripped = text.strip()
    if stripped.startswith("{") and '"name"' in stripped:
        return stripped
    return None


@dataclass(frozen=True)
class Score:
    called: bool
    levels: dict[str, bool] | None     # None when the case expects no call
    abstained_ok: bool | None          # None when the case expects a call
    error: dict | None = None          # the validator's reason, for level 2


def score(expected: Expected | None, call_text: str | None, verdict: dict | None) -> Score:
    """`verdict` is the judge's line for `call_text` (None when there is no call)."""
    if expected is None:
        return Score(call_text is not None, None, call_text is None)
    if call_text is None:
        return Score(False, dict.fromkeys(LEVELS, False), None)
    if verdict is None:
        raise ValueError("a call needs the judge's verdict")
    ok_json = verdict["json"]
    ok_schema = ok_json and verdict["schema"]
    ok_tool = ok_schema and verdict["name"] == expected.name
    ok_args = ok_tool and expected.args_match(json.loads(call_text)["arguments"])
    levels = {"json": ok_json, "schema": ok_schema, "tool": ok_tool, "args": ok_args}
    return Score(True, levels, None, verdict.get("error"))
