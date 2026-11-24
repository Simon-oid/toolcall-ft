# dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.833 [0.733, 0.917] |
| decision | 0.944 [0.906, 0.978] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 0.95 |
| unsupported | 20 | 0.55 |

Failures (first 12):

- `test_id-01761` no_tool: called '{"name": "crag_search", "arguments": {"query": "2 to the power of 10"}}' | 'What is 2 to the power of 10? Please check.'
- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'
- `test_id-01919` unsupported: called '{"name": "fs_delete", "arguments": {"path": "archive/results.toml"}}' | 'Okay, next: Erase archive/results.toml from the sandbox.'
- `test_id-01922` unsupported: called '{"name": "fs_write", "arguments": {"path": "dinner.txt", "content": "Dinner is at 7."}}' | 'Text my brother that dinner is at 7.'
- `test_id-01923` unsupported: called '{"name": "fs_write", "arguments": {"path": "drafts/notes-2026.zip", "content": "This is the contents of drafts/notes-202' | 'Compress drafts/notes-2026.toml into a zip.'
- `test_id-01924` unsupported: called '{"name": "fs_write", "arguments": {"path": "scripts/readme.py", "content": ""}}' | 'Hey there. Erase scripts/readme.py from the sandbox.'
- `test_id-01925` unsupported: called '{"name": "fs_delete", "arguments": {"path": "research/notes-2026.py"}}' | 'One more thing: Erase research/notes-2026.py from the sandbox.'
- `test_id-01930` unsupported: called '{"name": "fs_write", "arguments": {"path": "scripts/proposal.zip", "content": "This is the contents of scripts/proposal.' | 'Compress scripts/proposal.md into a zip.'
- `test_id-01931` unsupported: called '{"name": "fs_write", "arguments": {"path": "archive/results.py", "content": "data/raw/invoice.md"}}' | 'Copy data/raw/invoice.md to archive/results.py. Cheers.'
- `test_id-01932` unsupported: called '{"name": "fs_delete", "arguments": {"path": "research/invoice.toml"}}' | 'Erase research/invoice.toml from the sandbox.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.995 [0.984, 1.000] |
| L1 json | 0.995 [0.984, 1.000] |
| L2 schema | 0.995 [0.984, 1.000] |
| L3 tool | 0.995 [0.984, 1.000] |
| L4 args | 0.958 [0.926, 0.984] |
| abstain | 0.819 [0.743, 0.886] |
| decision | 0.932 [0.901, 0.959] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.97 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 1.00 |
| fs_read | 35 | 0.83 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 0.97 |
| unsupported | 35 | 0.51 |

Failures (first 12):

- `test_ood-00331` crag_search: fails args  | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> '{"name": "crag_search", "arguments": {"query": "the best hit"}}'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should the query be?'
- `test_ood-01107` fs_read: fails args  | 'Everything in archive/results.toml after line 99, please.' -> '{"name": "fs_read", "arguments": {"path": "archive/results.toml", "offset": 100, "limit": 1}}'
- `test_ood-01113` fs_read: fails args  | 'Everything in data/raw/outline.txt after line 11, please.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline.txt", "offset": 12, "limit": 1}}'
- `test_ood-01126` fs_read: fails args  | 'Resume research/invoice.toml from line 5.' -> '{"name": "fs_read", "arguments": {"path": "invoice.toml", "offset": 5, "limit": 1}}'
- `test_ood-01129` fs_read: fails args  | 'Everything in data/raw/outline.toml after line 4, please.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline.toml", "offset": 5, "limit": 1}}'
- `test_ood-01130` fs_read: fails args  | 'Resume research/outline.txt from line 12.' -> '{"name": "fs_read", "arguments": {"path": "research/outline.txt", "offset": 12, "limit": 1}}'
- `test_ood-01133` fs_read: fails args  | 'Everything in drafts/notes-2026.md after line 4, please.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.md", "offset": 5, "limit": 1}}'
- `test_ood-01784` no_tool: called '{"name": "crag_search", "arguments": {"query": "a kilobyte vs a megabyte"}}' | 'Which is bigger, a kilobyte or a megabyte? Please check.'
- `test_ood-01935` unsupported: called '{"name": "fs_write", "arguments": {"path": "scripts/invoice.zip", "content": "scripts/invoice.toml"}}' | 'Compress scripts/invoice.toml into a zip.'
- `test_ood-01937` unsupported: called '{"name": "fs_write", "arguments": {"path": "archive/agenda.zip", "content": "compressing..."}}' | 'Compress archive/agenda.toml into a zip.'
- `test_ood-01939` unsupported: called '{"name": "fs_write", "arguments": {"path": "research.zip", "content": "This is the contents of readme.txt."}}' | 'One more thing: Compress research/readme.txt into a zip.'
