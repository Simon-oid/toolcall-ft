# ft-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.992 [0.975, 1.000] |
| L4 args | 0.992 [0.975, 1.000] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.989 [0.972, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 0.95 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-01761` no_tool: called '{"name": "crag_search", "arguments": {"query": "2 to the power of 10"}}' | 'What is 2 to the power of 10? Please check.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.974 [0.947, 0.995] |
| L1 json | 0.974 [0.947, 0.995] |
| L2 schema | 0.974 [0.947, 0.995] |
| L3 tool | 0.958 [0.926, 0.984] |
| L4 args | 0.947 [0.915, 0.979] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.983 [0.966, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.86 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.91 |
| fs_read | 35 | 0.94 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'I can do that once I know more. What should the maximum number of chunks be?'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I search the docs for?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-00710` fs_list: fails tool  | 'What does research contain? Cheers.' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-01126` fs_read: fails args  | 'Resume research/invoice.toml from line 5.' -> '{"name": "fs_read", "arguments": {"path": "invoice.toml", "offset": 5}}'
- `test_ood-01127` fs_read: fails args  | 'Peek at drafts/notes-2026.txt: 5 lines from the start.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.txt", "offset": 1}}'
