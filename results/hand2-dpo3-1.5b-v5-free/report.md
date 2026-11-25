# hand2-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.906 [0.781, 1.000] |
| L3 tool | 0.625 [0.469, 0.781] |
| L4 args | 0.625 [0.469, 0.781] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 0.33 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 0.80 |
| fs_read | 8 | 0.38 |
| fs_stat | 4 | 1.00 |
| fs_write | 5 | 0.60 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand2-001` crag_search: fails tool  | 'look for anything about SQLite FTS5 in the knowledge base' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand2-002` crag_search: fails tool  | 'what do the docs say re: the modern protocol era? just 2 results is fine' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand2-004` crag_search: fails tool  | 'query the docs: TypeScript SDK benchmark' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand2-005` crag_search: fails tool  | 'I need the parts of the docs about structured logging, give me 6' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand2-011` fs_list: fails schema  | 'show the contents of the top-level directory' -> '{"name": "crag", "arguments": {}}'
- `test_hand2-015` fs_read: fails tool  | 'can you read invoices/2025/march.csv to me' -> '{"name": "fs_stat", "arguments": {"path": "invoices/2025/march.csv"}}'
- `test_hand2-016` fs_read: fails schema  | 'open drafts/blog/post-1.md' -> '{"name": "drafts/blog/post-1.md", "arguments": {}}'
- `test_hand2-020` fs_read: fails tool  | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_stat", "arguments": {"path": "exports/summary.txt"}}'
- `test_hand2-021` fs_read: fails tool  | 'I need line 3 of keys.txt' -> '{"name": "fs_stat", "arguments": {"path": "keys.txt"}}'
- `test_hand2-022` fs_read: fails tool  | 'print travel/itinerary.md, thanks' -> '{"name": "fs_stat", "arguments": {"path": "travel/itinerary.md"}}'
- `test_hand2-027` fs_write: fails schema  | "write 'flight at 7:40' to travel/notes.txt" -> '{"name": "fs_prompt", "arguments": {"whatfile": "travel/notes.txt"}}'
- `test_hand2-030` fs_write: fails tool  | 'replace the contents of keys.txt with: rotated' -> '{"name": "fs_stat", "arguments": {"path": "keys.txt"}}'
