# mt-dpo-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.987 [0.967, 1.000] |
| L1 json | 0.987 [0.967, 1.000] |
| L2 schema | 0.987 [0.967, 1.000] |
| L3 tool | 0.987 [0.967, 1.000] |
| L4 args | 0.987 [0.967, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.993 [0.981, 1.000] |
| step right | 0.978 [0.959, 0.993] |
| answer grounded | 0.958 [0.917, 0.990] |
| episode right | 0.950 [0.908, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.88 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.94 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\n```toml\ninvoice:\n  date: 2026-04-15\n  amount: 37.98\n```\n\nThe file contains:\n\ninvoice:\n  date: 2026-04-15\n  a'
- `mt_test_id-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nlunch at noon on Friday'
- `mt_test_id-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'archive/results.md is 38 bytes. Here it is:\n\nThe contents of archive/results.md:\n\nThis is what I read from archive/results.md: The contents '
- `mt_test_id-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nlunch at noon on Friday'
- `mt_test_id-01105` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/results.txt.' -> 'I can do that once I know more. Which folder should I save it in?'
- `mt_test_id-01123` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/checklist.md.' -> 'I can do that once I know more. Which folder should I save it in?'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.956 [0.929, 0.980] |
| L1 json | 0.956 [0.929, 0.980] |
| L2 schema | 0.956 [0.929, 0.980] |
| L3 tool | 0.885 [0.845, 0.925] |
| L4 args | 0.869 [0.825, 0.909] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.976 [0.960, 0.989] |
| step right | 0.903 [0.874, 0.929] |
| answer grounded | 0.931 [0.887, 0.969] |
| episode right | 0.820 [0.765, 0.870] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.74 |
| find_then_read | 60 | 0.98 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.93 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.78 |
| search_then_save | 60 | 0.93 |
| stats_then_search | 54 | 0.85 |

Failures (first 12):

- `mt_test_ood-00287` find_then_read: reply lacks the tool's fact | 'Somewhere in scripts there is a file named agenda. What does it say?' -> "The contents of scripts/agenda.md:\n\nagenda.md: This is the agenda for today's meeting. It includes items such as:\n\n- Review of last week's p"
- `mt_test_ood-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> "The contents of data/raw/readme.toml:\n\n```toml\nThis is readme.toml.\nIt's 38 bytes long.\n```\n\nHappy to help."
- `mt_test_ood-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of data/raw/invoice.txt:\n\nInvoice 123456789:\nDate: 2026-02-24\nAmount: $1,000.00\nDescription: Purchase of office supplies.\n\nThis'
- `mt_test_ood-00539` check_then_read: fails tool  | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt_test_ood-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> "The contents of scripts/invoice.md:\n\npick up the parcel\n\nIt's 39 bytes."
- `mt_test_ood-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'archive/readme.txt says:\n\nbudget approved'
- `mt_test_ood-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'The contents of research/readme.txt:\n\nbudget approved'
- `mt_test_ood-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> "Here is research/results.toml:\n\ntests: 18\npassing: true\n\nIt's 18 lines long."
- `mt_test_ood-00557` check_then_read: fails tool  | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
