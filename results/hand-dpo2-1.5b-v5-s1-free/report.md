# hand-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.872 [0.769, 0.974] |
| L2 schema | 0.846 [0.718, 0.949] |
| L3 tool | 0.795 [0.667, 0.923] |
| L4 args | 0.744 [0.590, 0.872] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.722 [0.593, 0.833] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.00 |
| crag_search | 8 | 0.75 |
| crag_stats | 4 | 0.75 |
| fs_list | 6 | 0.67 |
| fs_read | 10 | 0.80 |
| fs_stat | 5 | 0.80 |
| fs_write | 6 | 0.67 |
| no_tool | 5 | 0.00 |
| unsupported | 5 | 0.00 |

Failures (first 12):

- `test_hand-001` crag_search: fails json  | "what's the deal with Streamable HTTP in cMCP? look it up" -> '{"name": "crag_search", "arguments": {"query": "Streamable HTTP in cMCP"}'
- `test_hand-007` crag_search: fails tool  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "fs_list", "arguments": {"path": "cmcp-tee"}}'
- `test_hand-010` crag_stats: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | "what's the vector dimension of the embeddings in the index" -> '{"name": "crag_stats", "arguments": {"path": "index"}}'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-017` fs_list: fails json  | 'Can you tell me which files are in the photos directory?' -> '{"name": "fs_list", "arguments": {"path": "photos"}'
- `test_hand-022` fs_read: fails args  | 'show the bottom part of notes.txt starting from line 50' -> '{"name": "fs_read", "arguments": {"path": "notes.txt", "offset": 50, "limit": 10}}'
- `test_hand-027` fs_read: fails json  | 'dump letters/cover-letter.txt' -> '{"name": "fs_write", "arguments": {"path": "letters/cover-letter.txt", "content": "Dear Sir,\\n\\nI am writing to inquire about the possibilit'
- `test_hand-030` fs_stat: fails tool  | 'is photos/2026 a directory?' -> '{"name": "fs_list", "arguments": {"path": "photos/2026"}}'
- `test_hand-035` fs_write: fails json  | 'write the following to projects/website/robots.txt: User-agent: *' -> '{"name": "fs_write", "arguments": {"path": "projects/website/robots.txt", "content": "User-agent: *"})'
- `test_hand-037` fs_write: fails json  | 'overwrite reminders.txt so it contains just the word: done' -> '{"name": "fs_write", "arguments": {"path": "reminders.txt", "content": "done"}'
- `test_hand-039` no_tool: called '{"name": "crag_search", "arguments": {"query": "lol thanks that worked"}}' | 'lol thanks that worked'
- `test_hand-040` no_tool: called '{"name": "crag_search", "arguments": {"query": "binary search time complexity"}}' | "what's the time complexity of binary search?"
