# hand5-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 39

## test_hand5 (21 need a call, 18 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.905 [0.762, 1.000] |
| abstain | 0.000 [0.000, 0.000] |
| decision | 0.538 [0.385, 0.692] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 14 | 0.00 |
| crag_search | 5 | 0.80 |
| crag_stats | 2 | 1.00 |
| fs_list | 3 | 1.00 |
| fs_read | 5 | 1.00 |
| fs_stat | 3 | 1.00 |
| fs_write | 3 | 0.67 |
| no_tool | 2 | 0.00 |
| unsupported | 2 | 0.00 |

Failures (first 12):

- `test_hand5-013` fs_write: fails args  | 'write a .gitignore file that contains __pycache__/ and .env on separate lines' -> '{"name": "fs_write", "arguments": {"path": "a.gitignore", "content": "__pycache__\\n.\\\\env\\n"}}'
- `test_hand5-020` crag_search: fails args  | 'find the part about deployment in the docs, the one with the diagram' -> '{"name": "crag_search", "arguments": {"query": "deployment", "k": 1}}'
- `test_hand5-021` ambiguous: called '{"name": "fs_list", "arguments": {"path": "docs"}}' | 'can you read that file I mentioned earlier?'
- `test_hand5-022` ambiguous: called '{"name": "crag_search", "arguments": {"query": "it in the knowledge base"}}' | 'search for it in the knowledge base'
- `test_hand5-023` ambiguous: called '{"name": "fs_list", "arguments": {"path": "sandbox"}}' | 'write that summary to a file'
- `test_hand5-024` ambiguous: called '{"name": "fs_list", "arguments": {"path": "config", "exclude": "main"}' | 'show me the contents of the config file — not the main one, the other one'
- `test_hand5-025` ambiguous: called '{"name": "fs_list", "arguments": {"path": "that folder"}}' | 'check the stats on that folder'
- `test_hand5-026` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the error we were discussing"}}' | 'look up the error we were discussing'
- `test_hand5-027` ambiguous: called '{"name": "crag_search", "arguments": {"query": "the relevant section of the documentation"}}' | 'read the relevant section of the documentation'
- `test_hand5-028` ambiguous: called '{"name": "fs_write", "arguments": {"path": "docs/faq.md", "content": "this is docs/faq.md"}' | 'I need you to save this somewhere as a markdown file'
- `test_hand5-029` ambiguous: called '{"name": "crag_search", "arguments": {"query": "actually the topic I told you before", "k": 5}}' | 'search the knowledge base for 5 results about... actually the topic I told you before'
- `test_hand5-030` ambiguous: called '{"name": "fs_read", "arguments": {"path": "docs/README.md", "offset": 10, "limit": 5}}' | 'can you read the lines around the function definition?'
