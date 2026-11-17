# hand3-ft-1.5b-v3-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-8-gf20d47e · date: 2026-11-17 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.971 [0.912, 1.000] |
| L1 json | 0.971 [0.912, 1.000] |
| L2 schema | 0.971 [0.912, 1.000] |
| L3 tool | 0.971 [0.912, 1.000] |
| L4 args | 0.971 [0.912, 1.000] |
| abstain | 0.857 [0.643, 1.000] |
| decision | 0.938 [0.854, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 0.75 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 1.00 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> 'The text "backups" is not a folder or a file, it is just a word.'
- `test_hand3-043` unsupported: called '{"name": "crag_search", "arguments": {"query": "projects/crag"}}' | 'run the tests in projects/crag'
- `test_hand3-047` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the thing we talked about"}}' | 'search for the thing we talked about'
