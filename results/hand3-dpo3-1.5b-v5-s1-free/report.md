# hand3-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.824 [0.676, 0.941] |
| L1 json | 0.794 [0.647, 0.912] |
| L2 schema | 0.765 [0.618, 0.912] |
| L3 tool | 0.765 [0.618, 0.912] |
| L4 args | 0.765 [0.618, 0.912] |
| abstain | 0.929 [0.786, 1.000] |
| decision | 0.854 [0.750, 0.938] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 0.88 |
| crag_stats | 3 | 0.67 |
| fs_list | 8 | 0.75 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.25 |
| fs_write | 4 | 0.75 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand3-000` fs_list: fails json no call | 'what does photos contain' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "photos"}}'
- `test_hand3-007` fs_list: fails json no call | 'which files does homework have?' -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "homework"}}'
- `test_hand3-020` crag_search: fails json no call | 'pls search for the threat model' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the threat model"}}'
- `test_hand3-025` crag_stats: fails schema {'path': '/name', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | "what's the embedding dim of the index" -> '{"name": "crag_stats", "arguments": {"name": "the index"}}'
- `test_hand3-026` fs_stat: fails json no call | 'when did i last change thesis/abstract.md?' -> "I can't find the command to check when a file was last changed. Crag doesn't have a tool for that."
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> '<tool_call>'
- `test_hand3-029` fs_stat: fails json no call | 'permissions of recipes/carbonara.md?' -> "I can't find a command to check the permissions. My tools can only search and inspect the document index, and list, read, stat or write file"
- `test_hand3-030` fs_write: fails json  | "write 'call mum on sunday' to todo/today.md" -> '{"name": "fs_write", "arguments": {"path": "todo/today.md", "content": "call mum on sunday"}}}'
- `test_hand3-043` unsupported: called '{"name": "fs_list", "arguments": {"path": "projects/crag"}}' | 'run the tests in projects/crag'
