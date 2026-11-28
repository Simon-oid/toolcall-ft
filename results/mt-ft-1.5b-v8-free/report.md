# mt-ft-1.5b-v8-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.993 [0.980, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.996 [0.989, 1.000] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.992 [0.975, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 1.00 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.96 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 1.00 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id-01628` followup_read: fails args  | "What's in the third file?" -> '{"name": "fs_read", "arguments": {"path": "research/invoice.md"}}'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.980 [0.960, 0.996] |
| L1 json | 0.980 [0.960, 0.996] |
| L2 schema | 0.972 [0.948, 0.992] |
| L3 tool | 0.885 [0.845, 0.921] |
| L4 args | 0.861 [0.817, 0.905] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.989 [0.978, 0.998] |
| step right | 0.920 [0.894, 0.945] |
| answer grounded | 0.994 [0.981, 1.000] |
| episode right | 0.845 [0.795, 0.895] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.95 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.75 |
| search_then_save | 60 | 0.95 |
| stats_then_search | 54 | 0.74 |

Failures (first 12):

- `mt_test_ood-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00563` check_then_read: fails tool  | 'Hey there. Is there a scripts/invoice.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt_test_ood-00847` search_then_save: fails schema {'path': '/query', 'keyword': 'required', 'message': 'missing required property'} | 'Grab whatever the corpus ranks first for structured tool output and file it under research/invoice.toml. Please check.' -> '{"name": "crag_search", "arguments": {}}'
- `mt_test_ood-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'What should I write in archive/readme.toml?'
- `mt_test_ood-00871` search_then_save: fails schema {'path': '/query', 'keyword': 'required', 'message': 'missing required property'} | 'Okay, next: Grab whatever the corpus ranks first for structured tool output and file it under drafts/checklist.md.' -> '{"name": "crag_search", "arguments": {}}'
- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "an inventory of research"}}'
- `mt_test_ood-01144` list_then_write: fails tool  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/readme.md", "content": "This is the inventory of drafts."}}'
- `mt_test_ood-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/readme.py", "content": "notes-2026.toml\\nreadme.md\\nindex.html\\n"}}'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive: inventory of the archives"}}'
- `mt_test_ood-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "an inventory of drafts"}}'
- `mt_test_ood-01157` list_then_write: fails args  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/research/proposal.txt", "content": "checklist.toml\\nproposal.toml\\nreadme.toml\\nresults.t'
