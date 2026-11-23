# mtg-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.933 [0.887, 0.967] |
| L1 json | 0.933 [0.887, 0.967] |
| L2 schema | 0.933 [0.887, 0.967] |
| L3 tool | 0.933 [0.887, 0.967] |
| L4 args | 0.920 [0.873, 0.960] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.963 [0.937, 0.981] |
| step right | 0.922 [0.889, 0.952] |
| answer grounded | 0.906 [0.844, 0.958] |
| episode right | 0.833 [0.767, 0.892] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.72 |
| find_then_read | 36 | 0.94 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 0.92 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.86 |
| search_then_save | 36 | 0.94 |
| stats_then_search | 34 | 0.97 |

Failures (first 12):

- `mt_test_id_g-00225` find_then_read: fails json no call | 'Read whatever invoice file is inside archive.' -> 'I can do that once I know more. Which folder should I look in?'
- `mt_test_id_g-00234` find_then_read: fails json no call | "Hey there. There's a proposal file somewhere in research; read it to me." -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'I read drafts/notes-2026.md:\n\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'archive/results.md says:\n\nThis is what archive/results.md contains.'
- `mt_test_id_g-00509` check_then_read: fails args  | 'If data/raw/readme.txt exists, show me what it says.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00517` check_then_read: fails args  | 'Make sure data/raw/readme.md exists first, then open it.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00808` search_then_save: fails json no call | 'Pull the top passage on structured tool output out of the docs and write it to scripts/results.toml.' -> 'I can do that once I know more. What should I write in scripts/results.toml?'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.873 [0.829, 0.913] |
| L1 json | 0.873 [0.829, 0.913] |
| L2 schema | 0.861 [0.817, 0.901] |
| L3 tool | 0.841 [0.794, 0.885] |
| L4 args | 0.817 [0.770, 0.865] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.929 [0.905, 0.951] |
| step right | 0.858 [0.825, 0.889] |
| answer grounded | 0.887 [0.838, 0.931] |
| episode right | 0.735 [0.675, 0.795] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.67 |
| find_then_read | 60 | 0.98 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.97 |
| followup_stat | 40 | 0.93 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.65 |
| search_then_save | 60 | 0.87 |
| stats_then_search | 54 | 0.81 |

Failures (first 12):

- `mt_test_ood_g-00303` find_then_read: fails args  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_list", "arguments": {"path": "notes"}}'
- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'The contents of drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00531` check_then_read: fails args  | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'The contents of data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'The contents of scripts/invoice.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'archive/results.py says:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'archive/readme.txt says:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'The contents of research/readme.txt:\n\npick up the parcel\nbudget approved'
- `mt_test_ood_g-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\nall tests passing'
- `mt_test_ood_g-00556` check_then_read: reply lacks the tool's fact | 'Only if research/invoice.toml is present, display its contents. Please check.' -> 'Here is research/invoice.toml:\n\nbudget approved\nall tests passing'
