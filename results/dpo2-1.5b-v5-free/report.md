# dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 474

## test_id (120 need a call, 60 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.975 [0.942, 1.000] |
| abstain | 0.083 [0.017, 0.167] |
| decision | 0.694 [0.628, 0.761] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 20 | 0.05 |
| crag_search | 20 | 0.95 |
| crag_stats | 20 | 1.00 |
| fs_list | 20 | 0.95 |
| fs_read | 20 | 1.00 |
| fs_stat | 20 | 1.00 |
| fs_write | 20 | 0.95 |
| no_tool | 20 | 0.10 |
| unsupported | 20 | 0.10 |

Failures (first 12):

- `test_id-00308` crag_search: fails args  | 'Find me the passages about the SSRF egress guard. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "the SSRF egress guard", "k": 1}}'
- `test_id-00675` fs_list: fails args  | 'List the files in the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_id-01557` fs_write: fails args  | 'Write "budget approved" to drafts/proposal.py. Much appreciated.' -> '{"name": "fs_write", "arguments": {"path": "drafts/proposal.py", "content": "budget approved Much appreciated."}}'
- `test_id-01749` no_tool: called '{"name": "fs_write", "arguments": {"path": "coffee.txt", "content": "Much appreciated, coffee! A brew so strong,\\nIn the' | 'Write a limerick about coffee. Much appreciated.'
- `test_id-01750` no_tool: called '{"name": "crag_search", "arguments": {"query": "the Moon\'s distance from the Earth, roughly"}}' | 'How far is the Moon from the Earth, roughly?'
- `test_id-01751` no_tool: called '{"name": "crag_search", "arguments": {"query": "minutes in a day"}}' | 'Hey there. How many minutes are in a day?'
- `test_id-01752` no_tool: called '{"name": "crag_search", "arguments": {"query": "CPU"}}' | 'What does CPU stand for? Cheers.'
- `test_id-01753` no_tool: called '{"name": "fs_write", "arguments": {"path": "log.txt", "content": "Good night, talk tomorrow."}}' | 'Good night, talk tomorrow.'
- `test_id-01754` no_tool: called '{"name": "fs_write", "arguments": {"path": "goodnight.txt", "content": "Good night, talk tomorrow."}}' | 'One more thing: Good night, talk tomorrow.'
- `test_id-01755` no_tool: called '{"name": "crag_search", "arguments": {"query": "a day"}}' | 'How many minutes are in a day?'
- `test_id-01756` no_tool: called '{"name": "crag_search", "arguments": {"query": "Python compiled or interpreted"}}' | 'Okay, next: Is Python compiled or interpreted?'
- `test_id-01757` no_tool: called '{"name": "crag_search", "arguments": {"query": "gardening", "k": 1}}' | 'Suggest a title for a blog post about gardening.'

## test_ood (189 need a call, 105 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.979 [0.958, 0.995] |
| L2 schema | 0.974 [0.947, 0.995] |
| L3 tool | 0.963 [0.937, 0.989] |
| L4 args | 0.921 [0.878, 0.958] |
| abstain | 0.057 [0.019, 0.105] |
| decision | 0.663 [0.609, 0.718] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 35 | 0.03 |
| crag_search | 35 | 0.94 |
| crag_stats | 14 | 0.86 |
| fs_list | 35 | 0.94 |
| fs_read | 35 | 0.74 |
| fs_stat | 35 | 1.00 |
| fs_write | 35 | 1.00 |
| no_tool | 35 | 0.06 |
| unsupported | 35 | 0.09 |

Failures (first 12):

- `test_ood-00325` crag_search: fails args  | 'Run a retrieval on nDCG evaluation, please. Please check.' -> '{"name": "crag_search", "arguments": {"query": "nDCG evaluation", "k": 10}}'
- `test_ood-00339` crag_search: fails args  | 'Run a retrieval on log redaction, please. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "log redaction", "k": 10}}'
- `test_ood-00465` crag_stats: fails tool  | 'Okay, next: Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "crag"}}'
- `test_ood-00475` crag_stats: fails tool  | 'Hey there. Report the size of the document index.' -> '{"name": "fs_stat", "arguments": {"path": "crag"}}'
- `test_ood-00716` fs_list: fails args  | 'Hey there. What does the sandbox root contain?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_ood-00719` fs_list: fails args  | 'Hey there. Give me a directory listing for the sandbox root.' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_ood-01107` fs_read: fails json  | 'Everything in archive/results.toml after line 99, please.' -> '{"name": "fs_read", "arguments": {"path": "archive/results.toml", "offset": 100}'
- `test_ood-01109` fs_read: fails args  | 'Peek at data/raw/agenda.py: 5 lines from the start.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda.py", "offset": 1, "limit": 6}}'
- `test_ood-01113` fs_read: fails json  | 'Everything in data/raw/outline.txt after line 11, please.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline.txt", "offset": 12}'
- `test_ood-01123` fs_read: fails args  | 'One more thing: Peek at research/results.md: 5 lines from the start.' -> '{"name": "fs_read", "arguments": {"path": "research/results.md", "offset": 1, "limit": 6}}'
- `test_ood-01125` fs_read: fails args  | 'Peek at archive/invoice.md: 5 lines from the start. Cheers.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice.md", "offset": 1, "limit": 6}}'
- `test_ood-01126` fs_read: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'Resume research/invoice.toml from line 5.' -> '{"name": "fs_read", "arguments": {"path": "invoice.toml", "offset": 5, "limit": null}}'
