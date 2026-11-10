import json

from toolcall.evaluate import bootstrap, call_text, rates, score_cases
from toolcall.prompt import call_or_none_schema, load_tools, openai_tools

READ = {"id": "t-1", "split": "test_id", "intent": "fs_read", "family": 0,
        "request": "Read notes/a.md.", "expected": {"name": "fs_read",
                                                     "arguments": {"path": "notes/a.md"}}}
CHAT = {"id": "t-2", "split": "test_id", "intent": "no_tool", "family": 0,
        "request": "Hi!", "expected": None}


def tc(name, **args):
    return "<tool_call>\n" + json.dumps({"name": name, "arguments": args}) + "\n</tool_call>"


def test_constrained_none_is_no_call():
    assert call_text('{"name": "none", "reply": "Hello!"}') is None
    assert call_text(tc("fs_stat", path="a")) is not None
    assert call_text('{"name": "fs_read", "arguments": {broken') is not None   # judged, not dropped


def test_score_cases_and_rates():
    rows = score_cases([READ, CHAT, READ, CHAT],
                       [tc("fs_read", path="notes/a.md"), "Hello there!",
                        tc("fs_read", path="notes/b.md"), tc("crag_stats")])
    assert [r["score"]["called"] for r in rows] == [True, False, True, True]
    m = rates(rows)
    assert m["L3 tool"][0] == 1.0 and m["L4 args"][0] == 0.5
    assert m["abstain"][0] == 0.5 and m["decision"][0] == 0.75
    assert m["n"] == (2, 2)


def test_bootstrap_brackets_the_mean_and_is_seeded():
    xs = [1.0] * 30 + [0.0] * 10
    m, lo, hi = bootstrap(xs, resamples=2000)
    assert lo <= m == 0.75 <= hi and bootstrap(xs, resamples=2000) == (m, lo, hi)
    assert bootstrap([1.0] * 5)[1:] == (1.0, 1.0)


def test_tools_and_constraint_cover_every_tool():
    tools = load_tools()
    assert [t["function"]["name"] for t in openai_tools(tools)] == [t["name"] for t in tools]
    names = [o["properties"]["name"]["const"] for o in call_or_none_schema(tools)["oneOf"]]
    assert names == [t["name"] for t in tools] + ["none"]


def test_report_lists_rates_per_split_and_the_failures():
    from toolcall.evaluate import report

    rows = score_cases([READ, CHAT, READ, CHAT],
                       [tc("fs_read", path="notes/a.md"), "Hello there!",
                        tc("fs_read", path="notes/a.md", limit=0), tc("crag_stats")])
    text = report(rows, {"name": "demo", "model": "m"})
    assert text.startswith("# demo") and "## test_id (2 need a call, 2 need none)" in text
    assert "## test_ood" not in text                      # no rows: no section
    assert "| L4 args | 0.500" in text and "| fs_read | 2 | 0.50 |" in text
    assert "fails schema" in text and "minimum" in text   # the validator's reason is shown
    assert "called" in text and "crag_stats" in text      # a call where none was needed
