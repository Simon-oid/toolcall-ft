# dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.867 [0.800, 0.925] |
| L2 schema | 0.858 [0.792, 0.917] |
| L3 tool | 0.858 [0.792, 0.917] |
| L4 args | 0.842 [0.775, 0.908] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.667 [0.600, 0.733] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.00 |
| crag_search | 20 | 0.95 |
| crag_stats | 20 | 0.60 |
| fs_list | 20 | 0.80 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.70 |
| no_tool | 20 | 0.00 |
| unsupported | 20 | 0.00 |

Failures (first 12):

- `test_id-00308` crag_search: fails args  | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "the SSRF egress guard", "k": 1}}'
- `test_id-00445` crag_stats: fails json  | 'How many chunks are in the index?' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00446` crag_stats: fails json  | 'Is the search index empty? Cheers.' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00452` crag_stats: fails json  | 'Is the search index empty?' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00454` crag_stats: fails json  | 'What embedding dimension does the index use? Please check.' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00455` crag_stats: fails json  | 'How many files have been indexed?' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00457` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'How many chunks are in the index? Much appreciated.' -> '{"name": "crag_stats", "arguments": {"path": "index"}}'
- `test_id-00458` crag_stats: fails json  | 'Is the search index empty? Please check.' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00461` crag_stats: fails json  | 'How many files have been indexed? Please check.' -> '{"name": "crag_stats", "arguments": {}'
- `test_id-00670` fs_list: fails json  | "What's inside scripts? Please check." -> '{"name": "fs_list", "arguments": {"path": "scripts"}'
- `test_id-00675` fs_list: fails args  | 'List the files in the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_id-00680` fs_list: fails json  | 'Enumerate the entries of archive. Much appreciated.' -> '{"name": "fs_list", "arguments": {"path": "archive"}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.889 [0.841, 0.931] |
| L2 schema | 0.889 [0.841, 0.931] |
| L3 tool | 0.847 [0.794, 0.894] |
| L4 args | 0.794 [0.735, 0.852] |
| abstain | 0.019 [0.000, 0.048] |
| decision | 0.650 [0.595, 0.704] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.00 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 0.14 |
| fs_list | 35 | 0.83 |
| fs_read | 35 | 0.74 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.74 |
| no_tool | 35 | 0.06 |
| unsupported | 35 | 0.00 |

Failures (first 12):

- `test_ood-00325` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Please check.' -> '{"name": "crag_search", "arguments": {"query": "nDCG evaluation", "k": 10}}'
- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit", "k": 1}}'
- `test_ood-00339` crag_search: fails args  | 'Run a retrieval on log redaction, please. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "log redaction", "k": 10}}'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "document/index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-00468` crag_stats: fails json  | 'Is anything actually indexed right now? Cheers.' -> '{"name": "crag_stats", "arguments": {}'
- `test_ood-00469` crag_stats: fails json  | 'One more thing: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "crag_index"}'
- `test_ood-00470` crag_stats: fails json  | 'Is anything actually indexed right now?' -> '{"name": "crag_stats", "arguments": {}'
- `test_ood-00471` crag_stats: fails json  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "document/index"}'
- `test_ood-00472` crag_stats: fails json  | 'Is anything actually indexed right now? Please check.' -> '{"name": "crag_stats", "arguments": {}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "document index"}}'
- `test_ood-00474` crag_stats: fails json  | 'Okay, next: Is anything actually indexed right now?' -> '{"name": "crag_stats", "arguments": {}'
