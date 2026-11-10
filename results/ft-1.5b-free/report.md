# ft-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 72e7957-dirty · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.992 [0.975, 1.000] |
| L4 args | 0.992 [0.975, 1.000] |
| abstain | 0.950 [0.883, 1.000] |
| decision | 0.978 [0.956, 0.994] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.90 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.95 |

Failures (first 12):

- `test_id-00688` fs_list: fails json no call | "One more thing: What's inside archive?" -> 'Which archive are you referring to?'
- `test_id-01917` unsupported: called '{"name": "fs_write", "arguments": {"path": "research/notes-2026.md", "content": "Die Übersetzung der Datei \'research/not' | 'Translate research/notes-2026.md into German and save it.'
- `test_id-02103` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/checklist.md", "content": "This is the content of the checklist."}}' | 'Okay, next: Fill archive/checklist.md in.'
- `test_id-02116` ambiguous: called '{"name": "fs_write", "arguments": {"path": "drafts/checklist.py", "content": "This is the content of the checklist file.' | 'Fill drafts/checklist.py in.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.979 [0.958, 0.995] |
| L1 json | 0.979 [0.958, 0.995] |
| L2 schema | 0.974 [0.947, 0.995] |
| L3 tool | 0.947 [0.915, 0.979] |
| L4 args | 0.910 [0.868, 0.947] |
| abstain | 0.924 [0.867, 0.971] |
| decision | 0.959 [0.935, 0.980] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.83 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 0.57 |
| fs_list | 35 | 0.91 |
| fs_read | 35 | 0.83 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.94 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the single best hit", "k": 1}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'What should the search query be?'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00467` crag_stats: fails tool  | 'Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00471` crag_stats: fails tool  | 'Report the size of the document index. Cheers.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00473` crag_stats: fails tool  | 'Report the size of the document index. Please check.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00477` crag_stats: fails tool  | 'Report the size of the document index. Much appreciated.' -> '{"name": "fs_stat", "arguments": {"path": "index"}}'
- `test_ood-00478` crag_stats: fails schema {'path': '/query', 'keyword': 'required', 'message': 'missing required property'} | 'Hey there. Is anything actually indexed right now?' -> '{"name": "crag_search", "arguments": {}}'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> "I can't search the web: my tools can only inspect and inspect the document index, and list, read, stat or write files in the sandbox."
- `test_ood-00702` fs_list: fails json no call | 'Okay, next: What does research contain?' -> "I can't search the web: my tools can only search and inspect the document index, and list, read, stat or write files in the sandbox."
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> "I can't search the web: my tools can only search and inspect the document index, and list, read, stat or write files in the sandbox."
- `test_ood-01106` fs_read: fails args  | 'Display the file archive/results.txt for me.' -> '{"name": "fs_read", "arguments": {"path": "file/archive/results.txt"}}'
