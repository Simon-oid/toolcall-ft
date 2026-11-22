# mt-ft-1.5b-v4-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v4-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-18-gb048dad · date: 2026-11-21 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.593 [0.513, 0.667] |
| L1 json | 0.593 [0.513, 0.667] |
| L2 schema | 0.593 [0.513, 0.667] |
| L3 tool | 0.440 [0.360, 0.520] |
| L4 args | 0.327 [0.253, 0.407] |
| abstain | 0.983 [0.958, 1.000] |
| decision | 0.767 [0.715, 0.815] |
| step right | 0.530 [0.470, 0.589] |
| answer grounded | 0.740 [0.646, 0.823] |
| episode right | 0.358 [0.275, 0.450] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.25 |
| find_then_read | 36 | 0.19 |
| followup_ask | 12 | 0.92 |
| followup_read | 24 | 0.54 |
| followup_save | 24 | 0.83 |
| followup_stat | 24 | 0.83 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.36 |
| search_then_save | 36 | 0.58 |
| stats_then_search | 34 | 0.53 |

Failures (first 12):

- `mt_test_id-00210` find_then_read: fails tool  | 'One more thing: Open the outline file in data/raw.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline"}}'
- `mt_test_id-00211` find_then_read: fails json no call | 'One more thing: Open the outline file in data/raw.' -> 'I found the file in data/raw. Here are its contents:\n\n1. invoice.md\n2. notes-2026.txt\n3. outline.txt\n4. results.md'
- `mt_test_id-00214` find_then_read: fails json no call | 'Okay, next: Show me the agenda document that lives in research.' -> 'The agenda document is in the research folder. Here are some of its contents:\n\n- agenda.toml (20 bytes)\n- invoice.md (40 bytes)\n- outline.tx'
- `mt_test_id-00215` find_then_read: reply lacks the tool's fact | 'Okay, next: Show me the agenda document that lives in research.' -> 'I can do that once I know more. What should I write in agenda.toml?'
- `mt_test_id-00216` find_then_read: fails tool  | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me." -> '{"name": "fs_read", "arguments": {"path": "notes-2026"}}'
- `mt_test_id-00218` find_then_read: reply lacks the tool's fact | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me." -> "I can't read files: my tools can only search and inspect the document index, and list, read, stat or write files in the sandbox."
- `mt_test_id-00219` find_then_read: fails tool  | "I don't remember the extension, but read the checklist file in scripts." -> '{"name": "fs_read", "arguments": {"path": "scripts/checklist"}}'
- `mt_test_id-00220` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> 'I found the file in scripts. Here are its details:\n\n- checklist.md: 18 bytes\n- invoice.txt: 44 bytes\n- proposal.py: 19 bytes\n- results.toml:'
- `mt_test_id-00221` find_then_read: reply lacks the tool's fact | "I don't remember the extension, but read the checklist file in scripts." -> 'I can read files from the scripts folder. Here are some of them:\n\n- checklist.md (18 lines)\n- invoice.txt (44 lines)\n- proposal.py (19 lines'
- `mt_test_id-00222` find_then_read: fails tool  | 'Find the file called notes-2026 in archive and show me what it says.' -> '{"name": "fs_read", "arguments": {"path": "archive/notes-2026"}}'
- `mt_test_id-00225` find_then_read: fails tool  | 'Read whatever invoice file is inside archive.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice"}}'
- `mt_test_id-00226` find_then_read: fails json no call | 'Read whatever invoice file is inside archive.' -> 'I found the following files in archive:\n\n- Invoice: 18 lines, contents of invoice.md\n- Proposal: 24 lines, contents of proposal.py\n- Results'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.643 [0.583, 0.702] |
| L1 json | 0.643 [0.583, 0.702] |
| L2 schema | 0.635 [0.575, 0.694] |
| L3 tool | 0.405 [0.345, 0.464] |
| L4 args | 0.310 [0.254, 0.369] |
| abstain | 0.975 [0.950, 0.995] |
| decision | 0.790 [0.750, 0.827] |
| step right | 0.527 [0.480, 0.573] |
| answer grounded | 0.762 [0.694, 0.825] |
| episode right | 0.325 [0.260, 0.390] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.29 |
| find_then_read | 60 | 0.28 |
| followup_ask | 20 | 0.90 |
| followup_read | 40 | 0.65 |
| followup_save | 40 | 0.55 |
| followup_stat | 40 | 0.57 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.65 |
| search_then_save | 60 | 0.47 |
| stats_then_search | 54 | 0.52 |

Failures (first 12):

- `mt_test_ood-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "fs_read", "arguments": {"path": "research/results"}}'
- `mt_test_ood-00247` find_then_read: fails args  | 'Can you track down the results file under research and print it?' -> '{"name": "fs_read", "arguments": {"path": "results.py"}}'
- `mt_test_ood-00248` find_then_read: reply lacks the tool's fact | 'Can you track down the results file under research and print it?' -> 'The file `results.py` in the research directory contains:\n\n1. A note about lunch at noon on Friday.\n2. A message that the budget has been ap'
- `mt_test_ood-00249` find_then_read: fails tool  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "research/checklist"}}'
- `mt_test_ood-00250` find_then_read: fails json no call | 'Somewhere in research there is a file named checklist. What does it say?' -> 'The file named `checklist` in the research folder contains the following text:\n\n- File size: 19 bytes\n- Content: [checklist.toml]\n\n- File si'
- `mt_test_ood-00251` find_then_read: reply lacks the tool's fact | 'Somewhere in research there is a file named checklist. What does it say?' -> "I can't read files: my tools can only search and inspect the document index, and list, read, stat or write files in the sandbox."
- `mt_test_ood-00252` find_then_read: fails tool  | 'Can you track down the proposal file under data/raw and print it?' -> '{"name": "fs_read", "arguments": {"path": "data/raw/proposal"}}'
- `mt_test_ood-00255` find_then_read: fails tool  | 'Hey there. Somewhere in data/raw there is a file named invoice. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "data/raw/invoice"}}'
- `mt_test_ood-00256` find_then_read: fails json no call | 'Hey there. Somewhere in data/raw there is a file named invoice. What does it say?' -> 'The file in data/raw is named invoice. Here are the contents:\n\n- checklist.toml (24 bytes)\n- invoice.txt (20 bytes)\n- readme.txt (44 bytes)\n'
- `mt_test_ood-00258` find_then_read: fails tool  | 'Can you track down the outline file under research and print it?' -> '{"name": "fs_read", "arguments": {"path": "research/outline"}}'
- `mt_test_ood-00260` find_then_read: called '{"name": "crag_stats"}' | 'Can you track down the outline file under research and print it?'
- `mt_test_ood-00261` find_then_read: fails tool  | 'Somewhere in data/raw there is a file named agenda. What does it say? Cheers.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda"}}'
