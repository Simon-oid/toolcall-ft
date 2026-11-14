# gptoss120b-low-api

model: openai/gpt-oss-120b · gguf: gpt-oss-120b · decoding: hosted API, native tool calling, temperature 0 · llama.cpp: hosted API https://api.groq.com/openai/v1, reasoning_effort low · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.983 [0.958, 1.000] |
| L4 args | 0.875 [0.808, 0.933] |
| abstain | 0.900 [0.817, 0.967] |
| decision | 0.967 [0.939, 0.989] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.85 |
| crag_search | 20 | 0.65 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.90 |
| fs_read | 20 | 0.80 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.90 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.85 |

Failures (first 12):

- `test_id-00300` crag_search: fails args  | 'Search the docs for subscriptions.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"subscriptions"}}'
- `test_id-00302` crag_search: fails args  | 'Find me the passages about subscriptions.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"subscriptions"}}'
- `test_id-00305` crag_search: fails args  | 'Look through the indexed docs for anything on rate limiting at accept.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"rate limiting at accept"}}'
- `test_id-00308` crag_search: fails args  | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"SSRF egress guard"}}'
- `test_id-00311` crag_search: fails args  | 'Look through the indexed docs for anything on cancellation of requests.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"cancellation of requests"}}'
- `test_id-00314` crag_search: fails args  | 'Find me the passages about log redaction.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"log redaction"}}'
- `test_id-00317` crag_search: fails args  | 'Look through the indexed docs for anything on the SSRF egress guard.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"SSRF egress guard"}}'
- `test_id-00682` fs_list: fails args  | "Okay, next: What's inside archive?" -> '{"name": "fs_list", "arguments": {"path":""}}'
- `test_id-00688` fs_list: fails tool  | "One more thing: What's inside archive?" -> '{"name": "crag_search", "arguments": {"k":5,"query":"archive contents"}}'
- `test_id-01086` fs_read: fails args  | "What's in drafts/proposal.toml?" -> '{"name": "fs_read", "arguments": {"limit":1000,"offset":1,"path":"drafts/proposal.toml"}}'
- `test_id-01092` fs_read: fails args  | "What's in archive/agenda.toml?" -> '{"name": "fs_read", "arguments": {"limit":1000,"offset":1,"path":"archive/agenda.toml"}}'
- `test_id-01097` fs_read: fails args  | 'Read drafts/outline.toml.' -> '{"name": "fs_read", "arguments": {"limit":1000,"offset":1,"path":"drafts/outline.toml"}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.979 [0.958, 0.995] |
| L3 tool | 0.947 [0.915, 0.979] |
| L4 args | 0.889 [0.841, 0.931] |
| abstain | 0.790 [0.714, 0.867] |
| decision | 0.918 [0.888, 0.949] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.63 |
| crag_search | 35 | 0.69 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.80 |
| fs_read | 35 | 0.91 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.74 |

Failures (first 12):

- `test_ood-00320` crag_search: fails args  | 'Pull up whatever the corpus has regarding the SSRF egress guard.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"SSRF egress guard"}}'
- `test_ood-00324` crag_search: fails args  | 'Pull up whatever the corpus has regarding nDCG evaluation.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"nDCG evaluation"}}'
- `test_ood-00326` crag_search: fails args  | 'Hey there. Pull up whatever the corpus has regarding the soak test.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"soak test"}}'
- `test_ood-00332` crag_search: fails args  | 'Pull up whatever the corpus has regarding structured tool output.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"structured tool output"}}'
- `test_ood-00334` crag_search: fails args  | 'Pull up whatever the corpus has regarding cancellation of requests.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"cancellation of requests"}}'
- `test_ood-00340` crag_search: fails args  | 'Pull up whatever the corpus has regarding subscriptions.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"subscriptions"}}'
- `test_ood-00346` crag_search: fails args  | 'Pull up whatever the corpus has regarding the HNSW index.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"HNSW index"}}'
- `test_ood-00348` crag_search: fails args  | 'Hey there. Pull up whatever the corpus has regarding rate limiting at accept.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"rate limiting at accept"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I’m happy to run a retrieval for you, but I need to know what you’d like to search for. Could you please provide the query (the topic or que'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'I’m not sure what you’d like to search for. Could you please provide a short query (a few keywords or a sentence) that I should use for the '
- `test_ood-00352` crag_search: fails args  | 'Pull up whatever the corpus has regarding log redaction.' -> '{"name": "crag_search", "arguments": {"k":10,"query":"log redaction"}}'
- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"k":5,"query":"research contain"}}'
