# hand5-ft-1.5b-v7-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-26 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.952 [0.857, 1.000] |
| L4 args | 0.905 [0.762, 1.000] |
| abstain | 0.889 [0.722, 1.000] |
| decision | 0.949 [0.872, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.86 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 0.67 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand5-006` fs_stat: fails tool  | 'check the permissions and size of the logs/ directory' -> '{"name": "fs_list", "arguments": {"path": "logs"}}'
- `test_hand5-020` crag_search: fails args  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "k": 1}}'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
