# hand2-gptoss120b-low-api

model: openai/gpt-oss-120b · gguf: gpt-oss-120b · decoding: hosted API, native tool calling, temperature 0 · llama.cpp: hosted API https://api.groq.com/openai/v1, reasoning_effort low · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.875 [0.750, 0.969] |
| abstain | 0.812 [0.625, 1.000] |
| decision | 0.938 [0.854, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.60 |
| crag_search | 6 | 0.67 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 0.80 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 1.00 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand2-001` crag_search: fails args  | 'look for anything about SQLite FTS5 in the knowledge base' -> '{"name": "crag_search", "arguments": {"k":10,"query":"SQLite FTS5"}}'
- `test_hand2-004` crag_search: fails args  | 'query the docs: TypeScript SDK benchmark' -> '{"name": "crag_search", "arguments": {"k":10,"query":"TypeScript SDK benchmark"}}'
- `test_hand2-012` fs_list: fails args  | 'list music' -> '{"name": "fs_list", "arguments": {"path":""}}'
- `test_hand2-017` fs_read: fails args  | 'what does the first line of exports/summary.txt say?' -> '{"name": "fs_read", "arguments": {"path":"exports/summary.txt"}}'
- `test_hand2-040` unsupported: called '{"name": "fs_list", "arguments": {"path":""}}' | 'zip the exports folder'
- `test_hand2-045` ambiguous: called '{"name": "fs_list", "arguments": {"path":""}}' | 'list it'
- `test_hand2-046` ambiguous: called '{"name": "crag_search", "arguments": {"k":5,"query":"how big is it"}}' | 'how big is it?'
