# hand-dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.897 [0.795, 0.974] |
| abstain | 0.733 [0.467, 0.933] |
| decision | 0.926 [0.852, 0.981] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.88 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.80 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.20 |

Failures (first 12):

- `test_hand-007` crag_search: fails args  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_search", "arguments": {"query": "the replay fixtures are captured"}}'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-021` fs_read: fails args  | 'read me lines 100 to 120 of logs/2026/server.log' -> '{"name": "fs_read", "arguments": {"path": "logs/2026/server.log", "offset": 100, "limit": 31}}'
- `test_hand-022` fs_read: fails args  | 'show the bottom part of notes.txt starting from line 50' -> '{"name": "fs_read", "arguments": {"path": "notes.txt", "offset": 50, "limit": 10}}'
- `test_hand-044` unsupported: called '{"name": "fs_delete", "arguments": {"path": "reminders.txt"}}' | "delete reminders.txt, I don't need it anymore"
- `test_hand-046` unsupported: called '{"name": "fs_rename", "arguments": {"oldPath": "shopping.md", "newPath": "groceries.md"}}' | 'rename shopping.md to groceries.md'
- `test_hand-047` unsupported: called '{"name": "fs_read", "arguments": {"path": "deploy.sh"}}' | 'run deploy.sh for me'
- `test_hand-048` unsupported: called '{"name": "crag_rebuild", "arguments": {"model_name": "newer_model"}}' | 're-embed all documents with a newer model'
