# hand5-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-12-ga660538 · date: 2026-11-21 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.952 [0.857, 1.000] |
| L3 tool | 0.762 [0.571, 0.905] |
| L4 args | 0.619 [0.429, 0.810] |
| abstain | 0.556 [0.333, 0.778] |
| decision | 0.795 [0.667, 0.923] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.50 |
| crag_search | 5 | 0.40 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 0.20 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 0.67 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 0.50 |

Failures (first 12):

- `test_hand5-003` fs_read: fails tool  | 'can you show me lines 25 through 40 of src/main.py?' -> '{"name": "fs_list", "arguments": {"path": "src/main.py"}}'
- `test_hand5-004` fs_read: fails tool  | 'give me just the first 10 lines of README.md' -> '{"name": "fs_list", "arguments": {"path": "README.md"}}'
- `test_hand5-007` crag_search: fails args  | 'search the knowledge base for documents about retry logic and exponential backoff' -> '{"name": "crag_search", "arguments": {"query": "retry logic", "k": 5}}'
- `test_hand5-008` crag_search: fails args  | 'find anything in the docs related to authentication tokens' -> '{"name": "crag_search", "arguments": {"query": "authentication tokens", "k": 5}}'
- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"content": "__pycache__/\\n.env", "path": "/path/to/.gitignore"}}'
- `test_hand5-015` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read experiments/results.json please' -> '{"name": "fs_read", "arguments": {"limit": null, "offset": null, "path": "experiments/results.json"}}'
- `test_hand5-017` fs_read: fails tool  | 'show me 20 lines of logs/server.log starting at line 80' -> '{"name": "fs_list", "arguments": {"path": "logs/server.log"}}'
- `test_hand5-020` crag_search: fails tool  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "fs_list", "arguments": {"path": "docs/deployment.md"}}'
- `test_hand5-022` ambiguous: called '{"name": "crag_search", "arguments": {"query": "it in the knowledge base", "k": 5}}' | 'search for it in the knowledge base'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config"}}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-025` ambiguous: called '{"name": "crag_stats", "arguments": {"path": "folder_path"}}' | 'check the stats on that folder'
- `test_hand5-027` ambiguous: called '{"name": "fs_read", "arguments": {"path": "documentation/crags.md", "offset": 100, "limit": 100}}' | 'read the relevant section of the documentation'
