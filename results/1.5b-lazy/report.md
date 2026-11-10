# 1.5b-lazy

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: llama.cpp tool grammar, applied once a call starts (lazy) · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.975 [0.942, 1.000] |
| L1 json | 0.975 [0.942, 1.000] |
| L2 schema | 0.975 [0.942, 1.000] |
| L3 tool | 0.908 [0.850, 0.958] |
| L4 args | 0.775 [0.700, 0.850] |
| abstain | 0.567 [0.433, 0.700] |
| decision | 0.839 [0.783, 0.889] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.65 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 0.95 |
| fs_list | 20 | 0.60 |
| fs_read | 20 | 0.30 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.80 |
| no_tool | 20 | 0.40 |
| unsupported | 20 | 0.65 |

Failures (first 12):

- `test_id-00448` crag_stats: fails tool  | 'What embedding dimension does the index use?' -> '{"name": "fs_stat", "arguments": {"path": "index/embedding_dimension"}}'
- `test_id-00673` fs_list: fails args  | 'One more thing: Which files are under the base directory?' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00674` fs_list: fails args  | 'Enumerate the entries of the base directory.' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00675` fs_list: fails args  | 'List the files in the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00678` fs_list: fails args  | 'One more thing: ls scripts' -> '{"name": "fs_list", "arguments": {\n"path": "/scripts"\n}}'
- `test_id-00682` fs_list: fails json no call | "Okay, next: What's inside archive?" -> "I'm sorry, but I don't have any information about an archive. Could you please provide more details or clarify your question?"
- `test_id-00683` fs_list: fails args  | 'Show me the contents of archive. Please check.' -> '{"name": "fs_list", "arguments": {"path": "/archive"}}'
- `test_id-00684` fs_list: fails args  | 'Okay, next: ls the base directory' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> "I'm sorry, but I don't have any information about an archive. Could you please provide more details or clarify your question?"
- `test_id-01084` fs_read: fails args  | 'Read lines 40 to 44 of archive/checklist.md.' -> '{"name": "fs_read", "arguments": {"path": "archive/checklist.md", "limit": 4, "offset": 40}}'
- `test_id-01085` fs_read: fails tool  | 'Show drafts/outline.toml, lines 10 through 19. Much appreciated.' -> '{"name": "fs_list", "arguments": {"path": "drafts/outline.toml"}}'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_list", "arguments": {"path": "drafts/proposal.toml"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.989 [0.974, 1.000] |
| L3 tool | 0.868 [0.820, 0.915] |
| L4 args | 0.677 [0.608, 0.741] |
| abstain | 0.552 [0.457, 0.648] |
| decision | 0.833 [0.789, 0.874] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.60 |
| crag_search | 35 | 0.89 |
| crag_stats | 14 | 0.50 |
| fs_list | 35 | 0.40 |
| fs_read | 35 | 0.26 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.91 |
| no_tool | 35 | 0.40 |
| unsupported | 35 | 0.66 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "one more thing", "k": 1}}'
- `test_ood-00335` crag_search: fails args  | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> '{"name": "crag_search", "arguments": {"query": "cancellation"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'Sure, I can help with that. Could you please provide me with the query you want to retrieve from the structured tool output?'
- `test_ood-00353` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "single best hit", "k": 1}}'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00469` crag_stats: fails tool  | 'One more thing: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00471` crag_stats: fails tool  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00475` crag_stats: fails tool  | 'Hey there. Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00477` crag_stats: fails tool  | 'Report the size of the document index. Much appreciated.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00690` fs_list: fails args  | 'What does the sandbox root contain?' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
