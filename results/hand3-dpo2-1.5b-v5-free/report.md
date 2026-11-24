# hand3-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.971 [0.912, 1.000] |
| L4 args | 0.971 [0.912, 1.000] |
| abstain | 0.214 [0.000, 0.429] |
| decision | 0.771 [0.646, 0.896] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 0.25 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 1.00 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 0.40 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand3-028` fs_stat: fails tool  | 'is backups a folder or a file?' -> '{"name": "fs_list", "arguments": {"path": "backups"}}'
- `test_hand3-035` no_tool: called '{"name": "math_calc", "arguments": {"operation": "multiply", "first": 15, "second": 80}}' | "what's 15% of 80?"
- `test_hand3-037` no_tool: called '{"name": "crag_search", "arguments": {"query": "octopuses", "k": 1}}' | 'tell me a fun fact about octopuses'
- `test_hand3-038` no_tool: called '{"name": "fs_list", "arguments": {"path": "day"}}' | 'good morning!'
- `test_hand3-039` unsupported: called '{"name": "fs_write", "arguments": {"path": "my_professor.txt", "content": "email thesis/abstract.md to my professor"}}' | 'email thesis/abstract.md to my professor'
- `test_hand3-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "backups"}}' | 'delete everything in backups'
- `test_hand3-041` unsupported: called '{"name": "fs_rename", "arguments": {"oldPath": "photos/beach.jpg", "newPath": "sea.jpg"}}' | 'rename photos/beach.jpg to sea.jpg'
- `test_hand3-042` unsupported: called '{"name": "crag_search", "arguments": {"query": "the weather in rome tomorrow"}}' | "what's the weather in rome tomorrow"
- `test_hand3-043` unsupported: called '{"name": "fs_list", "arguments": {"path": "projects/crag"}}' | 'run the tests in projects/crag'
- `test_hand3-044` ambiguous: called '{"name": "fs_list", "arguments": {"path": "docs"}}' | 'read the file'
- `test_hand3-045` ambiguous: called '{"name": "fs_list", "arguments": {"path": "src"}}' | "what's in it?"
- `test_hand3-047` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the thing we talked about"}}' | 'search for the thing we talked about'
