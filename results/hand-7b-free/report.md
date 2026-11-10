# hand-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 0e81016-dirty · date: 2026-11-10 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.974 [0.923, 1.000] |
| L3 tool | 0.974 [0.923, 1.000] |
| L4 args | 0.872 [0.769, 0.974] |
| abstain | 0.867 [0.667, 1.000] |
| decision | 0.963 [0.907, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.80 |
| crag_search | 8 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 1.00 |
| fs_read | 10 | 0.60 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 0.83 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand-021` fs_read: fails args  | 'read me lines 100 to 120 of logs/2026/server.log' -> '{"name": "fs_read", "arguments": {"limit": 20, "offset": 100, "path": "logs/2026/server.log"}}'
- `test_hand-022` fs_read: fails schema {'path': '/limit', 'keyword': 'minimum', 'message': 'value below minimum'} | 'show the bottom part of notes.txt starting from line 50' -> '{"name": "fs_read", "arguments": {"offset": 50, "limit": -1, "path": "notes.txt"}}'
- `test_hand-026` fs_read: fails args  | 'line 8 of todo-list.txt — what does it say?' -> '{"name": "fs_read", "arguments": {"offset": 8, "path": "todo-list.txt"}}'
- `test_hand-027` fs_read: fails args  | 'dump letters/cover-letter.txt' -> '{"name": "fs_read", "arguments": {"path": "letters/cover-letter.txt", "offset": 1, "limit": 1000}}'
- `test_hand-035` fs_write: fails args  | 'write the following to projects/website/robots.txt: User-agent: *' -> '{"name": "fs_write", "arguments": {"content": "User-agent: *\\n", "path": "projects/website/robots.txt"}}'
- `test_hand-046` unsupported: called '{"name": "fs_read", "arguments": {"path": "shopping.md"}}' | 'rename shopping.md to groceries.md'
- `test_hand-051` ambiguous: called '{"name": "fs_list", "arguments": {"path": "."}}' | "what's in the folder?"
