# ft-1.5b-v2-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v2-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.950 [0.883, 1.000] |
| decision | 0.983 [0.961, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.90 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.95 |

Failures (first 12):

- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'
- `test_id-02103` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/checklist.md", "content": "This is the content of the checklist."}}' | 'Okay, next: Fill archive/checklist.md in.'
- `test_id-02116` ambiguous: called '{"name": "fs_write", "arguments": {"path": "drafts/checklist.py", "content": "This is the content of checklist.py."}}' | 'Fill drafts/checklist.py in.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.963, 1.000] |
| L1 json | 0.984 [0.963, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.974 [0.947, 0.995] |
| L4 args | 0.974 [0.947, 0.995] |
| abstain | 0.914 [0.857, 0.962] |
| decision | 0.959 [0.935, 0.980] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.83 |
| crag_search | 35 | 0.97 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.89 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.91 |

Failures (first 12):

- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What query should I run the search for?'
- `test_ood-00694` fs_list: fails json no call | 'What does research contain?' -> 'I can do that once I know more. What directory should I search?'
- `test_ood-00696` fs_list: fails tool  | 'What does data/raw contain?' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "fs_read", "arguments": {"path": "research"}}'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'I can do that once I know more. What directory should I search?'
- `test_ood-01947` unsupported: called '{"name": "fs_write", "arguments": {"path": "dinner.txt", "content": "Dinner is at 7."}}' | 'Text my brother that dinner is at 7. Please check.'
- `test_ood-01949` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/checklist.md"}}' | 'Translate research/checklist.md into German and save it.'
- `test_ood-01958` unsupported: called '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.toml"}}' | 'Translate scripts/notes-2026.toml into German and save it.'
- `test_ood-02119` ambiguous: called '{"name": "fs_write", "arguments": {"path": "data/raw/results.txt", "content": "This is the content of the file."}}' | 'Fill data/raw/results.txt in.'
- `test_ood-02120` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/outline.toml", "content": ""}}' | 'Fill archive/outline.toml in.'
- `test_ood-02131` ambiguous: called '{"name": "fs_write", "arguments": {"path": "research/notes-2026.txt", "content": "This is the text to be written into re' | 'Fill research/notes-2026.txt in. Please check.'
- `test_ood-02147` ambiguous: called '{"name": "fs_write", "arguments": {"path": "scripts/checklist.py", "content": "Please check."}}' | 'Fill scripts/checklist.py in. Please check.'
