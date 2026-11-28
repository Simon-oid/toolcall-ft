# mt-ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.993 [0.980, 1.000] |
| L4 args | 0.987 [0.967, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.993 [0.981, 1.000] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.983 [0.958, 1.000] |

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
| search_then_save | 36 | 0.97 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id-00806` search_then_save: fails tool  | 'Check the knowledge base for rate limiting at accept and put the best hit in data/raw/results.toml.' -> '{"name": "crag_search", "arguments": {"query": "structured tool output"}}'
- `mt_test_id-01628` followup_read: fails args  | "What's in the third file?" -> '{"name": "fs_read", "arguments": {"path": "research/invoice.md"}}'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.968 [0.944, 0.988] |
| L1 json | 0.968 [0.944, 0.988] |
| L2 schema | 0.968 [0.944, 0.988] |
| L3 tool | 0.897 [0.857, 0.933] |
| L4 args | 0.869 [0.825, 0.909] |
| abstain | 0.995 [0.985, 1.000] |
| decision | 0.980 [0.967, 0.991] |
| step right | 0.920 [0.894, 0.945] |
| answer grounded | 0.988 [0.969, 1.000] |
| episode right | 0.840 [0.790, 0.890] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 0.95 |
| followup_read | 40 | 0.95 |
| followup_save | 40 | 0.85 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.80 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.72 |

Failures (first 12):

- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research inventory\\nbooks\\njournals\\npapers\\nreports\\ntheses\\n'
- `mt_test_ood-01144` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "notes-2026.toml\\nreadme.py\\n"}}'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda.toml"}}'
- `mt_test_ood-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_read", "arguments": {"path": "research/drafts.txt"}}'
- `mt_test_ood-01162` list_then_write: fails tool  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "drafts/checklist.toml", "content": "data/raw"}}'
- `mt_test_ood-01168` list_then_write: fails tool  | 'I want data/raw/readme.py to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.py", "content": "research:\\n- papers\\n- datasets\\n- models\\n- tools\\n- notebooks'
- `mt_test_ood-01169` list_then_write: fails args  | 'I want data/raw/readme.py to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.md", "content": "notes-2026.txt\\noutline.txt\\nreadme.md\\n"}}'
- `mt_test_ood-01174` list_then_write: fails tool  | 'I want data/raw/proposal.md to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/proposal.md", "content": "archive: book, CD, DVD, USB, hard drive"}}'
- `mt_test_ood-01180` list_then_write: fails args  | 'I want archive/readme.toml to hold an inventory of data/raw.' -> '{"name": "fs_list", "arguments": {"path": "data"}}'
- `mt_test_ood-01186` list_then_write: fails args  | 'I want archive/proposal.toml to hold an inventory of data/raw.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood-01192` list_then_write: fails tool  | 'One more thing: I want data/raw/outline.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/outline.py", "content": "drafts = {\'2023-01-01\': \'First draft\', \'2023-01-02\': \'Second d'
