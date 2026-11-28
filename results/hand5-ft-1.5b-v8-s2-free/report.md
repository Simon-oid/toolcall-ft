# hand5-ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.952 [0.857, 1.000] |
| L4 args | 0.810 [0.619, 0.952] |
| abstain | 0.833 [0.667, 1.000] |
| decision | 0.923 [0.821, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.79 |
| crag_search | 5 | 0.60 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 0.67 |
| fs_write | 3 | 0.67 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand5-006` fs_stat: fails tool  | 'check the permissions and size of the logs/ directory' -> '{"name": "fs_list", "arguments": {"path": "logs"}}'
- `test_hand5-007` crag_search: fails args  | 'search the knowledge base for documents about retry logic and exponential backoff' -> '{"name": "crag_search", "arguments": {"query": "retry logic"}}'
- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"path": "my_gitignore.txt", "content": "__pycache__\\n.env"}}'
- `test_hand5-016` crag_search: fails args  | 'search for anything about vector similarity and cosine distance' -> '{"name": "crag_search", "arguments": {"query": "vector similarity"}}'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-030` ambiguous: called '{"name": "fs_read", "arguments": {"path": "src/func_def.md"}}' | 'can you read the lines around the function definition?'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
