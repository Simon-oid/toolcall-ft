# hand-ft-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.974 [0.923, 1.000] |
| abstain | 0.933 [0.800, 1.000] |
| decision | 0.981 [0.944, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.88 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 1.00 |
| fs_read | 10 | 1.00 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand-007` crag_search: fails args  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_search", "arguments": {"query": "the replay fixtures are captured"}}'
- `test_hand-048` unsupported: called '{"name": "crag_rebuild", "arguments": {}}' | 're-embed all documents with a newer model'
