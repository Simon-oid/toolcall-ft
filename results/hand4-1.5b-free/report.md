# hand4-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-11-g3f7fc69 · date: 2026-11-21 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.900 [0.750, 1.000] |
| L4 args | 0.800 [0.600, 0.950] |
| abstain | 0.600 [0.400, 0.800] |
| decision | 0.800 [0.675, 0.925] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 0.50 |
| crag_search | 5 | 1.00 |
| crag_stats | 2 | 1.00 |
| fs_list | 5 | 0.80 |
| fs_read | 3 | 0.00 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand4-000` ambiguous: called '{"name": "fs_read", "arguments": {"path": "docs/docs.md", "limit": null, "offset": null}}' | 'grab the bit about it from the docs'
- `test_hand4-001` ambiguous: called '{"name": "crag_search", "arguments": {"query": "stuff we covered", "k": 5}}' | 'search the knowledge base for the stuff we covered'
- `test_hand4-002` ambiguous: called '{"name": "crag_search", "arguments": {"query": "top 2", "k": 2}}' | 'look that up for me, top 2'
- `test_hand4-003` ambiguous: called '{"name": "crag_search", "arguments": {"query": "same thing as before", "k": 1}}' | 'check the index for the same thing as before. one hit'
- `test_hand4-004` ambiguous: called '{"name": "crag_search", "arguments": {"query": "last time", "k": 5}}' | 'pull up whatever we found last time'
- `test_hand4-005` ambiguous: called '{"name": "fs_list", "arguments": {"path": "folder_path"}}' | "what's inside that folder?"
- `test_hand4-006` ambiguous: called '{"name": "fs_list", "arguments": {"path": "/"}}' | "list what's in there"
- `test_hand4-011` ambiguous: called '{"name": "crag_search", "arguments": {"query": "save \'pick up the keys\' somewhere", "k": 5}}' | "save 'pick up the keys' somewhere"
- `test_hand4-016` fs_list: fails args  | "what's in invoices" -> '{"name": "fs_list", "arguments": {"path": "/invoices"}}'
- `test_hand4-029` fs_read: fails args  | 'cat config/settings.toml' -> '{"name": "fs_read", "arguments": {"path": "config/settings.toml", "offset": 1, "limit": 10}}'
- `test_hand4-030` fs_read: fails tool  | 'first 5 lines of logs/app.log' -> '{"name": "fs_list", "arguments": {"path": "logs/app.log"}}'
- `test_hand4-031` fs_read: fails tool  | 'show me journal/monday.md' -> '{"name": "fs_list", "arguments": {"path": "journal/monday.md"}}'
