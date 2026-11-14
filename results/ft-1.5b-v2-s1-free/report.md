# ft-1.5b-v2-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.983 [0.958, 1.000] |
| L4 args | 0.983 [0.958, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.994 [0.983, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.90 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00670` fs_list: fails tool  | "What's inside scripts? Please check." -> '{"name": "crag_search", "arguments": {"query": "scripts"}}'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which file or directory should I look in the archive?'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.963, 1.000] |
| L1 json | 0.984 [0.963, 1.000] |
| L2 schema | 0.979 [0.958, 0.995] |
| L3 tool | 0.884 [0.836, 0.926] |
| L4 args | 0.878 [0.831, 0.921] |
| abstain | 0.990 [0.971, 1.000] |
| decision | 0.986 [0.973, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.97 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 0.50 |
| fs_list | 35 | 0.60 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. Which tool should I call to search the document index?'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00469` crag_stats: fails tool  | 'One more thing: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00471` crag_stats: fails tool  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00475` crag_stats: fails tool  | 'Hey there. Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00477` crag_stats: fails tool  | 'Report the size of the document index. Much appreciated.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00690` fs_list: fails schema {'path': '/path', 'keyword': 'required', 'message': 'missing required property'} | 'What does the sandbox root contain?' -> '{"name": "fs_stat", "arguments": {}}'
- `test_ood-00692` fs_list: fails tool  | 'One more thing: What does data/raw contain?' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> "I can't search the document index to find that information."
