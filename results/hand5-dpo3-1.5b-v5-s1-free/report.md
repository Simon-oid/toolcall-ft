# hand5-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.762 [0.571, 0.905] |
| L1 json | 0.762 [0.571, 0.905] |
| L2 schema | 0.667 [0.476, 0.857] |
| L3 tool | 0.619 [0.381, 0.810] |
| L4 args | 0.571 [0.333, 0.762] |
| abstain | 0.889 [0.722, 1.000] |
| decision | 0.821 [0.692, 0.923] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.86 |
| crag_search | 5 | 0.20 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 0.80 |
| fs_stat | 3 | 0.67 |
| fs_write | 3 | 0.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand5-006` fs_stat: fails tool  | 'check the permissions and size of the logs/ directory' -> '{"name": "fs_list", "arguments": {"path": "logs/"}}'
- `test_hand5-007` crag_search: fails json no call | 'search the knowledge base for documents about retry logic and exponential backoff' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "retry logic and exponential backoff"}}'
- `test_hand5-008` crag_search: fails json no call | 'find anything in the docs related to authentication tokens' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "authentication tokens", "path": "docs"}}'
- `test_hand5-012` fs_write: fails json no call | 'create a file called notes/meeting.md with the text "Action items from Nov 21 standup"' -> '<tool_call>\n{"name": "fs_write", "arguments": {"path": "notes/meeting.md", "content": "Action items from Nov 21 standup"}}ьер'
- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"path": "afile.txt", "content": "__pycache__\\n.env"}}'
- `test_hand5-016` crag_search: fails json no call | 'search for anything about vector similarity and cosine distance' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "vector similarity and cosine distance"}}'
- `test_hand5-017` fs_read: fails schema {'path': '/offset', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'show me 20 lines of logs/server.log starting at line 80' -> '{"name": "crag_search", "arguments": {"query": "logs/server.log", "k": 20, "offset": 80}}'
- `test_hand5-019` fs_write: fails json no call | 'write a file at tmp/scratch.txt with "quick test" as content' -> '<tool_call>\n{"name": "fs_write", "arguments": {"path": "tmp/scratch.txt", "content": "quick test"}}ьер'
- `test_hand5-020` crag_search: fails schema {'path': '/additionalProperties', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "additionalProperties": false, "properties": {"k": {"maximum": 20, "minimum": 1'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config", "match": "not the main one"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-034` ambiguous: called '{"name": "fs_list", "arguments": {"path": "output"}}' | "check what's inside the output directory — you know which one"
