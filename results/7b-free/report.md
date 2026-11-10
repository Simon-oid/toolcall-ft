# 7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.992 [0.975, 1.000] |
| L1 json | 0.992 [0.975, 1.000] |
| L2 schema | 0.992 [0.975, 1.000] |
| L3 tool | 0.967 [0.933, 0.992] |
| L4 args | 0.950 [0.908, 0.983] |
| abstain | 0.650 [0.533, 0.767] |
| decision | 0.878 [0.828, 0.922] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.70 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.90 |
| fs_read | 20 | 0.80 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 0.80 |
| unsupported | 20 | 0.45 |

Failures (first 12):

- `test_id-00682` fs_list: fails json no call | "Okay, next: What's inside archive?" -> "I need the path to the archive you're interested in. Could you please provide it?"
- `test_id-00683` fs_list: fails tool  | 'Show me the contents of archive. Please check.' -> '{"name": "fs_read", "arguments": {"path": "archive", "offset": 1, "limit": 100}}'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_stat", "arguments": {"path": "drafts/proposal.toml"}}'
- `test_id-01092` fs_read: fails tool  | "What's in archive/agenda.toml?" -> '{"name": "fs_stat", "arguments": {"path": "archive/agenda.toml"}}'
- `test_id-01093` fs_read: fails args  | 'Print lines 3 to 7 from research/outline.py. Please check.' -> '{"name": "fs_read", "arguments": {"limit": 5, "offset": 2, "path": "research/outline.py"}}'
- `test_id-01097` fs_read: fails args  | 'Read drafts/outline.toml.' -> '{"name": "fs_read", "arguments": {"path": "drafts/outline.toml", "offset": 1, "limit": 1000}}'
- `test_id-01750` no_tool: called '{"name": "crag_search", "arguments": {"k": 5, "query": "distance Moon Earth"}}' | 'How far is the Moon from the Earth, roughly?'
- `test_id-01752` no_tool: called '{"name": "crag_search", "arguments": {"query": "CPU stand for", "k": 5}}' | 'What does CPU stand for? Cheers.'
- `test_id-01756` no_tool: called '{"name": "crag_search", "arguments": {"k": 5, "query": "Is Python compiled or interpreted?"}}' | 'Okay, next: Is Python compiled or interpreted?'
- `test_id-01767` no_tool: called '{"name": "crag_search", "arguments": {"query": "tip for remembering names", "k": 5}}' | 'Okay, next: Give me a tip for remembering names.'
- `test_id-01916` unsupported: called '{"name": "fs_stat", "arguments": {"path": "drafts/notes-2026.py"}}' | 'Hey there. Remove drafts/notes-2026.py permanently.'
- `test_id-01917` unsupported: called '{"name": "fs_read", "arguments": {"path": "research/notes-2026.md"}}' | 'Translate research/notes-2026.md into German and save it.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.958 [0.926, 0.984] |
| L1 json | 0.958 [0.926, 0.984] |
| L2 schema | 0.958 [0.926, 0.984] |
| L3 tool | 0.947 [0.915, 0.974] |
| L4 args | 0.905 [0.862, 0.942] |
| abstain | 0.600 [0.505, 0.695] |
| decision | 0.830 [0.786, 0.871] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.69 |
| crag_search | 35 | 1.00 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.74 |
| fs_read | 35 | 0.80 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.94 |
| no_tool | 35 | 0.66 |
| unsupported | 35 | 0.46 |

Failures (first 12):

- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research content", "k": 5}}'
- `test_ood-00698` fs_list: fails json no call | 'What does drafts contain?' -> 'To check what `drafts` contains, I need to know the exact path to it. Could you please provide the relative path to `drafts`? If `drafts` is'
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "research"}}'
- `test_ood-00704` fs_list: fails json no call | 'What does scripts contain?' -> 'To check what the `scripts` directory contains, I need to know its path relative to the sandbox root. Could you please provide the path to t'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'To provide you with information on what research contains, I can perform a search in the document index to find relevant chunks. Could you p'
- `test_ood-00712` fs_list: fails json no call | 'What does scripts contain? Cheers.' -> 'To check what the `scripts` directory contains, I need to know its path relative to the sandbox root. Could you please provide the path to t'
- `test_ood-00714` fs_list: fails json no call | 'One more thing: What does archive contain?' -> "To answer your question, I need to know the path to the archive you're referring to. Could you please provide the path, or if it's a specifi"
- `test_ood-00718` fs_list: fails json no call | 'One more thing: What does scripts contain?' -> 'To check what `scripts` contains, I first need to know the relative path to the `scripts` directory within the sandboxed file tree. Could yo'
- `test_ood-00722` fs_list: fails json no call | 'What does drafts contain? Cheers.' -> 'To check what `drafts` contains, I need to know the exact path to it. Could you please provide the relative path to the `drafts` directory, '
- `test_ood-01105` fs_read: fails args  | 'Let me see what drafts/notes-2026.py says.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.py", "offset": 1, "limit": 1000}}'
- `test_ood-01107` fs_read: fails args  | 'Everything in archive/results.toml after line 99, please.' -> '{"name": "fs_read", "arguments": {"offset": 99, "path": "archive/results.toml"}}'
- `test_ood-01113` fs_read: fails args  | 'Everything in data/raw/outline.txt after line 11, please.' -> '{"name": "fs_read", "arguments": {"offset": 11, "path": "data/raw/outline.txt"}}'
