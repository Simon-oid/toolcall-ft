# mtg-dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.973 [0.947, 0.993] |
| L1 json | 0.973 [0.947, 0.993] |
| L2 schema | 0.973 [0.947, 0.993] |
| L3 tool | 0.973 [0.947, 0.993] |
| L4 args | 0.960 [0.927, 0.987] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.985 [0.970, 0.996] |
| step right | 0.944 [0.915, 0.970] |
| answer grounded | 0.906 [0.844, 0.958] |
| episode right | 0.875 [0.817, 0.933] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.75 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.92 |
| followup_save | 24 | 0.96 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.92 |
| search_then_save | 36 | 0.97 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'The contents of archive/results.md:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'The contents of research/checklist.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00817` search_then_save: fails json no call | 'Hey there. Find the passage about log redaction and store it in archive/outline.txt.' -> 'Sure, but I need one detail first. What should I look up?'
- `mt_test_id_g-01105` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/results.txt.' -> 'Sure, but I need one detail first. Which folder should I save it in?'
- `mt_test_id_g-01123` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/checklist.md.' -> 'Sure, but I need one detail first. Which folder should I save it in?'
- `mt_test_id_g-01129` list_then_write: fails json no call | 'One more thing: Record which files are in drafts in the file scripts/readme.md.' -> 'I can do that once I know more. Which files should I save in drafts?'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.893 [0.853, 0.929] |
| L1 json | 0.877 [0.833, 0.917] |
| L2 schema | 0.877 [0.833, 0.917] |
| L3 tool | 0.833 [0.786, 0.877] |
| L4 args | 0.829 [0.782, 0.873] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.940 [0.918, 0.962] |
| step right | 0.865 [0.832, 0.896] |
| answer grounded | 0.887 [0.838, 0.931] |
| episode right | 0.710 [0.645, 0.770] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.69 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 0.90 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 0.88 |
| stats_then_search | 54 | 0.69 |

Failures (first 12):

- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'Here is drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'Here is data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'Here is data/raw/invoice.txt:\n\nrerun the benchmark'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'The contents of archive/results.py:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'Here is research/readme.txt:\n\npick up the parcel\nbudget approved'
- `mt_test_ood_g-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\nall tests passing'
- `mt_test_ood_g-00556` check_then_read: reply lacks the tool's fact | 'Only if research/invoice.toml is present, display its contents. Please check.' -> 'Here is research/invoice.toml:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00559` check_then_read: reply lacks the tool's fact | 'Okay, next: Is there a drafts/agenda.py? Read it out if so.' -> 'The contents of drafts/agenda.py:\n\nlunch at noon on Friday\nbudget approved'
- `mt_test_ood_g-00562` check_then_read: reply lacks the tool's fact | 'Okay, next: Only if archive/outline.md is present, display its contents.' -> 'The contents of archive/outline.md:\n\nbudget approved\npick up the parcel'
