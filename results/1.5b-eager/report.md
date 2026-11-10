# 1.5b-eager

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: whole reply constrained to a valid call or {name: none} (eager) · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.942 [0.900, 0.983] |
| L4 args | 0.767 [0.692, 0.842] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.667 [0.600, 0.733] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 0.85 |
| fs_list | 20 | 0.75 |
| fs_read | 20 | 0.20 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.80 |
| no_tool | 20 | 0.00 |
| unsupported | 20 | 0.00 |

Failures (first 12):

- `test_id-00448` crag_stats: fails tool  | 'What embedding dimension does the index use?' -> '{"name": "fs_stat", "arguments": {"path": "index/embedding_dimension"}}'
- `test_id-00454` crag_stats: fails tool  | 'What embedding dimension does the index use? Please check.' -> '{"name": "fs_stat", "arguments": {"path": "index/embedding_dimension"}}'
- `test_id-00460` crag_stats: fails tool  | 'Okay, next: What embedding dimension does the index use?' -> '{"name": "fs_stat", "arguments": {"path": "index/cRAG/emb_dim"}}'
- `test_id-00673` fs_list: fails args  | 'One more thing: Which files are under the base directory?' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00674` fs_list: fails args  | 'Enumerate the entries of the base directory.' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00675` fs_list: fails args  | 'List the files in the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00684` fs_list: fails args  | 'Okay, next: ls the base directory' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00688` fs_list: fails args  | "One more thing: What's inside archive?" -> '{"name": "fs_list", "arguments": {"path": "/path/to/archive"}}'
- `test_id-01084` fs_read: fails args  | 'Read lines 40 to 44 of archive/checklist.md.' -> '{"name": "fs_read", "arguments": {"path": "archive/checklist.md", "limit": 4, "offset": 40}}'
- `test_id-01085` fs_read: fails tool  | 'Show drafts/outline.toml, lines 10 through 19. Much appreciated.' -> '{"name": "fs_list", "arguments": {"path": "drafts/outline.toml"}}'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_list", "arguments": {"path": "drafts/proposal.toml"}}'
- `test_id-01088` fs_read: fails args  | 'I need lines 40 to 49 in archive/invoice.md.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice.md", "limit": 5, "offset": 36}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.915 [0.873, 0.952] |
| L4 args | 0.688 [0.624, 0.751] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.643 [0.588, 0.697] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.00 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 0.50 |
| fs_list | 35 | 0.46 |
| fs_read | 35 | 0.31 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.80 |
| no_tool | 35 | 0.00 |
| unsupported | 35 | 0.00 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "one more thing", "k": 1}}'
- `test_ood-00353` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "single best hit", "k": 1}}'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00469` crag_stats: fails tool  | 'One more thing: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00471` crag_stats: fails tool  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00475` crag_stats: fails tool  | 'Hey there. Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00477` crag_stats: fails tool  | 'Report the size of the document index. Much appreciated.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00690` fs_list: fails args  | 'What does the sandbox root contain?' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research", "k": 5}}'
- `test_ood-00698` fs_list: fails tool  | 'What does drafts contain?' -> '{"name": "crag_search", "arguments": {"query": "drafts"}}'
