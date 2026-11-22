# hand-ft-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.974 [0.923, 1.000] |
| L4 args | 0.923 [0.821, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.90 |
| fs_stat | 5 | 0.80 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path": "README"}}'
- `test_hand-030` fs_stat: fails tool  | 'is photos/2026 a directory?' -> '{"name": "fs_list", "arguments": {"path": "photos/2026"}}'
