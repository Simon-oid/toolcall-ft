# mt-ft-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

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


## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.996 [0.988, 1.000] |
| L1 json | 0.996 [0.988, 1.000] |
| L2 schema | 0.992 [0.980, 1.000] |
| L3 tool | 0.917 [0.881, 0.948] |
| L4 args | 0.901 [0.861, 0.937] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.998 [0.993, 1.000] |
| step right | 0.945 [0.923, 0.965] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.890 [0.845, 0.930] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.90 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.90 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.78 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.98 |

Failures (first 12):

- `mt_test_ood-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00557` check_then_read: fails tool  | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt_test_ood-00563` check_then_read: fails tool  | 'Hey there. Is there a scripts/invoice.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt_test_ood-00574` check_then_read: fails tool  | 'Is there a data/raw/results.py? Read it out if so. Much appreciated.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research"}}'
- `mt_test_ood-01144` list_then_write: fails tool  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/readme.txt", "content": "This is the inventory of drafts."}}'
- `mt_test_ood-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "notes-2026.toml\\nreadme.py\\n"}}'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive"}}'
- `mt_test_ood-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "drafts"}}'
- `mt_test_ood-01162` list_then_write: fails tool  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "data/raw", "content": "This is the inventory of data/raw."}}'
