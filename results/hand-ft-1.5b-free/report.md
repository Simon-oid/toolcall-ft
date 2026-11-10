# hand-ft-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 0e81016-dirty · date: 2026-11-10 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.897 [0.795, 0.974] |
| abstain | 0.933 [0.800, 1.000] |
| decision | 0.981 [0.944, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.80 |
| crag_search | 8 | 0.75 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 1.00 |
| fs_read | 10 | 0.80 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-005` crag_search: fails args  | 'search: json schema subset supported keywords' -> '{"name": "crag_search", "arguments": {"query": "supported keywords"}}'
- `test_hand-007` crag_search: fails args  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_search", "arguments": {"query": "the replay fixtures are captured"}}'
- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path": "README"}}'
- `test_hand-026` fs_read: fails args  | 'line 8 of todo-list.txt — what does it say?' -> '{"name": "fs_read", "arguments": {"path": "todo-list.txt", "offset": 8}}'
- `test_hand-051` ambiguous: called '{"name": "fs_list", "arguments": {"path": "the folder"}}' | "what's in the folder?"
