# mtg-ft-1.5b-v6-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

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
| call made | 0.956 [0.929, 0.980] |
| L1 json | 0.956 [0.929, 0.980] |
| L2 schema | 0.956 [0.929, 0.980] |
| L3 tool | 0.901 [0.861, 0.937] |
| L4 args | 0.853 [0.810, 0.893] |
| abstain | 0.995 [0.985, 1.000] |
| decision | 0.973 [0.958, 0.987] |
| step right | 0.916 [0.889, 0.940] |
| answer grounded | 0.994 [0.981, 1.000] |
| episode right | 0.830 [0.775, 0.880] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 0.98 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.95 |
| followup_save | 40 | 0.85 |
| followup_stat | 40 | 0.93 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 0.93 |
| stats_then_search | 54 | 0.85 |

Failures (first 12):

- `mt_test_ood_g-00250` find_then_read: fails args  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "research/checklist"}}'
- `mt_test_ood_g-00832` search_then_save: fails args  | 'Query the index on cancellation of requests; the top chunk should end up in data/raw/outline.py.' -> '{"name": "crag_search", "arguments": {"query": "the top chunk should end up in data/raw/outline.py"}}'
- `mt_test_ood_g-00850` search_then_save: fails args  | 'Query the index on cancellation of requests; the top chunk should end up in scripts/readme.md.' -> '{"name": "crag_search", "arguments": {"query": "the top chunk should end up in scripts/readme.md"}}'
- `mt_test_ood_g-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'I can do that once I know more. What should I write in archive/readme.toml?'
- `mt_test_ood_g-00874` search_then_save: fails args  | 'Query the index on cancellation of requests; the top chunk should end up in scripts/readme.txt. Please check.' -> '{"name": "crag_search", "arguments": {"query": "the top chunk should end up in scripts/readme.txt"}}'
- `mt_test_ood_g-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "an inventory of research"}}'
- `mt_test_ood_g-01144` list_then_write: fails tool  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/drafts", "content": "An inventory of drafts."}}'
- `mt_test_ood_g-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "notes-2026.toml\\nreadme.py\\n"}}'
- `mt_test_ood_g-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive"}}'
- `mt_test_ood_g-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "an inventory of drafts"}}'
- `mt_test_ood_g-01162` list_then_write: fails tool  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "data/raw", "content": "an inventory of data/raw"}}'
- `mt_test_ood_g-01163` list_then_write: fails args  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "data/raw", "content": "checklist.txt\\nresults.toml\\n"}}'
