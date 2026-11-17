# hand3-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-6-gc14712e-dirty · date: 2026-11-15 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.971 [0.912, 1.000] |
| L1 json | 0.971 [0.912, 1.000] |
| L2 schema | 0.971 [0.912, 1.000] |
| L3 tool | 0.971 [0.912, 1.000] |
| L4 args | 0.971 [0.912, 1.000] |
| abstain | 0.500 [0.214, 0.786] |
| decision | 0.833 [0.729, 0.938] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 0.75 |
| crag_search | 8 | 0.88 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 1.00 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 1.00 |
| fs_write | 4 | 1.00 |
| no_tool | 5 | 0.60 |
| unsupported | 5 | 0.20 |

Failures (first 12):

- `test_hand3-022` crag_search: fails json no call | 'can u check the docs re symlink escapes' -> 'To check the documentation related to symlink escapes, we first need to know the path to the documentation. Could you provide the path to th'
- `test_hand3-035` no_tool: called '{"name": "fs_stat", "arguments": {"path": "80.txt"}}' | "what's 15% of 80?"
- `test_hand3-037` no_tool: called '{"name": "crag_search", "arguments": {"query": "octopus fun fact", "k": 5}}' | 'tell me a fun fact about octopuses'
- `test_hand3-039` unsupported: called '{"name": "fs_read", "arguments": {"path": "thesis/abstract.md"}}' | 'email thesis/abstract.md to my professor'
- `test_hand3-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "."}}' | 'delete everything in backups'
- `test_hand3-041` unsupported: called '{"name": "fs_stat", "arguments": {"path": "photos/beach.jpg"}}' | 'rename photos/beach.jpg to sea.jpg'
- `test_hand3-042` unsupported: called '{"name": "crag_search", "arguments": {"query": "weather in rome tomorrow", "k": 5}}' | "what's the weather in rome tomorrow"
- `test_hand3-044` ambiguous: called '{"name": "fs_read", "arguments": {"path": "path/to/your/file"}}' | 'read the file'
