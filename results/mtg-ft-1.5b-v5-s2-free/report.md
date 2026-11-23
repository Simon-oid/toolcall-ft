# mtg-ft-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

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
| step right | 0.837 [0.793, 0.878] |
| answer grounded | 0.542 [0.448, 0.635] |
| episode right | 0.633 [0.550, 0.717] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.75 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 0.50 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.67 |
| search_then_save | 36 | 0.67 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'Here is drafts/notes-2026.md:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'Here is drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'The contents of archive/results.md:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'Here is research/checklist.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'Here is data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00795` search_then_save: reply lacks the tool's fact | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> 'Saved to archive/notes-2026.txt.'
- `mt_test_id_g-00798` search_then_save: reply lacks the tool's fact | 'Look up the soak test in the documentation and write the top result into data/raw/invoice.toml. Please check.' -> 'I wrote it to data/raw/invoice.toml.'
- `mt_test_id_g-00801` search_then_save: reply lacks the tool's fact | 'Find the passage about the SSRF egress guard and store it in scripts/notes-2026.toml.' -> "It's in scripts/notes-2026.toml now."
- `mt_test_id_g-00804` search_then_save: reply lacks the tool's fact | 'Get me the most relevant chunk on cancellation of requests from the index, then save it as data/raw/checklist.toml.' -> 'Saved to data/raw/checklist.toml.'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.996 [0.988, 1.000] |
| L1 json | 0.996 [0.988, 1.000] |
| L2 schema | 0.992 [0.980, 1.000] |
| L3 tool | 0.921 [0.885, 0.952] |
| L4 args | 0.909 [0.873, 0.944] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.998 [0.993, 1.000] |
| step right | 0.777 [0.737, 0.814] |
| answer grounded | 0.512 [0.438, 0.588] |
| episode right | 0.605 [0.540, 0.675] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.59 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.42 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.45 |
| search_then_save | 60 | 0.67 |
| stats_then_search | 54 | 0.98 |

Failures (first 12):

- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'Here is drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'Here is data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'Here is data/raw/invoice.txt:\n\nrerun the benchmark'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'The contents of archive/results.py:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'Here is research/readme.txt:\n\npick up the parcel\nbudget approved'
- `mt_test_ood_g-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\nall tests passing'
