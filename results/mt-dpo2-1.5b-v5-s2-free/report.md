# mt-dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.967 [0.933, 0.992] |
| decision | 0.985 [0.970, 0.996] |
| step right | 0.974 [0.952, 0.993] |
| answer grounded | 0.969 [0.927, 1.000] |
| episode right | 0.942 [0.900, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.91 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 0.67 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 1.00 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\n```toml\ninvoice:\n  amount: 100.50\n  date: 2026-04-15\n```\n\nThe file contains:\n\ninvoice:\n  amount: 100.50\n  da'
- `mt_test_id-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nlunch at noon on Friday'
- `mt_test_id-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> "archive/results.md says:\n\nThis is archive/results.md. It's 38 bytes long, and was last changed on 2026-04-05. It has mode 0644.\n\narchive/res"
- `mt_test_id-02152` followup_ask: called '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "agenda.toml\\n"}}' | 'Save that.'
- `mt_test_id-02154` followup_ask: called '{"name": "fs_write", "arguments": {"path": "docs/hnsw-index-impl.md", "content": "HNSW is not implemented; the exact sca' | 'Put that in a file for me.'
- `mt_test_id-02155` followup_ask: called '{"name": "fs_write", "arguments": {"path": "docs/soak-test-result.txt", "content": "The soak test runs the server for si' | 'Store the result.'
- `mt_test_id-02161` followup_ask: called '{"name": "fs_write", "arguments": {"path": "scripts/results.txt", "content": "checklist.txt\\ninvoice.md\\noutline.py\\nres' | 'Store the result.'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.996 [0.988, 1.000] |
| L1 json | 0.996 [0.988, 1.000] |
| L2 schema | 0.996 [0.988, 1.000] |
| L3 tool | 0.933 [0.901, 0.960] |
| L4 args | 0.921 [0.885, 0.952] |
| abstain | 0.945 [0.910, 0.975] |
| decision | 0.973 [0.958, 0.987] |
| step right | 0.920 [0.894, 0.945] |
| answer grounded | 0.969 [0.938, 0.994] |
| episode right | 0.845 [0.790, 0.895] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.81 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 0.45 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.78 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.98 |

Failures (first 12):

- `mt_test_ood-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of data/raw/invoice.txt:\n\nInvoice 123456789\nDate: 2026-02-24\nAmount: $1,000.00\nDescription: Purchase of office supplies.'
- `mt_test_ood-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\npick up the parcel'
- `mt_test_ood-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nbudget approved'
- `mt_test_ood-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\ntests/2026-02-12_19:03:57.txt: 18 bytes\n\nThis file contains one line, which says "tests/2026-02-12_19:03:57.'
- `mt_test_ood-00557` check_then_read: fails tool  | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt_test_ood-00563` check_then_read: fails tool  | 'Hey there. Is there a scripts/invoice.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt_test_ood-00573` check_then_read: reply lacks the tool's fact | 'Only if scripts/agenda.py is present, display its contents.' -> 'Here is scripts/agenda.py:\n\n#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\nimport os\nimport sys\n\ndef main():\n    print("This is scripts/age'
- `mt_test_ood-00574` check_then_read: fails tool  | 'Is there a data/raw/results.py? Read it out if so. Much appreciated.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research"}}'
