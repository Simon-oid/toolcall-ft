# hand-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.692 [0.538, 0.821] |
| L1 json | 0.590 [0.436, 0.744] |
| L2 schema | 0.564 [0.410, 0.718] |
| L3 tool | 0.564 [0.410, 0.718] |
| L4 args | 0.538 [0.385, 0.692] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.778 [0.667, 0.889] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.25 |
| crag_stats | 4 | 0.50 |
| fs_list | 6 | 0.67 |
| fs_read | 10 | 1.00 |
| fs_stat | 5 | 0.40 |
| fs_write | 6 | 0.17 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-000` crag_search: fails json  | "hey, I'm debugging a flaky test — can you check what the docs say about the handler timeout watchdog?" -> '{"name": "crag_search", "arguments": {"query": "the handler timeout watchdog"}}}'
- `test_hand-001` crag_search: fails json no call | "what's the deal with Streamable HTTP in cMCP? look it up" -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "Streamable HTTP in cMCP"}}'
- `test_hand-004` crag_search: fails json no call | 'Does the documentation mention anything about valgrind?' -> '<tool_call>'
- `test_hand-005` crag_search: fails json no call | 'search: json schema subset supported keywords' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "json schema subset supported keywords"}}'
- `test_hand-006` crag_search: fails json no call | 'Can u look up how the elicitation handler works' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "how the elicitation handler works"}}'
- `test_hand-007` crag_search: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_search", "arguments": {"query": "the replay fixtures", "path": "cmcp-tee"}}'
- `test_hand-009` crag_stats: fails json no call | 'how many documents did we index, roughly?' -> '|RF {"name": "crag_stats", "arguments": {}} |'
- `test_hand-010` crag_stats: fails json  | "what's the vector dimension of the embeddings in the index" -> '{"name": "crag_search", "arguments": {"query": "the vector dimension of the embeddings in the index"}};'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-014` fs_list: fails json no call | 'is there anything in the tmp folder?' -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "tmp"}}'
- `test_hand-029` fs_stat: fails json no call | 'when did I last touch recipes/pasta.md?' -> "I can't find a way to know when you last touched recipes/pasta.md. It's not something I can find with the tools I have."
- `test_hand-030` fs_stat: fails json no call | 'is photos/2026 a directory?' -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "photos/2026"}}'
