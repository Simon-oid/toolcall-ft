# hand2-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.906 [0.781, 1.000] |
| L2 schema | 0.844 [0.719, 0.969] |
| L3 tool | 0.781 [0.625, 0.906] |
| L4 args | 0.750 [0.594, 0.906] |
| abstain | 0.062 [0.000, 0.188] |
| decision | 0.688 [0.542, 0.812] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.00 |
| crag_search | 6 | 0.83 |
| crag_stats | 4 | 0.75 |
| fs_list | 5 | 0.60 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 0.60 |
| no_tool | 6 | 0.17 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand2-004` crag_search: fails args  | 'query the docs: TypeScript SDK benchmark' -> '{"name": "crag_search", "arguments": {"query": "TypeScript SDK benchmark", "k": 1}}'
- `test_hand2-006` crag_stats: fails schema {'path': '/query', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'how big is the search index right now, in chunks?' -> '{"name": "crag_stats", "arguments": {"query": "the search index", "k": 1}}'
- `test_hand2-010` fs_list: fails tool  | "what's in invoices/2025?" -> '{"name": "fs_read", "arguments": {"path": "invoices/2025"}}'
- `test_hand2-014` fs_list: fails json  | 'are there files in the exports folder' -> '{"name": "fs_list", "arguments": {"path": "exports"}'
- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt", "offset": 40, "limit": null}}'
- `test_hand2-025` fs_stat: fails tool  | 'is exports a file or a folder?' -> '{"name": "fs_list", "arguments": {"path": "exports"}}'
- `test_hand2-028` fs_write: fails json  | 'create drafts/blog/post-2.md containing: Coming soon' -> '{"name": "fs_write", "arguments": {"path": "drafts/blog/post-2.md", "content": "Coming soon"})'
- `test_hand2-029` fs_write: fails json  | 'save "remember the passport" in travel/checklist.txt please' -> '{"name": "fs_write", "arguments": {"path": "travel/checklist.txt", "content": "remember the passport"})'
- `test_hand2-033` no_tool: called '{"name": "math_sqrt", "arguments": {"number": 81}}' | "what's the square root of 81?"
- `test_hand2-034` no_tool: called '{"name": "fs_search", "arguments": {"query": "library" }}' | "how do you say 'library' in Spanish?"
- `test_hand2-035` no_tool: called '{"name": "crag_search", "arguments": {"query": "a name for my new laptop"}}' | 'can you suggest a name for my new laptop?'
- `test_hand2-036` no_tool: called '{"name": "fs_list", "arguments": {"path": "RAM vs storage"}}' | 'what is the difference between RAM and storage?'
