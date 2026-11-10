# ft-1.5b-v2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 4150f57-dirty · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.992 [0.975, 1.000] |
| L4 args | 0.975 [0.942, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.994 [0.983, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 0.95 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.95 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which directory should I look in the archive?'
- `test_id-01103` fs_read: fails args  | 'Show research/readme.toml, lines 3 through 7.' -> '{"name": "fs_read", "arguments": {"path": "readme.toml", "offset": 3, "limit": 5}}'
- `test_id-01550` fs_write: fails args  | 'Create drafts/readme.py containing: rerun the benchmark' -> '{"name": "fs_write", "arguments": {"path": "readme.py", "content": "rerun the benchmark"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.963, 1.000] |
| L1 json | 0.984 [0.963, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.947 [0.915, 0.979] |
| L4 args | 0.921 [0.878, 0.958] |
| abstain | 0.990 [0.971, 1.000] |
| decision | 0.986 [0.973, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.97 |
| crag_search | 35 | 0.89 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.74 |
| fs_read | 35 | 0.94 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit", "k": 1}}'
- `test_ood-00335` crag_search: fails args  | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit", "k": 1}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What query should I search the document index with?'
- `test_ood-00353` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit", "k": 1}}'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> 'I can do that once I know more. What specific type of research are you asking about, or what details would help me answer your question?'
- `test_ood-00698` fs_list: fails tool  | 'What does drafts contain?' -> '{"name": "fs_read", "arguments": {"path": "drafts"}}'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-00704` fs_list: fails tool  | 'What does scripts contain?' -> '{"name": "fs_read", "arguments": {"path": "scripts"}}'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'I can do that once I know more. What text file should I read from the documentation?'
- `test_ood-00712` fs_list: fails tool  | 'What does scripts contain? Cheers.' -> '{"name": "fs_read", "arguments": {"path": "scripts"}}'
- `test_ood-00714` fs_list: fails tool  | 'One more thing: What does archive contain?' -> '{"name": "fs_read", "arguments": {"path": "archive"}}'
- `test_ood-00720` fs_list: fails tool  | 'Okay, next: What does scripts contain?' -> '{"name": "fs_read", "arguments": {"path": "scripts"}}'
