# ft-1.5b-v6-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.983 [0.958, 1.000] |
| L1 json | 0.983 [0.958, 1.000] |
| L2 schema | 0.983 [0.958, 1.000] |
| L3 tool | 0.983 [0.958, 1.000] |
| L4 args | 0.983 [0.958, 1.000] |
| abstain | 0.967 [0.917, 1.000] |
| decision | 0.978 [0.956, 0.994] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.90 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.90 |

Failures (first 12):

- `test_id-00682` fs_list: fails json no call | "Okay, next: What's inside archive?" -> 'Which folder do you mean?'
- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'I can do that once I know more. Which folder should I look in?'
- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'
- `test_id-01931` unsupported: called '{"name": "fs_write", "arguments": {"path": "archive/results.py", "content": "data/raw/invoice.md"}}' | 'Copy data/raw/invoice.md to archive/results.py. Cheers.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.963 [0.937, 0.989] |
| L1 json | 0.963 [0.937, 0.989] |
| L2 schema | 0.963 [0.937, 0.989] |
| L3 tool | 0.963 [0.937, 0.989] |
| L4 args | 0.947 [0.910, 0.974] |
| abstain | 0.971 [0.933, 1.000] |
| decision | 0.966 [0.946, 0.986] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.83 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.97 |
| fs_read | 35 | 0.91 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.91 |

Failures (first 12):

- `test_ood-00321` crag_search: fails json no call | 'Run a retrieval on the soak test, please.' -> 'What should I look up in the docs?'
- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'Happy to help. What should I search the documentation for?'
- `test_ood-00343` crag_search: fails json no call | 'Okay, next: Run a retrieval on the soak test, please.' -> 'What should I look up in the docs?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I search the documentation for?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I search the documentation for?'
- `test_ood-00353` crag_search: fails json no call | 'Run a retrieval on nDCG evaluation, please. Just the single best hit.' -> 'What should I search the documentation for?'
- `test_ood-00700` fs_list: fails json no call | 'Hey there. What does the base directory contain?' -> 'I can do that once I know more. Which folder should I look in?'
- `test_ood-01106` fs_read: fails args  | 'Display the file archive/results.txt for me.' -> '{"name": "fs_read", "arguments": {"path": "file/archive/results.txt"}}'
- `test_ood-01122` fs_read: fails args  | 'Display the file archive/readme.py for me.' -> '{"name": "fs_read", "arguments": {"path": "file/archive/readme.py"}}'
- `test_ood-01126` fs_read: fails args  | 'Resume research/invoice.toml from line 5.' -> '{"name": "fs_read", "arguments": {"path": "invoice.toml", "offset": 5}}'
- `test_ood-01949` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/checklist.md"}}' | 'Translate research/checklist.md into German and save it.'
- `test_ood-01958` unsupported: called '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.toml"}}' | 'Translate scripts/notes-2026.toml into German and save it.'
