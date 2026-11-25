# dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.900 [0.842, 0.950] |
| L1 json | 0.892 [0.833, 0.942] |
| L2 schema | 0.892 [0.833, 0.942] |
| L3 tool | 0.892 [0.833, 0.942] |
| L4 args | 0.875 [0.817, 0.933] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.928 [0.889, 0.961] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 0.65 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.90 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 0.80 |
| fs_write | 20 | 0.90 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.95 |

Failures (first 12):

- `test_id-00300` crag_search: fails json no call | 'Search the docs for subscriptions.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "subscriptions"}}'
- `test_id-00302` crag_search: fails json no call | 'Find me the passages about subscriptions.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "subscriptions"}}'
- `test_id-00304` crag_search: fails json no call | 'Okay, next: I need info on nDCG evaluation; check the knowledge base.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "nDCG evaluation"}}'
- `test_id-00308` crag_search: fails args  | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "the SSRF egress guard", "k": 10}}'
- `test_id-00311` crag_search: fails json no call | 'Look through the indexed docs for anything on cancellation of requests.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "cancellation of requests"}}'
- `test_id-00313` crag_search: fails json no call | 'Can you look up the SSRF egress guard in the documentation?' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the SSRF egress guard"}}'
- `test_id-00314` crag_search: fails json no call | 'Find me the passages about log redaction.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "log redaction"}}'
- `test_id-00675` fs_list: fails json  | 'List the files in the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}};'
- `test_id-00683` fs_list: fails json no call | 'Show me the contents of archive. Please check.' -> '<tool_call>:///tools/{"name": "fs_list", "arguments": {"path": "archive"}}'
- `test_id-01291` fs_stat: fails json no call | 'What are the permissions on archive/results.txt?' -> '<tool_call>'
- `test_id-01303` fs_stat: fails json no call | 'What are the permissions on scripts/readme.txt?' -> '<tool_call>'
- `test_id-01304` fs_stat: fails args  | 'Is research/proposal.py a file or a directory?' -> '{"name": "fs_stat", "arguments": {"path": "research/propoal.py"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.862 [0.810, 0.910] |
| L1 json | 0.852 [0.799, 0.899] |
| L2 schema | 0.804 [0.746, 0.862] |
| L3 tool | 0.794 [0.735, 0.852] |
| L4 args | 0.735 [0.672, 0.799] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.912 [0.878, 0.942] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.77 |
| crag_stats | 14 | 0.29 |
| fs_list | 35 | 0.77 |
| fs_read | 35 | 0.77 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.54 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00327` crag_search: fails json no call | 'Run a retrieval on rate limiting at accept, please.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "rate limiting at accept"}}'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should the search query be?'
- `test_ood-00334` crag_search: fails json no call | 'Pull up whatever the corpus has regarding cancellation of requests.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "Cancellation of requests"}}'
- `test_ood-00340` crag_search: fails json no call | 'Pull up whatever the corpus has regarding subscriptions.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "subscriptions"}}'
- `test_ood-00343` crag_search: fails json  | 'Okay, next: Run a retrieval on the soak test, please.' -> '{"name": "crag_search", "arguments": {"query": "the soak test"}}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'What should the query be?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should the query be?'
- `test_ood-00352` crag_search: fails json no call | 'Pull up whatever the corpus has regarding log redaction.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "log redaction"}}'
- `test_ood-00465` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Okay, next: Report the size of the document index.' -> '{"name": "crag_stats", "arguments": {"path": "document index"}}'
- `test_ood-00467` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Report the size of the document index.' -> '{"name": "crag_stats", "arguments": {"path": "document index"}}'
- `test_ood-00468` crag_stats: fails json no call | 'Is anything actually indexed right now? Cheers.' -> '|RF: {"name": "crag_stats", "arguments": {}}|'
- `test_ood-00470` crag_stats: fails json no call | 'Is anything actually indexed right now?' -> '|RF: {"name": "crag_stats", "arguments": {}}|'
