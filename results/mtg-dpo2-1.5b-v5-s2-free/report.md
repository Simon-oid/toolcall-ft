# mtg-dpo2-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 0.967 [0.933, 0.992] |
| decision | 0.985 [0.970, 0.996] |
| step right | 0.878 [0.837, 0.915] |
| answer grounded | 0.698 [0.604, 0.781] |
| episode right | 0.725 [0.642, 0.800] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.75 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 0.67 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 0.75 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.75 |
| search_then_save | 36 | 0.83 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'Here is research/invoice.toml:\n\n```toml\ninvoice:\n  amount: 100.50\n  date: 2026-04-15\n```\n\nThe file contains:\n\ninvoice:\n  amount: 100.50\n  da'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nlunch at noon on Friday'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> "archive/results.md says:\n\nThis is archive/results.md. It's 38 bytes long, and was last changed on 2026-04-05. It has mode 0644.\n\narchive/res"
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'Here is research/checklist.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00801` search_then_save: reply lacks the tool's fact | 'Find the passage about the SSRF egress guard and store it in scripts/notes-2026.toml.' -> 'Done: I saved it to scripts/notes-2026.toml.'
- `mt_test_id_g-00810` search_then_save: reply lacks the tool's fact | 'Pull the top passage on structured tool output out of the docs and write it to scripts/results.toml.' -> 'Done: I saved it to scripts/results.toml.'
- `mt_test_id_g-00813` search_then_save: reply lacks the tool's fact | 'Search the docs for log redaction and save the best passage to drafts/readme.txt.' -> 'Done: I saved it to drafts/readme.txt.'
- `mt_test_id_g-00819` search_then_save: reply lacks the tool's fact | 'Hey there. Find the passage about log redaction and store it in archive/outline.txt.' -> 'Done: I saved it to archive/outline.txt.'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.996 [0.988, 1.000] |
| L1 json | 0.996 [0.988, 1.000] |
| L2 schema | 0.996 [0.988, 1.000] |
| L3 tool | 0.933 [0.901, 0.960] |
| L4 args | 0.921 [0.885, 0.952] |
| abstain | 0.945 [0.910, 0.975] |
| decision | 0.973 [0.958, 0.987] |
| step right | 0.799 [0.761, 0.834] |
| answer grounded | 0.625 [0.550, 0.700] |
| episode right | 0.625 [0.560, 0.690] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.59 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 0.45 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.75 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.50 |
| search_then_save | 60 | 0.75 |
| stats_then_search | 54 | 0.98 |

Failures (first 12):

- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'The contents of drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'Here is research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'The contents of data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of data/raw/invoice.txt:\n\nInvoice 123456789\nDate: 2026-02-24\nAmount: $1,000.00\nDescription: Purchase of office supplies.'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'Here is scripts/invoice.md:\n\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'archive/results.py says:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00545` check_then_read: fails tool  | 'Is there a archive/readme.txt? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nbudget approved'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'Here is research/readme.txt:\n\npick up the parcel\nbudget approved'
- `mt_test_ood_g-00551` check_then_read: fails tool  | 'One more thing: Is there a research/results.toml? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00553` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a research/results.toml? Read it out if so.' -> 'Here is research/results.toml:\n\ntests/2026-02-12_19:03:57.txt: 18 bytes\n\nThis file contains one line, which says "tests/2026-02-12_19:03:57.'
