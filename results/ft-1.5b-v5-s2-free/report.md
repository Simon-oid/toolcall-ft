# ft-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.994 [0.983, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.95 |

Failures (first 12):

- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.963, 1.000] |
| L1 json | 0.984 [0.963, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.984 [0.963, 1.000] |
| L4 args | 0.979 [0.958, 0.995] |
| abstain | 0.990 [0.971, 1.000] |
| decision | 0.986 [0.973, 0.997] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 0.97 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.97 |

Failures (first 12):

- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should I search the documentation for?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the documentation for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I search the documentation for?'
- `test_ood-01126` fs_read: fails args  | 'Resume research/invoice.toml from line 5.' -> '{"name": "fs_read", "arguments": {"path": "invoice.toml", "offset": 5}}'
- `test_ood-01958` unsupported: called '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.toml"}}' | 'Translate scripts/notes-2026.toml into German and save it.'
