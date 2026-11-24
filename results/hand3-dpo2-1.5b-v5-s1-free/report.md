# hand3-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.941 [0.853, 1.000] |
| L2 schema | 0.912 [0.794, 1.000] |
| L3 tool | 0.853 [0.735, 0.971] |
| L4 args | 0.824 [0.676, 0.941] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.708 [0.583, 0.833] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 0.00 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 0.33 |
| fs_list | 8 | 0.88 |
| fs_read | 7 | 0.86 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 0.75 |
| no_tool | 5 | 0.00 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand3-000` fs_list: fails tool  | 'what does photos contain' -> '{"name": "crag_search", "arguments": {"query": "photos"}}'
- `test_hand3-012` fs_read: fails args  | 'open taxes/2025.csv from line 20' -> '{"name": "fs_read", "arguments": {"path": "taxes/2025.csv", "offset": 20, "limit": 1}}'
- `test_hand3-024` crag_stats: fails json  | 'is the document index empty or not' -> '{"name": "crag_stats", "arguments": {}'
- `test_hand3-025` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | "what's the embedding dim of the index" -> '{"name": "crag_stats", "arguments": {"path": "index"}}'
- `test_hand3-028` fs_stat: fails tool  | 'is backups a folder or a file?' -> '{"name": "fs_list", "arguments": {"path": "backups"}}'
- `test_hand3-032` fs_write: fails json  | 'put this in notes/ideas.md: try the italian stemmer' -> '{"name": "fs_write", "arguments": {"path": "notes/ideas.md", "content": "try the italian stemmer"})'
- `test_hand3-034` no_tool: called '{"name": "fs_list", "arguments": {"path": "sandbox"}}' | 'ciao, come va?'
- `test_hand3-035` no_tool: called '{"name": "math_calculator", "arguments": {"operation": "multiply", "number1": 15, "number2": 80}}' | "what's 15% of 80?"
- `test_hand3-036` no_tool: called '{"name": "fs_list", "arguments": {"path": "docs"}}' | "thanks, that's all for today"
- `test_hand3-037` no_tool: called '{"name": "crag_search", "arguments": {"query": "a fun fact about octopuses"}}' | 'tell me a fun fact about octopuses'
- `test_hand3-038` no_tool: called '{"name": "fs_list", "arguments": {"path": "messages"}}' | 'good morning!'
- `test_hand3-039` unsupported: called '{"name": "fs_write", "arguments": {"path": "thesis/abstract.md", "content": "email your professor"}' | 'email thesis/abstract.md to my professor'
