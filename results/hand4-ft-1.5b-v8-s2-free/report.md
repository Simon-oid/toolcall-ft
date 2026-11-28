# hand4-ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.900 [0.750, 1.000] |
| decision | 0.950 [0.875, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 0.88 |
| crag_search | 5 | 1.00 |
| crag_stats | 2 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 3 | 1.00 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand4-001` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the stuff we covered"}}' | 'search the knowledge base for the stuff we covered'
- `test_hand4-004` ambiguous: called '{"name": "crag_search", "arguments": {"query": "whatever we found last time"}}' | 'pull up whatever we found last time'
