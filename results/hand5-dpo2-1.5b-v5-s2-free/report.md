# hand5-dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.905 [0.762, 1.000] |
| abstain | 0.667 [0.444, 0.889] |
| decision | 0.846 [0.718, 0.949] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.71 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 0.67 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 0.00 |

Failures (first 12):

- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"path": ".gitignore", "content": "__pycache__\\n.env"}}'
- `test_hand5-020` crag_search: fails args  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "k": 1}}'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-026` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the error"}}' | 'look up the error we were discussing'
- `test_hand5-030` ambiguous: called '{"name": "fs_read", "arguments": {"path": "docs/README.md", "offset": 10, "limit": 5}}' | 'can you read the lines around the function definition?'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
- `test_hand5-037` unsupported: called '{"name": "fs_list", "arguments": {"path": "logs"}}' | 'can you delete the old log files in logs/?'
- `test_hand5-038` unsupported: called '{"name": "fs_rename", "arguments": {"oldpath": "data/draft.csv", "newpath": "data/final.csv"}}' | 'rename data/draft.csv to data/final.csv'
