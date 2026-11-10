# 3b-lazy

model: Qwen/Qwen2.5-3B-Instruct · gguf: qwen2.5-3b-instruct-q4_k_m.gguf · decoding: llama.cpp tool grammar, applied once a call starts (lazy) · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.958 [0.917, 0.992] |
| L1 json | 0.958 [0.917, 0.992] |
| L2 schema | 0.958 [0.917, 0.992] |
| L3 tool | 0.900 [0.842, 0.950] |
| L4 args | 0.758 [0.683, 0.833] |
| abstain | 0.617 [0.500, 0.733] |
| decision | 0.844 [0.789, 0.894] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.75 |
| crag_search | 20 | 0.75 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 0.20 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.60 |
| no_tool | 20 | 0.70 |
| unsupported | 20 | 0.40 |

Failures (first 12):

- `test_id-00301` crag_search: fails json no call | 'Can you look up nDCG evaluation in the documentation? Give me 2 results. Much appreciated.' -> 'It seems there might be a misunderstanding. The provided functions do not include a capability to search through documentation or retrieve s'
- `test_id-00302` crag_search: fails json no call | 'Find me the passages about subscriptions.' -> 'Could you please provide more context or a specific query about subscriptions? For example, a topic or a keyword related to subscriptions. T'
- `test_id-00304` crag_search: fails tool  | 'Okay, next: I need info on nDCG evaluation; check the knowledge base.' -> '{"name": "fs_read", "arguments": {"path": "knowledge_base/article_nDCG_evaluation.txt"}}'
- `test_id-00313` crag_search: fails json no call | 'Can you look up the SSRF egress guard in the documentation?' -> 'I need to search the index for relevant chunks. Could you please provide more context or a specific question about the SSRF egress guard? Th'
- `test_id-00319` crag_search: fails json no call | 'Can you look up subscriptions in the documentation? Much appreciated.' -> 'I need to search for relevant chunks from the documentation index. Could you please provide me with a query to use for this search?'
- `test_id-01085` fs_read: fails args  | 'Show drafts/outline.toml, lines 10 through 19. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "drafts/outline.toml", "offset": 10}}'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_stat", "arguments": {"path": "drafts/proposal.toml"}}'
- `test_id-01087` fs_read: fails args  | 'Print the contents of archive/invoice.py. Please check.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice.py", "limit": 1, "offset": 1}}'
- `test_id-01091` fs_read: fails args  | 'Read scripts/notes-2026.md. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.md", "limit": 1000}}'
- `test_id-01092` fs_read: fails tool  | "What's in archive/agenda.toml?" -> '{"name": "fs_stat", "arguments": {"path": "archive/agenda.toml"}}'
- `test_id-01093` fs_read: fails args  | 'Print lines 3 to 7 from research/outline.py. Please check.' -> '{"name": "fs_read", "arguments": {"path": "research/outline.py", "limit": 7, "offset": 3}}'
- `test_id-01094` fs_read: fails tool  | 'Okay, next: head -n 10 scripts/notes-2026.toml' -> '{"name": "fs_list", "arguments": {"path": "scripts/notes-2026.toml"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.921 [0.878, 0.958] |
| L1 json | 0.915 [0.873, 0.952] |
| L2 schema | 0.915 [0.873, 0.952] |
| L3 tool | 0.910 [0.868, 0.947] |
| L4 args | 0.704 [0.640, 0.767] |
| abstain | 0.610 [0.514, 0.705] |
| decision | 0.810 [0.762, 0.854] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.80 |
| crag_search | 35 | 0.86 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.83 |
| fs_read | 35 | 0.29 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.43 |
| no_tool | 35 | 0.60 |
| unsupported | 35 | 0.43 |

Failures (first 12):

- `test_ood-00323` crag_search: fails json no call | 'Run a retrieval on the SSRF egress guard, please.' -> 'Sure, could you please provide me with a more specific query? What exact information are you looking for regarding the SSRF egress guard?'
- `test_ood-00325` crag_search: fails tool  | 'Run a retrieval on nDCG evaluation, please. Please check.' -> '{"name": "crag_stats", "arguments": {}}'
- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "specific query about the topic", "k": 1}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'Could you please specify the query you would like to run and the number of chunks (`k`) you would like to retrieve?'
- `test_ood-00353` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "your query here", "k": 1}}'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> "Could you please specify what aspect of research you're interested in? For example, theories, methods, findings, or applications."
- `test_ood-00702` fs_list: fails json no call | 'Okay, next: What does research contain?' -> "Could you please specify what aspect of research you're interested in, such as a specific topic, methodology, or any other detail?"
- `test_ood-00706` fs_list: fails json no call | 'What does archive contain?' -> 'Could you please specify which archive you are referring to? I need more information to provide relevant details.'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'Could you please specify what aspect of the research you are interested in, such as a particular topic or field?'
- `test_ood-00714` fs_list: fails json no call | 'One more thing: What does archive contain?' -> "I need to know the specific file or directory within the archive you're referring to. Could you please specify which file or directory you w"
- `test_ood-00722` fs_list: fails json no call | 'What does drafts contain? Cheers.' -> 'To provide information about what is contained in drafts, I would first need to know where the drafts are located. Could you please specify '
- `test_ood-01105` fs_read: fails args  | 'Let me see what drafts/notes-2026.py says.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.py", "limit": 1, "offset": 1}}'
