# dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.975 [0.942, 1.000] |
| L1 json | 0.975 [0.942, 1.000] |
| L2 schema | 0.975 [0.942, 1.000] |
| L3 tool | 0.975 [0.942, 1.000] |
| L4 args | 0.975 [0.942, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.983 [0.961, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.85 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00682` fs_list: fails json no call | "Okay, next: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-00683` fs_list: fails json no call | 'Show me the contents of archive. Please check.' -> 'I can do that once I know more. What should I call the folder?'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.910 [0.868, 0.947] |
| L1 json | 0.910 [0.868, 0.947] |
| L2 schema | 0.910 [0.868, 0.947] |
| L3 tool | 0.910 [0.868, 0.947] |
| L4 args | 0.905 [0.862, 0.942] |
| abstain | 0.990 [0.971, 1.000] |
| decision | 0.939 [0.912, 0.966] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.74 |
| crag_stats | 14 | 0.93 |
| fs_list | 35 | 0.86 |
| fs_read | 35 | 0.97 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.94 |
| no_tool | 35 | 0.97 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00321` crag_search: fails json no call | 'Run a retrieval on the soak test, please.' -> 'I can do that once I know more. What should I search the soak test for?'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'I can do that once I know more. What should the value of n be?'
- `test_ood-00329` crag_search: fails json no call | 'One more thing: Run a retrieval on log redaction, please.' -> 'I can do that once I know more. What should I look up in the docs?'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'I can do that once I know more. What should I search the HNSW index for?'
- `test_ood-00335` crag_search: fails json no call | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00343` crag_search: fails json no call | 'Okay, next: Run a retrieval on the soak test, please.' -> 'I can do that once I know more. What should I search the soak test for?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00478` crag_stats: fails json no call | 'Hey there. Is anything actually indexed right now?' -> 'I can check the index once I know more. Which folder should I look in?'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> "I can't search the docs yet: my tools can only list, read, stat or write files in the sandbox."
- `test_ood-00700` fs_list: fails json no call | 'Hey there. What does the base directory contain?' -> 'I can do that once I know more. Which folder should I look in?'
