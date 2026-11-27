# grpo-1.5b-v7-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: grpo-1.5b-v7-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-39-g8902c62-dirty · date: 2026-11-27 · cases: 474

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
| ambiguous | 20 | 1.00 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 1.00 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 1.00 |
| unsupported | 20 | 0.85 |

Failures (first 12):

- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'
- `test_id-01919` unsupported: called '{"name": "fs_write", "arguments": {"path": "archive/results.toml", "content": ""}}' | 'Okay, next: Erase archive/results.toml from the sandbox.'
- `test_id-01925` unsupported: called '{"name": "fs_delete", "arguments": {"path": "research/notes-2026.py"}}' | 'One more thing: Erase research/notes-2026.py from the sandbox.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.979 [0.958, 0.995] |
| L1 json | 0.979 [0.958, 0.995] |
| L2 schema | 0.979 [0.958, 0.995] |
| L3 tool | 0.979 [0.958, 0.995] |
| L4 args | 0.968 [0.942, 0.989] |
| abstain | 0.971 [0.933, 1.000] |
| decision | 0.976 [0.959, 0.993] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 1.00 |
| crag_search | 35 | 0.91 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.91 |
| fs_read | 35 | 1.00 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 1.00 |
| unsupported | 35 | 0.91 |

Failures (first 12):

- `test_ood-00331` crag_search: fails json no call | 'One more thing: Run a retrieval on the HNSW index, please. Just the single best hit.' -> 'What should I look up?'
- `test_ood-00349` crag_search: fails json no call | 'One more thing: Run a retrieval on structured tool output, please.' -> 'I can do that once I know more. What should I look up?'
- `test_ood-00351` crag_search: fails json no call | 'Run a retrieval on the HNSW index, please. Give me 2 results.' -> 'What should I search the docs for?'
- `test_ood-00690` fs_list: fails args  | 'What does the sandbox root contain?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'I can do that once I know more. Which folder should I look in?'
- `test_ood-00716` fs_list: fails args  | 'Hey there. What does the sandbox root contain?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_ood-01949` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/checklist.md"}}' | 'Translate research/checklist.md into German and save it.'
- `test_ood-01958` unsupported: called '{"name": "fs_read", "arguments": {"path": "scripts/notes-2026.toml"}}' | 'Translate scripts/notes-2026.toml into German and save it.'
- `test_ood-01959` unsupported: called '{"name": "fs_read", "arguments": {"path": "archive/proposal.toml"}}' | 'Translate archive/proposal.toml into German and save it. Cheers.'
