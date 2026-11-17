# hand3-ft-1.5b-v2-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-8-gf20d47e · date: 2026-11-17 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.971 [0.912, 1.000] |
| L1 json | 0.971 [0.912, 1.000] |
| L2 schema | 0.971 [0.912, 1.000] |
| L3 tool | 0.912 [0.794, 1.000] |
| L4 args | 0.912 [0.794, 1.000] |
| abstain | 0.786 [0.571, 1.000] |
| decision | 0.917 [0.833, 0.979] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 0.50 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 0.75 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-000` fs_list: fails tool  | 'what does photos contain' -> '{"name": "fs_read", "arguments": {"path": "photos"}}'
- `test_hand3-002` fs_list: fails tool  | 'whats under recipes/italian' -> '{"name": "fs_read", "arguments": {"path": "recipes/italian"}}'
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> 'backups is a folder.'
- `test_hand3-043` unsupported: called '{"name": "fs_read", "arguments": {"path": "projects/crag"}}' | 'run the tests in projects/crag'
- `test_hand3-045` ambiguous: called '{"name": "fs_list", "arguments": {}}' | "what's in it?"
- `test_hand3-047` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the thing we talked about"}}' | 'search for the thing we talked about'
