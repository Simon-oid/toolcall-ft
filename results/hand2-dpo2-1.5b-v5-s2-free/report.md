# hand2-dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.969 [0.906, 1.000] |
| L3 tool | 0.969 [0.906, 1.000] |
| L4 args | 0.969 [0.906, 1.000] |
| abstain | 0.938 [0.812, 1.000] |
| decision | 0.979 [0.938, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 1.00 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt", "offset": 40, "limit": null}}'
- `test_hand2-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "exports"}}' | 'zip the exports folder'
