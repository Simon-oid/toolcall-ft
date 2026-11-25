# dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.975 [0.942, 1.000] |
| L1 json | 0.975 [0.942, 1.000] |
| L2 schema | 0.867 [0.800, 0.925] |
| L3 tool | 0.667 [0.583, 0.750] |
| L4 args | 0.658 [0.575, 0.742] |
| abstain | 0.883 [0.800, 0.950] |
| decision | 0.944 [0.911, 0.972] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 0.40 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.30 |
| fs_read | 20 | 0.65 |
| fs_stat | 20 | 0.90 |
| fs_write | 20 | 0.70 |
| no_tool | 20 | 0.95 |
| unsupported | 20 | 0.70 |

Failures (first 12):

- `test_id-00300` crag_search: fails tool  | 'Search the docs for subscriptions.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00302` crag_search: fails tool  | 'Find me the passages about subscriptions.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00303` crag_search: fails tool  | 'Hey there. What does the index say about the soak test?' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00306` crag_search: fails tool  | 'Search the docs for the soak test. Just the top 10 hits. Cheers.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00308` crag_search: fails tool  | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00309` crag_search: fails tool  | 'Okay, next: What does the index say about log redaction? Just the top 2 hits.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00310` crag_search: fails tool  | 'I need info on the soak test; check the knowledge base. Just the single best hit.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00312` crag_search: fails tool  | 'Search the docs for the soak test. Just the top 2 hits.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00314` crag_search: fails tool  | 'Find me the passages about log redaction.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00316` crag_search: fails tool  | 'Hey there. I need info on the HNSW index; check the knowledge base. Give me 10 results.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00318` crag_search: fails tool  | 'Search the docs for nDCG evaluation. Just the top 10 hits.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_id-00319` crag_search: fails tool  | 'Can you look up subscriptions in the documentation? Much appreciated.' -> '{"name": "crag_stats", "arguments": {}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.974 [0.947, 0.995] |
| L1 json | 0.958 [0.926, 0.984] |
| L2 schema | 0.788 [0.730, 0.847] |
| L3 tool | 0.603 [0.534, 0.672] |
| L4 args | 0.587 [0.519, 0.656] |
| abstain | 0.943 [0.895, 0.981] |
| decision | 0.963 [0.939, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.31 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.29 |
| fs_read | 35 | 0.54 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.63 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.83 |

Failures (first 12):

- `test_ood-00321` crag_search: fails tool  | 'Run a retrieval on the soak test, please.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00322` crag_search: fails tool  | 'Okay, next: Pull up whatever the corpus has regarding cancellation of requests. Just the top 3 hits.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00323` crag_search: fails tool  | 'Run a retrieval on the SSRF egress guard, please.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'What should the maximum number of results be?'
- `test_ood-00326` crag_search: fails tool  | 'Hey there. Pull up whatever the corpus has regarding the soak test.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00328` crag_search: fails tool  | 'One more thing: Pull up whatever the corpus has regarding cancellation of requests. Just the top 2 hits.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00330` crag_search: fails tool  | 'One more thing: Pull up whatever the corpus has regarding the HNSW index.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should the search query be?'
- `test_ood-00333` crag_search: fails tool  | 'Hey there. Run a retrieval on the soak test, please. Give me 2 results.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00334` crag_search: fails tool  | 'Pull up whatever the corpus has regarding cancellation of requests.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00335` crag_search: fails tool  | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00336` crag_search: fails tool  | 'Pull up whatever the corpus has regarding nDCG evaluation. Just the single best hit.' -> '{"name": "crag_stats", "arguments": {}}'
