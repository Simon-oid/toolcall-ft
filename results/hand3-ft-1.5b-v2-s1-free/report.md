# hand3-ft-1.5b-v2-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-8-gf20d47e · date: 2026-11-17 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.971 [0.912, 1.000] |
| L1 json | 0.971 [0.912, 1.000] |
| L2 schema | 0.971 [0.912, 1.000] |
| L3 tool | 0.853 [0.735, 0.971] |
| L4 args | 0.853 [0.735, 0.971] |
| abstain | 0.929 [0.786, 1.000] |
| decision | 0.958 [0.896, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 0.62 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.50 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-000` fs_list: fails tool  | 'what does photos contain' -> '{"name": "crag_search", "arguments": {"query": "photos"}}'
- `test_hand3-001` fs_list: fails tool  | 'anything in backups?' -> '{"name": "crag_search", "arguments": {"query": "backups"}}'
- `test_hand3-002` fs_list: fails tool  | 'whats under recipes/italian' -> '{"name": "fs_read", "arguments": {"path": "recipes/italian"}}'
- `test_hand3-026` fs_stat: fails tool  | 'when did i last change thesis/abstract.md?' -> '{"name": "crag_search", "arguments": {"query": "thesis/abstract.md"}}'
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> 'The word "backups" is not a folder or a file, it is a noun.'
- `test_hand3-043` unsupported: called '{"name": "crag_search", "arguments": {"query": "projects/crag"}}' | 'run the tests in projects/crag'
