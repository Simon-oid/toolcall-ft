# hand-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.949 [0.872, 1.000] |
| L2 schema | 0.923 [0.821, 1.000] |
| L3 tool | 0.897 [0.795, 0.974] |
| L4 args | 0.872 [0.769, 0.974] |
| abstain | 0.200 [0.000, 0.400] |
| decision | 0.778 [0.667, 0.889] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.00 |
| crag_search | 8 | 0.88 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.80 |
| fs_stat | 5 | 0.80 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 0.60 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand-002` crag_search: fails json  | 'pls find stuff on the token bucket at the HTTP acceptor, top 3' -> '{"name": "fs_list", "arguments": {"path": "the HTTP acceptor", "query": "the token bucket", "k": 3}'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-022` fs_read: fails schema {'path': '/limit', 'keyword': 'minimum', 'message': 'value below minimum'} | 'show the bottom part of notes.txt starting from line 50' -> '{"name": "fs_read", "arguments": {"path": "notes.txt", "offset": 50, "limit": -1}}'
- `test_hand-026` fs_read: fails json  | 'line 8 of todo-list.txt — what does it say?' -> '{"name": "fs_read", "arguments": {"path": "todo-list.txt", "offset": 8, limit: 1}}'
- `test_hand-030` fs_stat: fails tool  | 'is photos/2026 a directory?' -> '{"name": "fs_list", "arguments": {"path": "photos/2026"}}'
- `test_hand-040` no_tool: called '{"name": "crag_search", "arguments": {"query": "binary search time complexity"}}' | "what's the time complexity of binary search?"
- `test_hand-043` no_tool: called '{"name": "crag_search", "arguments": {"query": "good morning :)"}}' | 'good morning :)'
- `test_hand-044` unsupported: called '{"name": "fs_delete", "arguments": {"path": "reminders.txt"}}' | "delete reminders.txt, I don't need it anymore"
- `test_hand-045` unsupported: called '{"name": "fs_write", "arguments": {"path": "cover_letter.txt", "content": "the cover letter text here"}}' | 'email the cover letter to hr@example.com'
- `test_hand-046` unsupported: called '{"name": "fs_rename", "arguments": {"oldPath": "shopping.md", "newPath": "groceries.md"}}' | 'rename shopping.md to groceries.md'
- `test_hand-047` unsupported: called '{"name": "fs_read", "arguments": {"path": "deploy.sh"}}' | 'run deploy.sh for me'
- `test_hand-048` unsupported: called '{"name": "crag_stats", "arguments": {}}' | 're-embed all documents with a newer model'
