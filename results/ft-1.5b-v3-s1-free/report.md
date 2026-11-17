# ft-1.5b-v3-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-8-gf20d47e · date: 2026-11-17 · cases: 474

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
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.952 [0.921, 0.979] |
| L4 args | 0.952 [0.921, 0.979] |
| abstain | 0.952 [0.905, 0.990] |
| decision | 0.976 [0.959, 0.993] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.89 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 0.50 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.97 |

Failures (first 12):

- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'Which text should I search the HNSW index for?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What query should I run the search for?'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-00471` crag_stats: fails tool  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00472` crag_stats: fails schema {'path': '/query', 'keyword': 'required', 'message': 'missing required property'} | 'Is anything actually indexed right now? Please check.' -> '{"name": "crag_search", "arguments": {}}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-00475` crag_stats: fails tool  | 'Hey there. Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00477` crag_stats: fails tool  | 'Report the size of the document index. Much appreciated.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-01947` unsupported: called '{"name": "fs_write", "arguments": {"path": "dinner.txt", "content": "Dinner is at 7."}}' | 'Text my brother that dinner is at 7. Please check.'
- `test_ood-02120` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/outline.toml", "content": "the content you want to write"}}' | 'Fill archive/outline.toml in.'
- `test_ood-02126` ambiguous: called '{"name": "crag_search", "arguments": {"query": "that"}}' | 'Find the part about that in the docs. Cheers.'
