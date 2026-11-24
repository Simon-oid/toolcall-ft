# hand4-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.950 [0.850, 1.000] |
| L3 tool | 0.950 [0.850, 1.000] |
| L4 args | 0.950 [0.850, 1.000] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.500 [0.350, 0.650] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 0.00 |
| crag_search | 5 | 1.00 |
| crag_stats | 2 | 0.50 |
| fs_list | 5 | 1.00 |
| fs_read | 3 | 1.00 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 1.00 |
| no_tool | 2 | 0.00 |
| unsupported | 2 | 0.00 |

Failures (first 12):

- `test_hand4-000` ambiguous: called '{"name": "crag_search", "arguments": {"query": "it"}}' | 'grab the bit about it from the docs'
- `test_hand4-001` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the stuff we covered"}}' | 'search the knowledge base for the stuff we covered'
- `test_hand4-002` ambiguous: called '{"name": "crag_search", "arguments": {"query": "top 2"}}' | 'look that up for me, top 2'
- `test_hand4-003` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the same thing as before", "k": 1}}' | 'check the index for the same thing as before. one hit'
- `test_hand4-004` ambiguous: called '{"name": "crag_stats", "arguments": {}' | 'pull up whatever we found last time'
- `test_hand4-005` ambiguous: called '{"name": "fs_list", "arguments": {"path": "that_folder_name"}}' | "what's inside that folder?"
- `test_hand4-006` ambiguous: called '{"name": "fs_list", "arguments": {"path": "there"}}' | "list what's in there"
- `test_hand4-007` ambiguous: called '{"name": "fs_list", "arguments": {"path": "other"}}' | 'show me the contents of the other directory'
- `test_hand4-008` ambiguous: called '{"name": "fs_list", "arguments": {"path": "reports"}}' | 'fill in the report'
- `test_hand4-009` ambiguous: called '{"name": "fs_write", "arguments": {"path": "notes/todo.md", "content": "this is the contents of notes/todo.md"}' | 'write it to notes/todo.md'
- `test_hand4-010` ambiguous: called '{"name": "fs_write", "arguments": {"path": "journal/today.md", "content": "I wrote this in today\'s journal."}}' | 'add a line to journal/today.md'
- `test_hand4-011` ambiguous: called '{"name": "fs_write", "arguments": {"path": "somewhere", "content": "pick up the keys"}}' | "save 'pick up the keys' somewhere"
