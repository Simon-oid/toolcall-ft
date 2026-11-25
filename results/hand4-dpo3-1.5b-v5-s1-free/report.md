# hand4-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.850 [0.700, 1.000] |
| L1 json | 0.850 [0.700, 1.000] |
| L2 schema | 0.800 [0.600, 0.950] |
| L3 tool | 0.800 [0.600, 0.950] |
| L4 args | 0.800 [0.600, 0.950] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.925 [0.825, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 1.00 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 0.50 |
| fs_list | 5 | 1.00 |
| fs_read | 3 | 1.00 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 0.33 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand4-024` crag_search: fails json no call | 'look for rate limiting in the index' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "rate limiting"}}'
- `test_hand4-027` fs_write: fails json no call | "put 'meeting moved to 3pm' in work/notes.md" -> '<tool_call>\n{"name": "fs_write", "arguments": {"path": "work/notes.md", "content": "meeting moved to 3pm"}}ьер'
- `test_hand4-028` fs_write: fails json no call | "save the line 'v4 ready' into logs/status.txt" -> '<tool_call>\n{"name": "fs_write", "arguments": {"path": "logs/status.txt", "content": "v4 ready"}}\n}'
- `test_hand4-035` crag_stats: fails schema {'path': '/property', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'how many files are in the index?' -> '{"name": "crag_stats", "arguments": {"property": "file count"}}'
