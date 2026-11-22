# mt-ft-1.5b-v4-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v4-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-21 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.600 [0.520, 0.680] |
| L1 json | 0.593 [0.513, 0.673] |
| L2 schema | 0.580 [0.500, 0.660] |
| L3 tool | 0.453 [0.373, 0.533] |
| L4 args | 0.353 [0.280, 0.433] |
| abstain | 0.992 [0.975, 1.000] |
| decision | 0.774 [0.722, 0.822] |
| step right | 0.574 [0.515, 0.633] |
| answer grounded | 0.812 [0.729, 0.885] |
| episode right | 0.408 [0.317, 0.500] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.38 |
| find_then_read | 36 | 0.25 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.54 |
| followup_save | 24 | 0.67 |
| followup_stat | 24 | 0.92 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.39 |
| search_then_save | 36 | 0.78 |
| stats_then_search | 34 | 0.50 |

Failures (first 12):

- `mt_test_id-00210` find_then_read: fails tool  | 'One more thing: Open the outline file in data/raw.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline"}}'
- `mt_test_id-00211` find_then_read: fails json no call | 'One more thing: Open the outline file in data/raw.' -> 'I found the files in the outline. They are:\n\n- Invoice: 16 lines\n- Notes (2026): 39 lines\n- Outline: 24 lines\n- Results: 44 lines'
- `mt_test_id-00214` find_then_read: fails json no call | 'Okay, next: Show me the agenda document that lives in research.' -> 'I found the following files in the research folder:\n\n- agenda.toml (20 bytes)\n- invoice.md (40 bytes)\n- outline.txt (19 bytes)\n- results.tom'
- `mt_test_id-00215` find_then_read: reply lacks the tool's fact | 'Okay, next: Show me the agenda document that lives in research.' -> 'I can do that once I know more. Which file should I read?'
- `mt_test_id-00216` find_then_read: fails tool  | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me." -> '{"name": "fs_read", "arguments": {"path": "notes-2026"}}'
- `mt_test_id-00217` find_then_read: fails json no call | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me." -> 'I found the file `notes-2026.toml` in archive. Here it is:\n\n```toml\n# Notes for 2026\n\n- Task 1: Plan project launch\n- Task 2: Research marke'
- `mt_test_id-00218` find_then_read: reply lacks the tool's fact | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me." -> 'I can do that once I know more. Which file should I read from archive?'
- `mt_test_id-00219` find_then_read: fails tool  | "I don't remember the extension, but read the checklist file in scripts." -> '{"name": "fs_read", "arguments": {"path": "scripts/checklist"}}'
- `mt_test_id-00220` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> 'I found the files in scripts. Here they are:\n\n- checklist.md, size: 18 bytes\n- invoice.txt, size: 44 bytes\n- proposal.py, size: 19 bytes\n- r'
- `mt_test_id-00222` find_then_read: fails tool  | 'Find the file called notes-2026 in archive and show me what it says.' -> '{"name": "fs_read", "arguments": {"path": "archive/notes-2026"}}'
- `mt_test_id-00223` find_then_read: fails json no call | 'Find the file called notes-2026 in archive and show me what it says.' -> 'I found the file called notes-2026 in archive. Here is what it says:\n\nnotes-2026.toml\n\n(file size: 40 bytes)'
- `mt_test_id-00225` find_then_read: fails tool  | 'Read whatever invoice file is inside archive.' -> '{"name": "fs_read", "arguments": {"path": "archive/invoice"}}'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.627 [0.567, 0.687] |
| L1 json | 0.627 [0.567, 0.687] |
| L2 schema | 0.623 [0.563, 0.683] |
| L3 tool | 0.413 [0.353, 0.476] |
| L4 args | 0.321 [0.266, 0.381] |
| abstain | 0.990 [0.975, 1.000] |
| decision | 0.788 [0.750, 0.825] |
| step right | 0.542 [0.496, 0.588] |
| answer grounded | 0.775 [0.706, 0.838] |
| episode right | 0.355 [0.290, 0.420] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.24 |
| find_then_read | 60 | 0.25 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.68 |
| followup_save | 40 | 0.45 |
| followup_stat | 40 | 0.70 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.65 |
| search_then_save | 60 | 0.63 |
| stats_then_search | 54 | 0.48 |

Failures (first 12):

- `mt_test_ood-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "fs_read", "arguments": {"path": "research/results"}}'
- `mt_test_ood-00247` find_then_read: fails json no call | 'Can you track down the results file under research and print it?' -> 'Here are the files in the research folder:\n\n1. agenda.md - Size: 44 bytes\n2. notes-2026.md - Size: 42 bytes\n3. outline.py - Size: 19 bytes\n4'
- `mt_test_ood-00249` find_then_read: fails tool  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "checklist"}}'
- `mt_test_ood-00250` find_then_read: fails json no call | 'Somewhere in research there is a file named checklist. What does it say?' -> 'The file named `checklist` in the research folder contains:\n\n- A toml file: checklist.toml (19 bytes)\n- An txt file: invoice.txt (16 bytes)\n'
- `mt_test_ood-00252` find_then_read: fails tool  | 'Can you track down the proposal file under data/raw and print it?' -> '{"name": "fs_read", "arguments": {"path": "data/raw/propose"}}'
- `mt_test_ood-00253` find_then_read: fails json no call | 'Can you track down the proposal file under data/raw and print it?' -> 'Here is the content of the proposal file:\n\n```markdown\nproposal.toml\n\nThis is a proposal document.\nIt contains details and ideas for a proje'
- `mt_test_ood-00255` find_then_read: fails tool  | 'Hey there. Somewhere in data/raw there is a file named invoice. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "data/raw/invoice"}}'
- `mt_test_ood-00256` find_then_read: fails json no call | 'Hey there. Somewhere in data/raw there is a file named invoice. What does it say?' -> 'The file `invoice.txt` in the `data/raw` directory contains the following text:\n\n```\nInvoice details:\n- Item: Product A\n- Quantity: 10\n- Pri'
- `mt_test_ood-00258` find_then_read: fails tool  | 'Can you track down the outline file under research and print it?' -> '{"name": "fs_read", "arguments": {"path": "research/outline"}}'
- `mt_test_ood-00259` find_then_read: fails json no call | 'Can you track down the outline file under research and print it?' -> 'I found the files in the research folder. Here they are:\n\n- **invoice.toml**: 24 bytes\n- **outline.md**: 18 bytes\n- **proposal.txt**: 37 byt'
- `mt_test_ood-00260` find_then_read: reply lacks the tool's fact | 'Can you track down the outline file under research and print it?' -> 'I found the outline file in the research folder. Here it is:\n\n```\nOutline of the project:\n- Introduction\n- Methodology\n- Results\n- Conclusio'
- `mt_test_ood-00261` find_then_read: fails tool  | 'Somewhere in data/raw there is a file named agenda. What does it say? Cheers.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda"}}'
