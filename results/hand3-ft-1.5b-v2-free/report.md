# hand3-ft-1.5b-v2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-6-gc14712e-dirty · date: 2026-11-15 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.971 [0.912, 1.000] |
| L1 json | 0.971 [0.912, 1.000] |
| L2 schema | 0.971 [0.912, 1.000] |
| L3 tool | 0.912 [0.794, 1.000] |
| L4 args | 0.912 [0.794, 1.000] |
| abstain | 0.929 [0.786, 1.000] |
| decision | 0.958 [0.896, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 0.75 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-000` fs_list: fails tool  | 'what does photos contain' -> '{"name": "fs_read", "arguments": {"path": "photos"}}'
- `test_hand3-004` fs_list: fails tool  | 'contents of the receipts folder pls' -> '{"name": "fs_read", "arguments": {"path": "receipts"}}'
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> 'The term "backups" is not a folder or a file. It is an adjective that describes the action of making copies of data to protect against loss.'
- `test_hand3-043` unsupported: called '{"name": "crag_search", "arguments": {"query": "projects/crag"}}' | 'run the tests in projects/crag'
