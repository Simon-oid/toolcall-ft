# hand3-dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.941 [0.853, 1.000] |
| L1 json | 0.941 [0.853, 1.000] |
| L2 schema | 0.941 [0.853, 1.000] |
| L3 tool | 0.941 [0.853, 1.000] |
| L4 args | 0.912 [0.794, 1.000] |
| abstain | 0.929 [0.786, 1.000] |
| decision | 0.938 [0.854, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 0.88 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 1.00 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.50 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-017` crag_search: fails args  | 'find stuff about TSan in the knowledge base. one result is enough' -> '{"name": "crag_search", "arguments": {"query": "TSan"}}'
- `test_hand3-026` fs_stat: fails json no call | 'when did i last change thesis/abstract.md?' -> 'I can do that once I know more. Which file should I check the modification time for?'
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> 'backups is a folder.'
- `test_hand3-043` unsupported: called '{"name": "fs_list", "arguments": {"path": "projects/crag"}}' | 'run the tests in projects/crag'
