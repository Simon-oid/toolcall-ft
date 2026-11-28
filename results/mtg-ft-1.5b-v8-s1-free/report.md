# mtg-ft-1.5b-v8-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 1.000 [1.000, 1.000] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 1.000 [1.000, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 1.00 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 1.00 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):


## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.968 [0.944, 0.988] |
| L1 json | 0.968 [0.944, 0.988] |
| L2 schema | 0.968 [0.944, 0.988] |
| L3 tool | 0.873 [0.829, 0.913] |
| L4 args | 0.861 [0.817, 0.901] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.982 [0.969, 0.993] |
| step right | 0.918 [0.892, 0.942] |
| answer grounded | 0.988 [0.969, 1.000] |
| episode right | 0.840 [0.790, 0.890] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.95 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.93 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.78 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.67 |

Failures (first 12):

- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research inventory\\n"}}'
- `mt_test_ood_g-01144` list_then_write: fails tool  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/readme.py", "content": "This is an inventory of drafts."}}'
- `mt_test_ood_g-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "notes-2026.toml\\nreadme.py\\n"}}'
- `mt_test_ood_g-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive\\n"}}'
- `mt_test_ood_g-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "drafts_inventory\\n- initial_draft1\\n- revised_draft2\\n- fina'
- `mt_test_ood_g-01157` list_then_write: fails args  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "checklist.toml\\nproposal.toml\\nreadme.toml\\nresults.toml\\n"}}'
- `mt_test_ood_g-01162` list_then_write: fails tool  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "drafts/checklist.toml", "content": "data/raw\\n"}}'
- `mt_test_ood_g-01168` list_then_write: fails tool  | 'I want data/raw/readme.py to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.py", "content": "research:\\n  papers\\n  reports\\n  presentations\\n  datasets\\n  '
- `mt_test_ood_g-01174` list_then_write: fails tool  | 'I want data/raw/proposal.md to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/proposal.md", "content": "archive\\nbooks\\ncd\\ndvd\\nelectronics\\nfilm\\ngames\\nhardware\\n'
