# mtg-ft-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.993 [0.980, 1.000] |
| L3 tool | 0.993 [0.980, 1.000] |
| L4 args | 0.987 [0.967, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.830 [0.785, 0.874] |
| answer grounded | 0.542 [0.448, 0.635] |
| episode right | 0.633 [0.550, 0.717] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.72 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 0.50 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.67 |
| search_then_save | 36 | 0.64 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'Here is drafts/notes-2026.md:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'The contents of archive/results.md:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00509` check_then_read: fails args  | 'If data/raw/readme.txt exists, show me what it says.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'Here is research/checklist.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'Here is data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00793` search_then_save: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}}'
- `mt_test_id_g-00795` search_then_save: reply lacks the tool's fact | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> "It's in archive/notes-2026.txt now."
- `mt_test_id_g-00798` search_then_save: reply lacks the tool's fact | 'Look up the soak test in the documentation and write the top result into data/raw/invoice.toml. Please check.' -> "It's in data/raw/invoice.toml now."

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.988 [0.972, 1.000] |
| L1 json | 0.988 [0.972, 1.000] |
| L2 schema | 0.988 [0.972, 1.000] |
| L3 tool | 0.948 [0.921, 0.972] |
| L4 args | 0.933 [0.901, 0.960] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.993 [0.985, 1.000] |
| step right | 0.790 [0.752, 0.827] |
| answer grounded | 0.512 [0.438, 0.588] |
| episode right | 0.590 [0.520, 0.660] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.69 |
| find_then_read | 60 | 0.98 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.50 |
| followup_stat | 40 | 0.97 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.47 |
| search_then_save | 60 | 0.65 |
| stats_then_search | 54 | 0.98 |

Failures (first 12):

- `mt_test_ood_g-00303` find_then_read: fails tool  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_stat", "arguments": {"path": "research/notes-2026"}}'
- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'Here is drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'Here is data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of data/raw/invoice.txt:\n\nrerun the benchmark'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'The contents of archive/results.py:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'This is what archive/readme.txt contains:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'Here is research/readme.txt:\n\npick up the parcel\nbudget approved'
- `mt_test_ood_g-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\nall tests passing'
- `mt_test_ood_g-00556` check_then_read: reply lacks the tool's fact | 'Only if research/invoice.toml is present, display its contents. Please check.' -> 'Here is research/invoice.toml:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00559` check_then_read: reply lacks the tool's fact | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> 'The contents of drafts/agenda.py:\n\nlunch at noon on Friday\nbudget approved'
