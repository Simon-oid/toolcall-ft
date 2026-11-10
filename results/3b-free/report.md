# 3b-free

model: Qwen/Qwen2.5-3B-Instruct · gguf: qwen2.5-3b-instruct-q4_k_m.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.975 [0.942, 1.000] |
| L1 json | 0.975 [0.942, 1.000] |
| L2 schema | 0.975 [0.942, 1.000] |
| L3 tool | 0.950 [0.908, 0.983] |
| L4 args | 0.817 [0.750, 0.883] |
| abstain | 0.617 [0.483, 0.733] |
| decision | 0.856 [0.806, 0.906] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.80 |
| crag_search | 20 | 0.90 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 0.35 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.65 |
| no_tool | 20 | 0.65 |
| unsupported | 20 | 0.40 |

Failures (first 12):

- `test_id-00301` crag_search: fails json no call | 'Can you look up nDCG evaluation in the documentation? Give me 2 results. Much appreciated.' -> 'It seems there might be a misunderstanding. The provided functions do not include a capability to search through documentation or retrieve s'
- `test_id-00302` crag_search: fails json no call | 'Find me the passages about subscriptions.' -> 'Could you please provide more context or a specific query about subscriptions? For example, are you looking for information on how to subscr'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_stat", "arguments": {"path": "drafts/proposal.toml"}}'
- `test_id-01087` fs_read: fails args  | 'Print the contents of archive/invoice.py. Please check.' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "archive/invoice.py"}}'
- `test_id-01091` fs_read: fails args  | 'Read scripts/notes-2026.md. Much appreciated.' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "scripts/notes-2026.md"}}'
- `test_id-01092` fs_read: fails tool  | "What's in archive/agenda.toml?" -> '{"name": "fs_stat", "arguments": {"path": "archive/agenda.toml"}}'
- `test_id-01094` fs_read: fails tool  | 'Okay, next: head -n 10 scripts/notes-2026.toml' -> '{"name": "fs_list", "arguments": {"path": "scripts/notes-2026.toml"}}'
- `test_id-01096` fs_read: fails args  | 'Hey there. Open data/raw/agenda.md and show it to me.' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "data/raw/agenda.md"}}'
- `test_id-01097` fs_read: fails args  | 'Read drafts/outline.toml.' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "drafts/outline.toml"}}'
- `test_id-01098` fs_read: fails args  | "What's in archive/invoice.md?" -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "archive/invoice.md"}}'
- `test_id-01099` fs_read: fails args  | 'Print the contents of scripts/readme.toml.' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "scripts/readme.toml"}}'
- `test_id-01100` fs_read: fails args  | 'One more thing: cat scripts/readme.toml' -> '{"name": "fs_read", "arguments": {"limit": 1, "offset": 1, "path": "scripts/readme.toml"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.926 [0.889, 0.963] |
| L1 json | 0.926 [0.889, 0.963] |
| L2 schema | 0.921 [0.878, 0.958] |
| L3 tool | 0.910 [0.868, 0.947] |
| L4 args | 0.704 [0.640, 0.767] |
| abstain | 0.600 [0.505, 0.695] |
| decision | 0.810 [0.762, 0.854] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.77 |
| crag_search | 35 | 0.86 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.80 |
| fs_read | 35 | 0.37 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.37 |
| no_tool | 35 | 0.54 |
| unsupported | 35 | 0.49 |

Failures (first 12):

- `test_ood-00323` crag_search: fails json no call | 'Run a retrieval on the SSRF egress guard, please.' -> 'Sure, could you please provide me with a more specific query? What exact information are you looking for regarding the SSRF egress guard?'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'It seems there might be a misunderstanding. The `crag_search` function is designed for hybrid retrieval using BM25 and cosine similarity, no'
- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"k": 1, "query": "single best hit"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'Could you please specify the query you would like to run and the number of chunks (`k`) you would like to retrieve?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'It seems there is no direct function provided for nDCG evaluation or ranking. However, I can perform a retrieval using BM25 and cosine simil'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> 'Could you please specify what aspect of research you are interested in? For example, theories, methods, findings, or applications.'
- `test_ood-00696` fs_list: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'What does data/raw contain?' -> '{"name": "crag_stats", "arguments": {"path": "data/raw"}}'
- `test_ood-00702` fs_list: fails json no call | 'Okay, next: What does research contain?' -> "Could you please specify what aspect of research you're interested in, such as a specific topic, methodology, or any other detail? This will"
- `test_ood-00706` fs_list: fails json no call | 'What does archive contain?' -> 'Could you please specify which archive you are referring to? I need more information to provide relevant information.'
- `test_ood-00710` fs_list: fails tool  | 'What does research contain? Cheers.' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "What does research contain? Cheers."}}'
- `test_ood-00712` fs_list: fails tool  | 'What does scripts contain? Cheers.' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "scripts"}}'
- `test_ood-00714` fs_list: fails json no call | 'One more thing: What does archive contain?' -> "I need to know the specific file or directory within the archive you're referring to. Could you please specify which one you're interested i"
