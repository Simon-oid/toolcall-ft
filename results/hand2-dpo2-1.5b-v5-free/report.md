# hand2-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.969 [0.906, 1.000] |
| L3 tool | 0.969 [0.906, 1.000] |
| L4 args | 0.969 [0.906, 1.000] |
| abstain | 0.125 [0.000, 0.312] |
| decision | 0.708 [0.583, 0.833] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.00 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 1.00 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 0.33 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt", "offset": 40, "limit": null}}'
- `test_hand2-033` no_tool: called '{"name": "math_sqrt", "arguments": {"number": 81}}' | "what's the square root of 81?"
- `test_hand2-034` no_tool: called '{"name": "crag_search", "arguments": {"query": "library", "language": "es"}}' | "how do you say 'library' in Spanish?"
- `test_hand2-035` no_tool: called '{"name": "crag_search", "arguments": {"query": "a name for my new laptop"}}' | 'can you suggest a name for my new laptop?'
- `test_hand2-036` no_tool: called '{"name": "crag_search", "arguments": {"query": "the difference between RAM and storage"}}' | 'what is the difference between RAM and storage?'
- `test_hand2-038` unsupported: called '{"name": "fs_write", "arguments": {"path": "the-trash-folder", "content": ""}}' | 'move keys.txt into the trash folder and empty it'
- `test_hand2-039` unsupported: called '{"name": "fs_write", "arguments": {"path": "Twitter.txt", "content": "my blog draft"}}' | 'post my blog draft on Twitter'
- `test_hand2-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "exports"}}' | 'zip the exports folder'
- `test_hand2-041` unsupported: called '{"name": "crag_search", "arguments": {"query": "the stock price of AMD today"}}' | "what's the stock price of AMD today?"
- `test_hand2-042` unsupported: called '{"name": "fs_list", "arguments": {"path": "processes"}}' | "kill the process that's using port 8080"
- `test_hand2-043` ambiguous: called '{"name": "fs_list", "arguments": {"path": "old"}}' | 'open the one I mentioned earlier'
- `test_hand2-044` ambiguous: called '{"name": "fs_write", "arguments": {"path": "example.txt", "content": "This is the content of example.txt."}}' | 'write it to a file'
