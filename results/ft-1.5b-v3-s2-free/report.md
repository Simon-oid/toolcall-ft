# ft-1.5b-v3-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v3-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-8-gf20d47e · date: 2026-11-17 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.983 [0.950, 1.000] |
| decision | 0.994 [0.983, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.95 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 1.00 |

Failures (first 12):

- `test_id-02103` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/checklist.md", "content": "This is the checklist for the project."}}' | 'Okay, next: Fill archive/checklist.md in.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.995 [0.984, 1.000] |
| L1 json | 0.995 [0.984, 1.000] |
| L2 schema | 0.995 [0.984, 1.000] |
| L3 tool | 0.989 [0.974, 1.000] |
| L4 args | 0.974 [0.947, 0.995] |
| abstain | 0.895 [0.829, 0.952] |
| decision | 0.959 [0.935, 0.980] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.71 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 0.97 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.97 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.97 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the best hit", "k": 1}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. Which text should I search the documentation for?'
- `test_ood-00351` crag_search: fails args  | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> '{"name": "crag_search", "arguments": {"query": "the query", "k": 2}}'
- `test_ood-01107` fs_read: fails tool  | 'Everything in archive/results.toml after line 99, please.' -> '{"name": "crag_search", "arguments": {"query": "archive/results.toml after line 99", "k": 1}}'
- `test_ood-01575` fs_write: fails args  | 'Hey there. Could you write archive/agenda.md? It should say: all tests passing' -> '{"name": "fs_write", "arguments": {"path": "agenda.md", "content": "all tests passing"}}'
- `test_ood-01947` unsupported: called '{"name": "fs_write", "arguments": {"path": "dinner.txt", "content": "Dinner is at 7."}}' | 'Text my brother that dinner is at 7. Please check.'
- `test_ood-02119` ambiguous: called '{"name": "fs_write", "arguments": {"path": "data/raw/results.txt", "content": "This is the content of the file."}}' | 'Fill data/raw/results.txt in.'
- `test_ood-02120` ambiguous: called '{"name": "fs_write", "arguments": {"path": "archive/outline.toml", "content": "This is the content of the outline file."' | 'Fill archive/outline.toml in.'
- `test_ood-02126` ambiguous: called '{"name": "crag_search", "arguments": {"query": "that"}}' | 'Find the part about that in the docs. Cheers.'
- `test_ood-02128` ambiguous: called '{"name": "crag_search", "arguments": {"query": "that"}}' | 'Find the part about that in the docs.'
- `test_ood-02129` ambiguous: called '{"name": "fs_write", "arguments": {"path": "drafts/outline.py", "content": "This is the outline for the document."}}' | 'Okay, next: Fill drafts/outline.py in.'
- `test_ood-02131` ambiguous: called '{"name": "fs_write", "arguments": {"path": "research/notes-2026.txt", "content": "This is the content of notes-2026.txt.' | 'Fill research/notes-2026.txt in. Please check.'
