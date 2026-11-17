# ft-1.5b-v3-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-7-g38cb0d9 · date: 2026-11-15 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.992 [0.975, 1.000] |
| L4 args | 0.992 [0.975, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.994 [0.983, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which file or directory should I look in the archive?'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.989 [0.974, 1.000] |
| L3 tool | 0.974 [0.947, 0.995] |
| L4 args | 0.968 [0.942, 0.989] |
| abstain | 0.971 [0.933, 1.000] |
| decision | 0.983 [0.966, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.94 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.91 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.97 |

Failures (first 12):

- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'I can do that once I know more. Which tool should I use to run the retrieval?'
- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What query should I run the search on?'
- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "fs_read", "arguments": {"path": "research"}}'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "fs_read", "arguments": {"path": "research"}}'
- `test_ood-00710` fs_list: fails tool  | 'What does research contain? Cheers.' -> '{"name": "fs_read", "arguments": {"path": "research"}}'
- `test_ood-01947` unsupported: called '{"name": "fs_read", "arguments": {"path": "text.txt"}}' | 'Text my brother that dinner is at 7. Please check.'
- `test_ood-02120` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/outline.toml", "content": "This is the content of the outline file."' | 'Fill archive/outline.toml in.'
- `test_ood-02131` ambiguous: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.txt"}}' | 'Fill research/notes-2026.txt in. Please check.'
