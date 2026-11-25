# dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.417 [0.333, 0.500] |
| L1 json | 0.358 [0.275, 0.442] |
| L2 schema | 0.358 [0.275, 0.442] |
| L3 tool | 0.358 [0.275, 0.442] |
| L4 args | 0.358 [0.275, 0.442] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.611 [0.539, 0.683] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 0.60 |
| crag_stats | 20 | 0.45 |
| fs_list | 20 | 0.70 |
| fs_read | 20 | 0.15 |
| fs_stat | 20 | 0.25 |
| fs_write | 20 | 0.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-00300` crag_search: fails json no call | 'Search the docs for subscriptions.' -> 'Which subset should I search the docs for: all files, or just one folder? If you mean one folder, which folder should I search that in?'
- `test_id-00302` crag_search: fails json no call | 'Find me the passages about subscriptions.' -> 'Which file should I read those from?'
- `test_id-00303` crag_search: fails json no call | 'Hey there. What does the index say about the soak test?' -> 'Which folder should I search in? The default is the root.'
- `test_id-00305` crag_search: fails json no call | 'Look through the indexed docs for anything on rate limiting at accept.' -> 'Which file should I read from docs?'
- `test_id-00308` crag_search: fails json no call | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> 'What should I do once I know more? What should I look up first?'
- `test_id-00311` crag_search: fails json no call | 'Look through the indexed docs for anything on cancellation of requests.' -> 'Which folder should I search in? I can do that once I know more. Let me check the index first.'
- `test_id-00314` crag_search: fails json no call | 'Find me the passages about log redaction.' -> 'What should I do with the results? I can list, read, stat or write to a file.'
- `test_id-00319` crag_search: fails json no call | 'Can you look up subscriptions in the documentation? Much appreciated.' -> 'I can do that once I know more. What should I look up: subscriptions or something else?'
- `test_id-00446` crag_stats: fails json no call | 'Is the search index empty? Cheers.' -> 'I can do that once I know more. What should I look up: k=10 or just query="empty"?'
- `test_id-00447` crag_stats: fails json  | 'Show me the index statistics.' -> '{"name": "crag_stats", "arguments": {}}\n<tool_call>'
- `test_id-00451` crag_stats: fails json  | 'One more thing: How many chunks are in the index?' -> '{"name": "crag_stats", "arguments": {}}\n<tool_call>'
- `test_id-00453` crag_stats: fails json  | 'Show me the index statistics. Much appreciated.' -> '{"name": "crag_stats", "arguments": {}}\n<tool_call>'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.307 [0.243, 0.376] |
| L1 json | 0.302 [0.238, 0.365] |
| L2 schema | 0.302 [0.238, 0.365] |
| L3 tool | 0.302 [0.238, 0.365] |
| L4 args | 0.302 [0.238, 0.365] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.554 [0.497, 0.609] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.37 |
| crag_stats | 14 | 0.29 |
| fs_list | 35 | 0.83 |
| fs_read | 35 | 0.17 |
| fs_stat | 35 | 0.14 |
| fs_write | 35 | 0.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 1.00 |

Failures (first 12):

- `test_ood-00321` crag_search: fails json no call | 'Run a retrieval on the soak test, please.' -> 'Happy to help. What should I look up?'
- `test_ood-00323` crag_search: fails json no call | 'Run a retrieval on the SSRF egress guard, please.' -> 'What should I look up: the SSRF egress guard?'
- `test_ood-00325` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Please check.' -> 'What should I do with the results? I can search the docs now: what should I do with the results?'
- `test_ood-00326` crag_search: fails json no call | 'Hey there. Pull up whatever the corpus has regarding the soak test.' -> 'Which folder should I look in? I can do that once I know more. The soak test is in the root, so let me check.'
- `test_ood-00327` crag_search: fails json no call | 'Run a retrieval on rate limiting at accept, please.' -> 'What should I do with the results? I can search the docs now: rate limiting at accept. What should I do with the results? I can search the d'
- `test_ood-00329` crag_search: fails json no call | 'One more thing: Run a retrieval on log redaction, please.' -> 'Happy to help. What should I look up?'
- `test_ood-00330` crag_search: fails json no call | 'One more thing: Pull up whatever the corpus has regarding the HNSW index.' -> 'Which folder should I look in? (Press enter for the top folder.)'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'Happy to help. What should I look up?'
- `test_ood-00333` crag_search: fails json no call | 'Hey there. Run a retrieval on the soak test, please. Give me 2 results.' -> 'Happy to help. What should I look up?'
- `test_ood-00334` crag_search: fails json no call | 'Pull up whatever the corpus has regarding cancellation of requests.' -> 'Which folder should I look in? I can do that once I know more.'
- `test_ood-00335` crag_search: fails json no call | 'Run a retrieval on cancellation of requests, please. Just the single best hit. Cheers.' -> 'What should I look up: cancellation of requests?'
- `test_ood-00337` crag_search: fails json no call | 'Run a retrieval on log redaction, please. Just the single best hit.' -> 'Which file should I search log redaction in?'
