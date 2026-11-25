# hand5-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.952 [0.857, 1.000] |
| L1 json | 0.952 [0.857, 1.000] |
| L2 schema | 0.905 [0.762, 1.000] |
| L3 tool | 0.476 [0.238, 0.667] |
| L4 args | 0.429 [0.238, 0.619] |
| abstain | 0.889 [0.722, 1.000] |
| decision | 0.923 [0.821, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.93 |
| crag_search | 5 | 0.20 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 0.67 |
| fs_read | 5 | 0.20 |
| fs_stat | 3 | 0.67 |
| fs_write | 3 | 0.33 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 0.50 |

Failures (first 12):

- `test_hand5-000` fs_list: fails json no call | 'show me the top-level directory listing' -> 'What should the file be called?'
- `test_hand5-002` fs_read: fails tool  | 'read the file config.yaml for me' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand5-004` fs_read: fails tool  | 'give me just the first 10 lines of README.md' -> '{"name": "fs_stat", "arguments": {"path": "README.md"}}'
- `test_hand5-006` fs_stat: fails tool  | 'check the permissions and size of the logs/ directory' -> '{"name": "fs_list", "arguments": {"path": "logs/"}}'
- `test_hand5-007` crag_search: fails tool  | 'search the knowledge base for documents about retry logic and exponential backoff' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand5-008` crag_search: fails tool  | 'find anything in the docs related to authentication tokens' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand5-012` fs_write: fails schema  | 'create a file called notes/meeting.md with the text "Action items from Nov 21 standup"' -> '{"name": "fs_prompt", "arguments": {"prompt": "The text to save in notes/meeting.md: "}}'
- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"path": "afile.txt", "content": "__pycache__\\n.env"}}'
- `test_hand5-015` fs_read: fails tool  | 'read experiments/results.json please' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand5-016` crag_search: fails tool  | 'search for anything about vector similarity and cosine distance' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand5-017` fs_read: fails tool  | 'show me 20 lines of logs/server.log starting at line 80' -> '{"name": "fs_stat", "arguments": {"path": "logs/server.log"}}'
- `test_hand5-020` crag_search: fails tool  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_stats", "arguments": {}}'
