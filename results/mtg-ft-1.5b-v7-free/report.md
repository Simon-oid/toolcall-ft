# mtg-ft-1.5b-v7-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-26 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.993 [0.980, 1.000] |
| L1 json | 0.993 [0.980, 1.000] |
| L2 schema | 0.993 [0.980, 1.000] |
| L3 tool | 0.993 [0.980, 1.000] |
| L4 args | 0.987 [0.967, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.996 [0.989, 1.000] |
| step right | 0.989 [0.974, 1.000] |
| answer grounded | 0.990 [0.969, 1.000] |
| episode right | 0.975 [0.942, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 1.00 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.94 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 0.97 |

Failures (first 12):

- `mt_test_id_g-01111` list_then_write: fails json no call | 'Record which files are in archive in the file scripts/notes-2026.toml.' -> 'Sure, but I need one detail first. What should I save in scripts/notes-2026.toml?'
- `mt_test_id_g-01121` list_then_write: fails args  | 'Save a listing of drafts as data/raw/readme.txt. Please check.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.txt", "content": "agenda.txt\\nchecklist.py\\nproposal.py\\results.py\\n"}}'
- `mt_test_id_g-01384` stats_then_search: reply lacks the tool's fact | "Hey there. If the index isn't empty, search it for subscriptions." -> 'From the index (docs/subscriptions.md): Connections beyond 64 per second are closed at accept.'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.984 [0.968, 0.996] |
| L1 json | 0.984 [0.968, 0.996] |
| L2 schema | 0.984 [0.968, 0.996] |
| L3 tool | 0.833 [0.786, 0.877] |
| L4 args | 0.806 [0.758, 0.853] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.991 [0.982, 0.998] |
| step right | 0.883 [0.852, 0.912] |
| answer grounded | 0.975 [0.950, 0.994] |
| episode right | 0.770 [0.710, 0.825] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.83 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.88 |
| followup_stat | 40 | 0.80 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.73 |
| search_then_save | 60 | 0.98 |
| stats_then_search | 54 | 0.76 |

Failures (first 12):

- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'Here is data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'Here is archive/readme.txt:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00557` check_then_read: fails tool  | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt_test_ood_g-00563` check_then_read: fails tool  | 'Hey there. Is there a scripts/invoice.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt_test_ood_g-00580` check_then_read: fails tool  | 'Hey there. Is there a drafts/notes-2026.txt? Read it out if so.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.txt"}}'
- `mt_test_ood_g-00881` search_then_save: fails args  | 'Hey there. Query the index on subscriptions; the top chunk should end up in archive/checklist.py.' -> '{"name": "fs_write", "arguments": {"path": "archive/checklist.py", "content": "docs/subscriptions.md"}}'
- `mt_test_ood_g-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research"}}'
