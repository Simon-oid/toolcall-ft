# mtg-ft-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.993 [0.980, 1.000] |
| L1 json | 0.993 [0.980, 1.000] |
| L2 schema | 0.993 [0.980, 1.000] |
| L3 tool | 0.993 [0.980, 1.000] |
| L4 args | 0.980 [0.953, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.996 [0.989, 1.000] |
| step right | 0.826 [0.781, 0.870] |
| answer grounded | 0.542 [0.448, 0.635] |
| episode right | 0.625 [0.542, 0.708] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.75 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.96 |
| followup_save | 24 | 0.50 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.61 |
| search_then_save | 36 | 0.67 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'This is what drafts/notes-2026.md contains:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'The contents of archive/results.md:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'This is what research/checklist.md contains:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00795` search_then_save: reply lacks the tool's fact | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> "It's in archive/notes-2026.txt now."
- `mt_test_id_g-00798` search_then_save: reply lacks the tool's fact | 'Look up the soak test in the documentation and write the top result into data/raw/invoice.toml. Please check.' -> "It's in data/raw/invoice.toml now."
- `mt_test_id_g-00801` search_then_save: reply lacks the tool's fact | 'Find the passage about the SSRF egress guard and store it in scripts/notes-2026.toml.' -> "It's in scripts/notes-2026.toml now."
- `mt_test_id_g-00804` search_then_save: reply lacks the tool's fact | 'Get me the most relevant chunk on cancellation of requests from the index, then save it as data/raw/checklist.toml.' -> 'Saved to data/raw/checklist.toml.'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.972 [0.952, 0.992] |
| L1 json | 0.968 [0.944, 0.988] |
| L2 schema | 0.968 [0.944, 0.988] |
| L3 tool | 0.905 [0.865, 0.940] |
| L4 args | 0.897 [0.857, 0.933] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.985 [0.973, 0.996] |
| step right | 0.770 [0.730, 0.808] |
| answer grounded | 0.512 [0.438, 0.588] |
| episode right | 0.540 [0.470, 0.610] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.69 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.50 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.50 |
| search_then_save | 60 | 0.63 |
| stats_then_search | 54 | 0.76 |

Failures (first 12):

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
- `mt_test_ood_g-00562` check_then_read: reply lacks the tool's fact | 'Okay, next: Only if archive/outline.md is present, display its contents.' -> 'The contents of archive/outline.md:\n\nbudget approved\npick up the parcel'
