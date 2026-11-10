import json

import pytest

from toolcall.judge import judge
from toolcall.score import CaseError, extract_call, parse_expected, score


def call(name, **arguments):
    return json.dumps({"name": name, "arguments": arguments})


def run(expected, text):
    exp = parse_expected(expected)
    call_text = extract_call(text)
    verdict = judge([call_text])[0] if call_text is not None else None
    return score(exp, call_text, verdict)


READ = {"name": "fs_read", "arguments": {"path": "notes.md", "limit": 20}}


class TestExtract:
    def test_tool_call_markup(self):
        assert extract_call('ok <tool_call>\n{"name": "x"}\n</tool_call>') == '{"name": "x"}'

    def test_bare_json_call(self):
        assert extract_call(' {"name": "x", "arguments": {}} ') == '{"name": "x", "arguments": {}}'

    def test_prose_is_no_call(self):
        assert extract_call("Which file do you mean?") is None


class TestLevels:
    def test_right_call_passes_all_four(self):
        s = run(READ, f"<tool_call>{call('fs_read', path='notes.md', limit=20)}</tool_call>")
        assert s.levels == {"json": True, "schema": True, "tool": True, "args": True}

    def test_broken_json_fails_everything(self):
        s = run(READ, '<tool_call>{"name": "fs_read", "arguments": {path: 1}}</tool_call>')
        assert s.levels == {"json": False, "schema": False, "tool": False, "args": False}

    def test_schema_violation_stops_at_level_one(self):
        s = run(READ, f"<tool_call>{call('fs_read', path='notes.md', limit=0)}</tool_call>")
        assert s.levels["json"] and not s.levels["schema"]
        assert s.error["keyword"] == "minimum"

    def test_wrong_tool(self):
        s = run(READ, f"<tool_call>{call('fs_stat', path='notes.md')}</tool_call>")
        assert s.levels["schema"] and not s.levels["tool"]

    def test_wrong_argument_value(self):
        s = run(READ, f"<tool_call>{call('fs_read', path='notes.md', limit=10)}</tool_call>")
        assert s.levels["tool"] and not s.levels["args"]

    def test_integer_is_not_float_or_bool(self):
        exp = {"name": "fs_read", "arguments": {"path": "a", "limit": 1}}
        assert not run(exp, call("fs_read", path="a", limit=True)).levels["args"]

    def test_no_call_when_one_was_expected(self):
        s = run(READ, "I'll read it for you.")
        assert not s.called and not any(s.levels.values())


class TestArgumentRules:
    def test_optional_argument_may_be_left_out(self):
        exp = {"name": "crag_search", "arguments": {"query": {"contains_all": ["bm25"]}, "k": 5},
               "optional": ["k"]}
        assert run(exp, call("crag_search", query="BM25 parameters")).levels["args"]
        assert not run(exp, call("crag_search", query="BM25", k=3)).levels["args"]

    def test_contains_all_is_case_insensitive_and_needs_every_word(self):
        exp = {"name": "crag_search", "arguments": {"query": {"contains_all": ["rrf", "k"]}}}
        assert run(exp, call("crag_search", query="RRF k constant")).levels["args"]
        assert not run(exp, call("crag_search", query="fusion")).levels["args"]

    def test_any_of(self):
        exp = {"name": "fs_list", "arguments": {"path": {"any_of": ["", "."]}}}
        assert run(exp, call("fs_list", path=".")).levels["args"]

    def test_unrequested_argument_fails(self):
        exp = {"name": "fs_read", "arguments": {"path": "a"}}
        assert not run(exp, call("fs_read", path="a", offset=3)).levels["args"]

    def test_bad_specs_are_rejected(self):
        with pytest.raises(CaseError):
            parse_expected({"name": "x", "arguments": {"a": {"any_of": []}}})
        with pytest.raises(CaseError):
            parse_expected({"name": "x", "arguments": {}, "optional": ["a"]})


class TestAbstain:
    def test_abstaining_on_a_no_tool_case(self):
        s = run(None, "MCP is a protocol for tools.")
        assert s.abstained_ok and s.levels is None

    def test_calling_on_a_no_tool_case_is_wrong(self):
        assert not run(None, f"<tool_call>{call('crag_stats')}</tool_call>").abstained_ok


def test_judge_batch_keeps_order():
    vs = judge([call("crag_stats"), "nope", call("rm", x=1)])
    assert [v["json"] for v in vs] == [True, False, True]
    assert [v["known"] for v in vs] == [True, False, False]
