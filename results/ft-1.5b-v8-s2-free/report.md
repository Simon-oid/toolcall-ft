# ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.994 [0.983, 1.000] |

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
| unsupported | 20 | 0.95 |

Failures (first 12):

- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.963, 1.000] |
| L1 json | 0.984 [0.963, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.963 [0.937, 0.989] |
| L4 args | 0.963 [0.937, 0.989] |
| abstain | 0.952 [0.905, 0.990] |
| decision | 0.973 [0.952, 0.990] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 0.93 |
| fs_list | 35 | 0.91 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.86 |

Failures (first 12):

- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the docs for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I look up?'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "crag"}}'
- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-00710` fs_list: fails tool  | 'What does research contain? Cheers.' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `test_ood-01947` unsupported: called '{"name": "fs_write", "arguments": {"path": "message.txt", "content": "Dinner is at 7."}}' | 'Text my brother that dinner is at 7. Please check.'
- `test_ood-01949` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/checklist.md"}}' | 'Translate research/checklist.md into German and save it.'
- `test_ood-01958` unsupported: called '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.toml"}}' | 'Translate scripts/notes-2026.toml into German and save it.'
- `test_ood-01959` unsupported: called '{"name": "fs_read", "arguments": {"path": "archive/proposal.toml"}}' | 'Translate archive/proposal.toml into German and save it. Cheers.'
- `test_ood-01962` unsupported: called '{"name": "fs_read", "arguments": {"path": "data/raw/results.toml"}}' | 'Translate data/raw/results.toml into German and save it.'
