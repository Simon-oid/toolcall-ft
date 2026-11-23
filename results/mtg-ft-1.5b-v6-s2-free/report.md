# mtg-ft-1.5b-v6-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

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
| call made | 0.972 [0.948, 0.992] |
| L1 json | 0.972 [0.948, 0.992] |
| L2 schema | 0.972 [0.948, 0.992] |
| L3 tool | 0.917 [0.881, 0.948] |
| L4 args | 0.897 [0.857, 0.933] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.985 [0.973, 0.996] |
| step right | 0.942 [0.920, 0.965] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.875 [0.830, 0.920] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.97 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.85 |
| search_then_save | 60 | 0.88 |
| stats_then_search | 54 | 0.87 |

Failures (first 12):

- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood_g-00835` search_then_save: fails json no call | 'Grab whatever the corpus ranks first for the soak test and file it under scripts/results.md.' -> 'I can do that once I know more. What should I write in scripts/results.md?'
- `mt_test_ood_g-00841` search_then_save: fails json no call | 'One more thing: Grab whatever the corpus ranks first for the HNSW index and file it under archive/agenda.txt.' -> 'I can do that once I know more. What should I write in archive/agenda.txt?'
- `mt_test_ood_g-00847` search_then_save: fails json no call | 'Grab whatever the corpus ranks first for structured tool output and file it under research/invoice.toml. Please check.' -> 'I can do that once I know more. What should I write in research/invoice.toml?'
- `mt_test_ood_g-00859` search_then_save: fails json no call | 'Hey there. Grab whatever the corpus ranks first for the soak test and file it under research/outline.txt.' -> 'I can do that once I know more. What should I write in research/outline.txt?'
- `mt_test_ood_g-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'What topic should I search the docs for?'
- `mt_test_ood_g-00865` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for the HNSW index and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I write in drafts/checklist.md?'
- `mt_test_ood_g-00871` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for structured tool output and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I write in drafts/checklist.md?'
- `mt_test_ood_g-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research"}}'
- `mt_test_ood_g-01145` list_then_write: fails args  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "drafts/inventory.txt", "content": "notes-2026.toml\\nreadme.py\\n"}}'
- `mt_test_ood_g-01150` list_then_write: fails args  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
