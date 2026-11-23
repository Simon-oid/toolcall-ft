# ft-1.5b-v6-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.975 [0.942, 1.000] |
| L1 json | 0.975 [0.942, 1.000] |
| L2 schema | 0.975 [0.942, 1.000] |
| L3 tool | 0.975 [0.942, 1.000] |
| L4 args | 0.975 [0.942, 1.000] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.978 [0.956, 0.994] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.85 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 0.95 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00682` fs_list: fails json no call | "Okay, next: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-00683` fs_list: fails json no call | 'Show me the contents of archive. Please check.' -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-01761` no_tool: called '{"name": "crag_search", "arguments": {"query": "2 to the power of 10"}}' | 'What is 2 to the power of 10? Please check.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.979 [0.958, 0.995] |
| L1 json | 0.979 [0.958, 0.995] |
| L2 schema | 0.979 [0.958, 0.995] |
| L3 tool | 0.979 [0.958, 0.995] |
| L4 args | 0.968 [0.942, 0.989] |
| abstain | 0.990 [0.971, 1.000] |
| decision | 0.983 [0.966, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.89 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 0.94 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 0.97 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should I search the docs for?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'I can do that once I know more. What should I search the documentation for?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-01109` fs_read: fails args  | 'Peek at data/raw/agenda.py: 5 lines from the start.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda.py", "offset": 5}}'
- `test_ood-01125` fs_read: fails args  | 'Peek at archive/invoice.md: 5 lines from the start. Cheers.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice.md", "offset": 1, "limit": 6}}'
- `test_ood-01790` no_tool: called '{"name": "crag_search", "arguments": {"query": "orange"}}' | "What rhymes with 'orange'? Please check."
