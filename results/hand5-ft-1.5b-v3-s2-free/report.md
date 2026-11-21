# hand5-ft-1.5b-v3-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-12-ga660538 · date: 2026-11-21 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.952 [0.857, 1.000] |
| abstain | 0.722 [0.500, 0.889] |
| decision | 0.872 [0.769, 0.974] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.64 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand5-020` crag_search: fails args  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "k": 1}}'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-025` ambiguous: called '{"name": "crag_stats", "arguments": {"path": "that folder"}}' | 'check the stats on that folder'
- `test_hand5-026` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the error we were discussing"}}' | 'look up the error we were discussing'
- `test_hand5-029` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the topic I told you before", "k": 5}}' | 'search the knowledge base for 5 results about... actually the topic I told you before'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
