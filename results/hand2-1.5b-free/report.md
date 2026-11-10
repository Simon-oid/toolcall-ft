# hand2-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 4150f57-dirty · date: 2026-11-10 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.938 [0.844, 1.000] |
| L3 tool | 0.875 [0.750, 0.969] |
| L4 args | 0.844 [0.719, 0.969] |
| abstain | 0.625 [0.375, 0.875] |
| decision | 0.875 [0.771, 0.958] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.40 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 0.75 |
| fs_list | 5 | 0.80 |
| fs_read | 8 | 0.75 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 0.67 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand2-006` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'how big is the search index right now, in chunks?' -> '{"name": "crag_stats", "arguments": {"path": "index"}}'
- `test_hand2-011` fs_list: fails args  | 'show the contents of the top-level directory' -> '{"name": "fs_list", "arguments": {"path": "/"}}'
- `test_hand2-019` fs_read: fails tool  | 'show me the first 25 lines of music/playlist.m3u' -> '{"name": "fs_list", "arguments": {"path": "music/playlist.m3u"}}'
- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"limit": null, "offset": 40, "path": "exports/summary.txt"}}'
- `test_hand2-025` fs_stat: fails tool  | 'is exports a file or a folder?' -> '{"name": "fs_list", "arguments": {"path": "exports"}}'
- `test_hand2-034` no_tool: called '{"name": "crag_search", "arguments": {"query": "library Spanish", "k": 1}}' | "how do you say 'library' in Spanish?"
- `test_hand2-036` no_tool: called '{"name": "crag_search", "arguments": {"query": "difference between RAM and storage"}}' | 'what is the difference between RAM and storage?'
- `test_hand2-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "exports"}}' | 'zip the exports folder'
- `test_hand2-043` ambiguous: called '{"name": "fs_list", "arguments": {"path": "path/to/mentioned/file"}}' | 'open the one I mentioned earlier'
- `test_hand2-045` ambiguous: called '{"name": "fs_list", "arguments": {"path": "/"}}' | 'list it'
- `test_hand2-046` ambiguous: called '{"name": "fs_stat", "arguments": {"path": "/path/to/your/file"}}' | 'how big is it?'
