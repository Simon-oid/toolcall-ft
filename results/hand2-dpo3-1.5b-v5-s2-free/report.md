# hand2-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.281 [0.125, 0.438] |
| L1 json | 0.250 [0.125, 0.406] |
| L2 schema | 0.250 [0.125, 0.406] |
| L3 tool | 0.250 [0.125, 0.406] |
| L4 args | 0.250 [0.125, 0.406] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.521 [0.375, 0.667] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 0.33 |
| crag_stats | 4 | 0.50 |
| fs_list | 5 | 0.40 |
| fs_read | 8 | 0.12 |
| fs_stat | 4 | 0.25 |
| fs_write | 5 | 0.00 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand2-000` crag_search: fails json no call | 'my boss asked how the server deals with request cancellation, can you find that in the docs' -> 'I can do that once I know more. What should I look up?'
- `test_hand2-003` crag_search: fails json no call | 'Find documentation on the worker pool size setting.' -> 'Which file should I read that information from?'
- `test_hand2-004` crag_search: fails json no call | 'query the docs: TypeScript SDK benchmark' -> 'I can do that once I know more. What should I look up?'
- `test_hand2-005` crag_search: fails json no call | 'I need the parts of the docs about structured logging, give me 6' -> "Which folder should I search in? (Optional: The docs are in the folder named 'docs'.)"
- `test_hand2-007` crag_stats: fails json  | 'give me the stats of the knowledge base' -> '{"name": "crag_stats", "arguments": {}}\n<tool_call>'
- `test_hand2-008` crag_stats: fails json no call | 'did the indexing actually work? show the db diagnostics' -> 'I can do that once I know more. What should I look up?'
- `test_hand2-011` fs_list: fails json no call | 'show the contents of the top-level directory' -> 'Which folder should I list? The top-level one is fine.'
- `test_hand2-013` fs_list: fails json no call | "I can't remember what I put in drafts/blog — list it please" -> 'Sure, but I need one detail first. Which folder should I list?'
- `test_hand2-014` fs_list: fails json no call | 'are there files in the exports folder' -> 'I can do that once I know more. Which folder should I look in?'
- `test_hand2-015` fs_read: fails json no call | 'can you read invoices/2025/march.csv to me' -> 'Sure, but I need one detail first. What should the file be called?'
- `test_hand2-016` fs_read: fails json no call | 'open drafts/blog/post-1.md' -> 'I can do that once I know more. What should I look up: the contents of drafts/blog/post-1.md?'
- `test_hand2-017` fs_read: fails json no call | 'what does the first line of exports/summary.txt say?' -> 'Which file should I read that from? exports/summary.txt.'
