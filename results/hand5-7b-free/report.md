# hand5-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-12-ga660538 · date: 2026-11-21 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.810 [0.619, 0.952] |
| abstain | 0.722 [0.500, 0.889] |
| decision | 0.872 [0.769, 0.974] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.79 |
| crag_search | 5 | 0.20 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 0.00 |

Failures (first 12):

- `test_hand5-007` crag_search: fails args  | 'search the knowledge base for documents about retry logic and exponential backoff' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "retry logic and exponential backoff"}}'
- `test_hand5-008` crag_search: fails args  | 'find anything in the docs related to authentication tokens' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "authentication tokens"}}'
- `test_hand5-016` crag_search: fails args  | 'search for anything about vector similarity and cosine distance' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "vector similarity cosine distance"}}'
- `test_hand5-020` crag_search: fails args  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "k": 5}}'
- `test_hand5-025` ambiguous: called '{"name": "crag_stats", "arguments": {}}' | 'check the stats on that folder'
- `test_hand5-032` ambiguous: called '{"name": "fs_stat", "arguments": {"path": ""}}' | 'get the metadata for the file I uploaded yesterday'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
- `test_hand5-037` unsupported: called '{"name": "fs_list", "arguments": {"path": "logs/"}}' | 'can you delete the old log files in logs/?'
- `test_hand5-038` unsupported: called '{"name": "fs_list", "arguments": {"path": "data/"}}' | 'rename data/draft.csv to data/final.csv'
