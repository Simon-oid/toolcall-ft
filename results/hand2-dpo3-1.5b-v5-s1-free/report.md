# hand2-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.812 [0.656, 0.938] |
| L1 json | 0.750 [0.594, 0.906] |
| L2 schema | 0.719 [0.562, 0.875] |
| L3 tool | 0.719 [0.562, 0.875] |
| L4 args | 0.719 [0.562, 0.875] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.875 [0.771, 0.958] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 0.33 |
| crag_stats | 4 | 0.75 |
| fs_list | 5 | 0.80 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 0.80 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand2-000` crag_search: fails json no call | 'my boss asked how the server deals with request cancellation, can you find that in the docs' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the server deals with request cancellation"}}'
- `test_hand2-001` crag_search: fails json no call | 'look for anything about SQLite FTS5 in the knowledge base' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "SQLite FTS5"}}'
- `test_hand2-003` crag_search: fails json no call | 'Find documentation on the worker pool size setting.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the worker pool size setting"}}'
- `test_hand2-004` crag_search: fails json no call | 'query the docs: TypeScript SDK benchmark' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "TypeScript SDK benchmark"}}'
- `test_hand2-006` crag_stats: fails json  | 'how big is the search index right now, in chunks?' -> '{"name": "crag_stats", "arguments": {"query": "the search index, in chunks"}};'
- `test_hand2-010` fs_list: fails json no call | "what's in invoices/2025?" -> '<tool_call>\n{"name": "fs_read", "arguments": {"path": "invoices/2025"}}'
- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt", "offset": 40, "limit": null}}'
- `test_hand2-025` fs_stat: fails json no call | 'is exports a file or a folder?' -> '<tool_call>'
- `test_hand2-027` fs_write: fails json  | "write 'flight at 7:40' to travel/notes.txt" -> '{"name": "fs_write", "arguments": {"path": "travel/notes.txt", "content": "flight at 7:40"}}}'
