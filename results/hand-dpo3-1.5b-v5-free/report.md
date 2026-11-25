# hand-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.974 [0.923, 1.000] |
| L2 schema | 0.872 [0.769, 0.974] |
| L3 tool | 0.615 [0.462, 0.769] |
| L4 args | 0.590 [0.436, 0.744] |
| abstain | 0.933 [0.800, 1.000] |
| decision | 0.981 [0.944, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.38 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 0.67 |
| fs_read | 10 | 0.40 |
| fs_stat | 5 | 0.80 |
| fs_write | 6 | 0.67 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand-002` crag_search: fails tool  | 'pls find stuff on the token bucket at the HTTP acceptor, top 3' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand-003` crag_search: fails tool  | "I'm writing a report on hybrid search. Grab me the 10 most relevant chunks about BM25 vs cosine fusion." -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand-004` crag_search: fails json  | 'Does the documentation mention anything about valgrind?' -> '{"name": "crag_stats", "arguments": {}'
- `test_hand-005` crag_search: fails tool  | 'search: json schema subset supported keywords' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand-007` crag_search: fails tool  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-013` fs_list: fails schema  | "show me what's under projects/website" -> '{"name": "projects/website", "arguments": {}}'
- `test_hand-021` fs_read: fails tool  | 'read me lines 100 to 120 of logs/2026/server.log' -> '{"name": "fs_stat", "arguments": {"path": "logs/2026/server.log"}}'
- `test_hand-022` fs_read: fails tool  | 'show the bottom part of notes.txt starting from line 50' -> '{"name": "fs_stat", "arguments": {"path": "notes.txt"}}'
- `test_hand-023` fs_read: fails tool  | 'cat backup/config.ini' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand-025` fs_read: fails tool  | 'skim the first 3 lines of README' -> '{"name": "fs_stat", "arguments": {"path": "README"}}'
- `test_hand-026` fs_read: fails tool  | 'line 8 of todo-list.txt — what does it say?' -> '{"name": "fs_stat", "arguments": {"path": "todo-list.txt"}}'
