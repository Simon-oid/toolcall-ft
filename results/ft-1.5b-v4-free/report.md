# ft-1.5b-v4-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v4-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-11-g3f7fc69 · date: 2026-11-21 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):


## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.958 [0.926, 0.984] |
| L1 json | 0.958 [0.926, 0.984] |
| L2 schema | 0.958 [0.926, 0.984] |
| L3 tool | 0.958 [0.926, 0.984] |
| L4 args | 0.958 [0.926, 0.984] |
| abstain | 0.981 [0.952, 1.000] |
| decision | 0.966 [0.942, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.94 |
| crag_search | 35 | 0.77 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00321` crag_search: fails json no call | 'Run a retrieval on the soak test, please.' -> 'I can do that once I know more. What should I look up?'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'I can do that once I know more. What should the query be? And how many results should I get?'
- `test_ood-00329` crag_search: fails json no call | 'One more thing: Run a retrieval on log redaction, please.' -> 'I can do that once I know more. What should the query be?'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-00343` crag_search: fails json no call | 'Okay, next: Run a retrieval on the soak test, please.' -> 'I can do that once I know more. What should I look up?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I look up?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I look up?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-02141` ambiguous: called '{"name": "fs_stat", "arguments": {"path": "document"}}' | 'Check how large the document is. Cheers.'
- `test_ood-02148` ambiguous: called '{"name": "fs_stat", "arguments": {"path": "document"}}' | 'Check how large the document is. Please check.'
