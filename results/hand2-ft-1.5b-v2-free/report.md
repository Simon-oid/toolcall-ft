# hand2-ft-1.5b-v2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 4150f57-dirty · date: 2026-11-10 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.969 [0.906, 1.000] |
| L1 json | 0.969 [0.906, 1.000] |
| L2 schema | 0.969 [0.906, 1.000] |
| L3 tool | 0.938 [0.844, 1.000] |
| L4 args | 0.906 [0.812, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.979 [0.938, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 0.80 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand2-010` fs_list: fails tool  | "what's in invoices/2025?" -> '{"name": "fs_read", "arguments": {"path": "invoices/2025"}}'
- `test_hand2-017` fs_read: fails args  | 'what does the first line of exports/summary.txt say?' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt"}}'
- `test_hand2-025` fs_stat: fails json no call | 'is exports a file or a folder?' -> '_exports is not a file or a folder. It is an export statement in JavaScript, which is used to define and export variables, functions, or cla'
