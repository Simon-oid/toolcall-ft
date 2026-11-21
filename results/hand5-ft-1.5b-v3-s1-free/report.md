# hand5-ft-1.5b-v3-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-12-ga660538 · date: 2026-11-21 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.952 [0.857, 1.000] |
| L3 tool | 0.952 [0.857, 1.000] |
| L4 args | 0.952 [0.857, 1.000] |
| abstain | 0.833 [0.667, 1.000] |
| decision | 0.923 [0.821, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.79 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand5-020` crag_search: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "path": "docs", "additionalProperties": false}}'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-029` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the topic I told you before", "k": 5}}' | 'search the knowledge base for 5 results about... actually the topic I told you before'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
