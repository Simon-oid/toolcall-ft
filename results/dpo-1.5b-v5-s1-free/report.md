# dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.942 [0.900, 0.983] |
| L1 json | 0.942 [0.900, 0.983] |
| L2 schema | 0.942 [0.900, 0.983] |
| L3 tool | 0.942 [0.900, 0.983] |
| L4 args | 0.942 [0.900, 0.983] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.961 [0.933, 0.989] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 0.95 |
| crag_stats | 20 | 0.90 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.85 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00319` crag_search: fails json no call | 'Can you look up subscriptions in the documentation? Much appreciated.' -> 'Sure, but I need one detail first. Which topic should I search the docs for: subscriptions or subscription?'
- `test_id-00456` crag_stats: fails json no call | 'Hey there. Give me diagnostics on the retrieval database.' -> 'Sure, I can do that once I know more. Which tool should I use?'
- `test_id-00464` crag_stats: fails json no call | 'One more thing: Is the search index empty?' -> 'To check if the index is empty, I can use the `crag_stats` tool. What should the index be called?'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-01546` fs_write: fails json no call | "One more thing: Save the text 'all tests passing' as data/raw/checklist.txt." -> 'I can do that once I know more. Which folder should checklist.txt be saved in?'
- `test_id-01551` fs_write: fails json no call | 'One more thing: Write "budget approved" to archive/invoice.txt.' -> 'Sure, but I need one detail first. What should the file look like? Should it be in all caps or not?'
- `test_id-01558` fs_write: fails json no call | "One more thing: Save the text 'all tests passing' as data/raw/invoice.txt." -> 'I can do that once I know more. Which folder should invoice.txt be saved in?'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.910 [0.868, 0.947] |
| L1 json | 0.910 [0.868, 0.947] |
| L2 schema | 0.910 [0.868, 0.947] |
| L3 tool | 0.910 [0.868, 0.947] |
| L4 args | 0.878 [0.831, 0.921] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.942 [0.915, 0.966] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.74 |
| crag_stats | 14 | 0.86 |
| fs_list | 35 | 0.86 |
| fs_read | 35 | 0.86 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.94 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00321` crag_search: fails json no call | 'Run a retrieval on the soak test, please.' -> 'Sure, but I need one detail first. What should I look up?'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'I can do that once I know more. What should the value of k be?'
- `test_ood-00329` crag_search: fails json no call | 'One more thing: Run a retrieval on log redaction, please.' -> 'Sure, but I need one detail first. What should the query look like?'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'Sure, but I need one detail first. Which folder should I search in?'
- `test_ood-00335` crag_search: fails json no call | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> 'Sure, but I need one detail first. What should I look up?'
- `test_ood-00343` crag_search: fails json no call | 'Okay, next: Run a retrieval on the soak test, please.' -> 'Sure, but I need one detail first. Which document should I search the docs/soak-test folder?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'Sure, but I need one detail first. What should the query be?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I search the docs for?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'Sure, but I need one detail first: what should the query be?'
- `test_ood-00466` crag_stats: fails json no call | 'One more thing: Is anything actually indexed right now?' -> 'I can check. Which tool should I use to do that?'
- `test_ood-00478` crag_stats: fails json no call | 'Hey there. Is anything actually indexed right now?' -> 'I can check the index for you. Which tool should I use to do that?'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> 'I can do that once I know more. Which folder should I look in?'
