# hand-ft-1.5b-v2-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.974 [0.923, 1.000] |
| abstain | 0.867 [0.667, 1.000] |
| decision | 0.963 [0.907, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.60 |
| crag_search | 8 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 1.00 |
| fs_read | 10 | 0.90 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path": "README"}}'
- `test_hand-051` ambiguous: called '{"name": "fs_list", "arguments": {"path": "the folder"}}' | "what's in the folder?"
- `test_hand-053` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the thing we talked about"}}' | 'search for the thing we talked about'
