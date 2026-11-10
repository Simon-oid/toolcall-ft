# 7b-lazy

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: llama.cpp tool grammar, applied once a call starts (lazy) · llama.cpp: b1-a4d4f2f · commit: fb164bc · date: 2026-11-10 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.975 [0.942, 1.000] |
| L4 args | 0.900 [0.842, 0.950] |
| abstain | 0.667 [0.550, 0.783] |
| decision | 0.889 [0.844, 0.933] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.80 |
| crag_search | 20 | 1.00 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 0.45 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 1.00 |
| no_tool | 20 | 0.80 |
| unsupported | 20 | 0.40 |

Failures (first 12):

- `test_id-00683` fs_list: fails tool  | 'Show me the contents of archive. Please check.' -> '{"name": "fs_read", "arguments": {"path": "archive", "offset": 1}}'
- `test_id-01084` fs_read: fails args  | 'Read lines 40 to 44 of archive/checklist.md.' -> '{"name": "fs_read", "arguments": {"path": "archive/checklist.md", "offset": 40}}'
- `test_id-01085` fs_read: fails args  | 'Show drafts/outline.toml, lines 10 through 19. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "drafts/outline.toml", "offset": 10}}'
- `test_id-01086` fs_read: fails tool  | "What's in drafts/proposal.toml?" -> '{"name": "fs_stat", "arguments": {"path": "drafts/proposal.toml"}}'
- `test_id-01088` fs_read: fails args  | 'I need lines 40 to 49 in archive/invoice.md.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice.md", "offset": 40}}'
- `test_id-01089` fs_read: fails args  | 'Give me the top 5 lines of scripts/outline.py. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "scripts/outline.py", "offset": 1}}'
- `test_id-01090` fs_read: fails args  | 'Read lines 40 to 44 of research/results.py.' -> '{"name": "fs_read", "arguments": {"path": "research/results.py", "offset": 40}}'
- `test_id-01092` fs_read: fails tool  | "What's in archive/agenda.toml?" -> '{"name": "fs_stat", "arguments": {"path": "archive/agenda.toml"}}'
- `test_id-01093` fs_read: fails args  | 'Print lines 3 to 7 from research/outline.py. Please check.' -> '{"name": "fs_read", "arguments": {"path": "research/outline.py", "offset": 3000000003000000}}'
- `test_id-01095` fs_read: fails args  | 'Give me scripts/agenda.toml from line 25 to line 45.' -> '{"name": "fs_read", "arguments": {"path": "scripts/agenda.toml", "offset": 25}}'
- `test_id-01097` fs_read: fails args  | 'Read drafts/outline.toml.' -> '{"name": "fs_read", "arguments": {"path": "drafts/outline.toml", "offset": 1}}'
- `test_id-01103` fs_read: fails args  | 'Show research/readme.toml, lines 3 through 7.' -> '{"name": "fs_read", "arguments": {"path": "research/readme.toml", "offset": 3}}'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.952 [0.921, 0.979] |
| L1 json | 0.952 [0.921, 0.979] |
| L2 schema | 0.952 [0.921, 0.979] |
| L3 tool | 0.942 [0.905, 0.974] |
| L4 args | 0.836 [0.783, 0.889] |
| abstain | 0.610 [0.514, 0.705] |
| decision | 0.830 [0.786, 0.871] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.66 |
| crag_search | 35 | 1.00 |
| crag_stats | 14 | 1.00 |
| fs_list | 35 | 0.71 |
| fs_read | 35 | 0.46 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 0.94 |
| no_tool | 35 | 0.71 |
| unsupported | 35 | 0.46 |

Failures (first 12):

- `test_ood-00694` fs_list: fails tool  | 'What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research content", "k": 5}}'
- `test_ood-00698` fs_list: fails json no call | 'What does drafts contain?' -> 'To check what `drafts` contains, I need to know the exact path to it. Could you please provide the relative path to the `drafts` directory? '
- `test_ood-00702` fs_list: fails tool  | 'Okay, next: What does research contain?' -> '{"name": "crag_search", "arguments": {"query": "research", "k": 5}}'
- `test_ood-00704` fs_list: fails json no call | 'What does scripts contain?' -> 'To check what the `scripts` directory contains, I need to know its path relative to the sandbox root. Could you please provide the path to t'
- `test_ood-00710` fs_list: fails json no call | 'What does research contain? Cheers.' -> 'To provide you with information on what research contains, I can perform a search in the document index to find relevant chunks. Could you p'
- `test_ood-00712` fs_list: fails json no call | 'What does scripts contain? Cheers.' -> "To answer your question, I need to know the path to the scripts you're referring to. Could you please provide the path to the directory cont"
- `test_ood-00714` fs_list: fails json no call | 'One more thing: What does archive contain?' -> "To answer your question, I need to know the path to the archive you're referring to. Could you please provide the path, or if it's a specifi"
- `test_ood-00718` fs_list: fails json no call | 'One more thing: What does scripts contain?' -> 'To check what `scripts` contains, I first need to know the relative path to the `scripts` directory within the sandboxed file tree. Could yo'
- `test_ood-00720` fs_list: fails json no call | 'Okay, next: What does scripts contain?' -> 'To find out what `scripts` contains, I need to know the exact path to the `scripts` directory within the sandboxed file tree. Could you plea'
- `test_ood-00722` fs_list: fails json no call | 'What does drafts contain? Cheers.' -> 'To check what `drafts` contains, I need to know the exact path to it. Could you please provide the relative path to the `drafts` directory? '
- `test_ood-01105` fs_read: fails args  | 'Let me see what drafts/notes-2026.py says.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.py", "offset": 1}}'
- `test_ood-01107` fs_read: fails args  | 'Everything in archive/results.toml after line 99, please.' -> '{"name": "fs_read", "arguments": {"path": "archive/results.toml", "offset": 99}}'
