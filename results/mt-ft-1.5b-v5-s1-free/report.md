# mt-ft-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 722

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

- `mt_test_id-01628` followup_read: fails args  | "What's in the third file?" -> '{"name": "fs_read", "arguments": {"path": "research/results.py"}}'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.972 [0.952, 0.992] |
| L1 json | 0.968 [0.944, 0.988] |
| L2 schema | 0.968 [0.944, 0.988] |
| L3 tool | 0.905 [0.865, 0.940] |
| L4 args | 0.897 [0.857, 0.933] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.985 [0.973, 0.996] |
| step right | 0.942 [0.920, 0.962] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.870 [0.825, 0.915] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.83 |
| search_then_save | 60 | 0.97 |
| stats_then_search | 54 | 0.76 |

Failures (first 12):

- `mt_test_ood-00841` search_then_save: fails json no call | 'One more thing: Grab whatever the corpus ranks first for the HNSW index and file it under archive/agenda.txt.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'What text should readme.toml contain?'
- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research: books, papers, notes"}}'
- `mt_test_ood-01144` list_then_write: fails json no call | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> 'I can do that once I know more. What should the file contain?'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive: books, papers, presentations, notes"}}'
- `mt_test_ood-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "an inventory of drafts"}}'
- `mt_test_ood-01162` list_then_write: fails tool  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "drafts/checklist.toml", "content": "data/raw\\n"}}'
- `mt_test_ood-01168` list_then_write: fails json  | 'I want data/raw/readme.py to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.py", "content": "research:\\n- papers\\n- presentations\\n- datasets\\n- code\\n- not'
- `mt_test_ood-01174` list_then_write: fails tool  | 'I want data/raw/proposal.md to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/proposal.md", "content": "archive: books, papers, images, videos, documents"}}'
- `mt_test_ood-01181` list_then_write: fails args  | 'I want archive/readme.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/inventory.txt", "content": "checklist.py\\nproposal.md\\nreadme.toml\\nresults.toml\\n"}}'
- `mt_test_ood-01186` list_then_write: fails tool  | 'I want archive/proposal.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "archive/proposal.toml", "content": "data/raw\\n"}}'
- `mt_test_ood-01192` list_then_write: fails tool  | 'One more thing: I want data/raw/outline.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/outline.py", "content": "an inventory of drafts"}}'
