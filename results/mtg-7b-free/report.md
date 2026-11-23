# mtg-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.907 [0.860, 0.953] |
| L1 json | 0.900 [0.847, 0.947] |
| L2 schema | 0.900 [0.847, 0.947] |
| L3 tool | 0.820 [0.760, 0.880] |
| L4 args | 0.780 [0.713, 0.847] |
| abstain | 0.908 [0.858, 0.958] |
| decision | 0.907 [0.870, 0.941] |
| step right | 0.752 [0.700, 0.804] |
| answer grounded | 0.729 [0.635, 0.812] |
| episode right | 0.517 [0.425, 0.608] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.66 |
| find_then_read | 36 | 0.78 |
| followup_ask | 12 | 0.33 |
| followup_read | 24 | 0.83 |
| followup_save | 24 | 0.54 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.64 |
| search_then_save | 36 | 0.89 |
| stats_then_search | 34 | 0.76 |

Failures (first 12):

- `mt_test_id_g-00210` find_then_read: fails tool  | 'One more thing: Open the outline file in data/raw.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline.txt"}}'
- `mt_test_id_g-00213` find_then_read: fails tool  | 'Okay, next: Show me the agenda document that lives in research.' -> '{"name": "fs_read", "arguments": {"path": "research/agenda.txt"}}'
- `mt_test_id_g-00214` find_then_read: fails json no call | 'Okay, next: Show me the agenda document that lives in research.' -> 'The `research` directory contains the following files:\n- `agenda.toml`\n- `invoice.md`\n- `outline.txt`\n- `results.toml`\n\nWhich one is the age'
- `mt_test_id_g-00219` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> "Could you please specify the path to the checklist file in the `scripts` directory? If you're not sure about the exact path, you can provide"
- `mt_test_id_g-00228` find_then_read: fails tool  | 'Open the invoice file in scripts.' -> '{"name": "fs_read", "arguments": {"path": "scripts/invoice.txt"}}'
- `mt_test_id_g-00232` find_then_read: fails json no call | 'Show me the invoice document that lives in scripts.' -> 'The invoice document lives in the `scripts` directory and is named `invoice.toml`. \n\nWould you like to read the contents of this file?'
- `mt_test_id_g-00234` find_then_read: fails json no call | "Hey there. There's a proposal file somewhere in research; read it to me." -> 'To proceed, I need to know the path to the proposal file within the research directory. Could you provide the path, or let me know the name '
- `mt_test_id_g-00238` find_then_read: fails json no call | "Okay, next: I don't remember the extension, but read the proposal file in scripts." -> 'I see there are a few files in `scripts`: `agenda.txt`, `invoice.toml`, and `proposal.toml`. Could you please specify which one you would li'
- `mt_test_id_g-00493` check_then_read: fails tool  | 'If research/invoice.toml exists, show me what it says.' -> '{"name": "fs_read", "arguments": {"path": "research/invoice.toml"}}'
- `mt_test_id_g-00495` check_then_read: called '{"name": "fs_read", "arguments": {"path": "research/invoice.toml"}}' | 'If research/invoice.toml exists, show me what it says.'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The content of `drafts/notes-2026.md` is:\n```\nrerun the benchmark\nlunch at noon on Friday\n```\n\nIt seems to contain some notes or reminders. '
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The content of the file `drafts/checklist.txt` is:\n\n```\npick up the parcel\n```'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.940 [0.909, 0.968] |
| L1 json | 0.937 [0.905, 0.964] |
| L2 schema | 0.937 [0.905, 0.964] |
| L3 tool | 0.794 [0.742, 0.841] |
| L4 args | 0.786 [0.734, 0.837] |
| abstain | 0.900 [0.855, 0.940] |
| decision | 0.923 [0.898, 0.947] |
| step right | 0.748 [0.706, 0.788] |
| answer grounded | 0.738 [0.669, 0.806] |
| episode right | 0.480 [0.410, 0.550] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.69 |
| find_then_read | 60 | 0.90 |
| followup_ask | 20 | 0.10 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.47 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.58 |
| search_then_save | 60 | 0.83 |
| stats_then_search | 54 | 0.70 |

Failures (first 12):

- `mt_test_ood_g-00249` find_then_read: fails tool  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "checklist"}}'
- `mt_test_ood_g-00260` find_then_read: called '{"name": "fs_read", "arguments": {"path": "research/outline.md"}}' | 'Can you track down the outline file under research and print it?'
- `mt_test_ood_g-00264` find_then_read: fails tool  | 'Can you track down the notes-2026 file under drafts and print it?' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026"}}'
- `mt_test_ood_g-00279` find_then_read: fails tool  | 'Somewhere in archive there is a file named results. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "archive/results"}}'
- `mt_test_ood_g-00302` find_then_read: called '{"name": "fs_list", "arguments": {"path": "research"}}' | 'Can you track down the agenda file under research and print it?'
- `mt_test_ood_g-00303` find_then_read: fails tool  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "notes-2026"}}'
- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'The contents of `drafts/outline.toml` are as follows:\n\n1. pick up the parcel\n2. lunch at noon on Friday'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'The file `research/proposal.md` contains the following content:\n\n```\nbudget approved\nall tests passing\n```\n\nIt seems like the content is qui'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'The contents of the file `data/raw/readme.toml` are:\n\n```\nrerun the benchmark\nall tests passing\n```'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of the file `data/raw/invoice.txt` are:\n\n```\nrerun the benchmark\n```'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'The content of `scripts/invoice.md` is:\n```\nrerun the benchmark\npick up the parcel\n```'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'The contents of `archive/results.py` are as follows:\n\n```\nbudget approved\nlunch at noon on Friday\n```\n\nIs there anything specific you need h'
