# hand4-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-11-g3f7fc69 · date: 2026-11-21 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.950 [0.850, 1.000] |
| abstain | 0.550 [0.350, 0.750] |
| decision | 0.775 [0.650, 0.900] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 0.56 |
| crag_search | 5 | 1.00 |
| crag_stats | 2 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 3 | 1.00 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 0.67 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 0.00 |

Failures (first 12):

- `test_hand4-001` ambiguous: called '{"name": "crag_search", "arguments": {"query": "stuff we covered", "k": 5}}' | 'search the knowledge base for the stuff we covered'
- `test_hand4-003` ambiguous: called '{"name": "crag_search", "arguments": {"k": 1, "query": "same thing as before"}}' | 'check the index for the same thing as before. one hit'
- `test_hand4-006` ambiguous: called '{"name": "fs_list", "arguments": {"path": "."}}' | "list what's in there"
- `test_hand4-007` ambiguous: called '{"name": "fs_list", "arguments": {"path": "other"}}' | 'show me the contents of the other directory'
- `test_hand4-009` ambiguous: called '{"name": "fs_write", "arguments": {"content": "TODO: Add your tasks here.", "path": "notes/todo.md"}}' | 'write it to notes/todo.md'
- `test_hand4-010` ambiguous: called '{"name": "fs_write", "arguments": {"content": "<text-to-add>", "path": "journal/today.md"}}' | 'add a line to journal/today.md'
- `test_hand4-011` ambiguous: called '{"name": "fs_write", "arguments": {"content": "pick up the keys", "path": "notes/pick_up_keys.txt"}}' | "save 'pick up the keys' somewhere"
- `test_hand4-028` fs_write: fails args  | "save the line 'v4 ready' into logs/status.txt" -> '{"name": "fs_write", "arguments": {"content": "v4 ready\\n", "path": "logs/status.txt"}}'
- `test_hand4-038` unsupported: called '{"name": "fs_stat", "arguments": {"path": "logs/app.log"}}' | 'delete logs/app.log'
- `test_hand4-039` unsupported: called '{"name": "fs_list", "arguments": {"path": "music"}}' | 'zip up the music folder'
