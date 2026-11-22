# mt-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-17-gdbc46be-dirty · date: 2026-11-21 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.907 [0.860, 0.953] |
| L1 json | 0.900 [0.847, 0.947] |
| L2 schema | 0.900 [0.847, 0.947] |
| L3 tool | 0.820 [0.760, 0.880] |
| L4 args | 0.780 [0.713, 0.847] |
| abstain | 0.908 [0.858, 0.958] |
| decision | 0.907 [0.870, 0.941] |
| step right | 0.826 [0.781, 0.870] |
| answer grounded | 0.938 [0.885, 0.979] |
| episode right | 0.658 [0.575, 0.742] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.88 |
| find_then_read | 36 | 0.78 |
| followup_ask | 12 | 0.33 |
| followup_read | 24 | 0.83 |
| followup_save | 24 | 0.96 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.69 |
| search_then_save | 36 | 0.92 |
| stats_then_search | 34 | 0.76 |

Failures (first 12):

- `mt_test_id-00210` find_then_read: fails tool  | 'One more thing: Open the outline file in data/raw.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/outline.txt"}}'
- `mt_test_id-00213` find_then_read: fails tool  | 'Okay, next: Show me the agenda document that lives in research.' -> '{"name": "fs_read", "arguments": {"path": "research/agenda.txt"}}'
- `mt_test_id-00214` find_then_read: fails json no call | 'Okay, next: Show me the agenda document that lives in research.' -> 'The `research` directory contains the following files:\n- `agenda.toml`\n- `invoice.md`\n- `outline.txt`\n- `results.toml`\n\nWhich one is the age'
- `mt_test_id-00219` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> "Could you please specify the path to the checklist file in the `scripts` directory? If you're not sure about the exact path, you can provide"
- `mt_test_id-00228` find_then_read: fails tool  | 'Open the invoice file in scripts.' -> '{"name": "fs_read", "arguments": {"path": "scripts/invoice.txt"}}'
- `mt_test_id-00232` find_then_read: fails json no call | 'Show me the invoice document that lives in scripts.' -> 'The invoice document lives in the `scripts` directory and is named `invoice.toml`. \n\nWould you like to read the contents of this file?'
- `mt_test_id-00234` find_then_read: fails json no call | "Hey there. There's a proposal file somewhere in research; read it to me." -> 'To proceed, I need to know the path to the proposal file within the research directory. Could you provide the path, or let me know the name '
- `mt_test_id-00238` find_then_read: fails json no call | "Okay, next: I don't remember the extension, but read the proposal file in scripts." -> 'I see there are a few files in `scripts`: `agenda.txt`, `invoice.toml`, and `proposal.toml`. Could you please specify which one you would li'
- `mt_test_id-00493` check_then_read: fails tool  | 'If research/invoice.toml exists, show me what it says.' -> '{"name": "fs_read", "arguments": {"path": "research/invoice.toml"}}'
- `mt_test_id-00495` check_then_read: called '{"name": "fs_read", "arguments": {"path": "research/invoice.toml"}}' | 'If research/invoice.toml exists, show me what it says.'
- `mt_test_id-00509` check_then_read: fails tool  | 'If data/raw/readme.txt exists, show me what it says.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/readme.txt"}}'
- `mt_test_id-00518` check_then_read: called '{"name": "fs_list", "arguments": {"path": "data/raw"}}' | 'Make sure data/raw/readme.md exists first, then open it.'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.940 [0.909, 0.968] |
| L1 json | 0.937 [0.905, 0.964] |
| L2 schema | 0.937 [0.905, 0.964] |
| L3 tool | 0.794 [0.742, 0.841] |
| L4 args | 0.786 [0.734, 0.837] |
| abstain | 0.900 [0.855, 0.940] |
| decision | 0.923 [0.898, 0.947] |
| step right | 0.834 [0.799, 0.867] |
| answer grounded | 0.981 [0.956, 1.000] |
| episode right | 0.660 [0.595, 0.725] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 0.90 |
| followup_ask | 20 | 0.10 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 0.90 |
| followup_stat | 40 | 1.00 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.63 |
| search_then_save | 60 | 0.85 |
| stats_then_search | 54 | 0.70 |

Failures (first 12):

- `mt_test_ood-00249` find_then_read: fails tool  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "checklist"}}'
- `mt_test_ood-00260` find_then_read: called '{"name": "fs_read", "arguments": {"path": "research/outline.md"}}' | 'Can you track down the outline file under research and print it?'
- `mt_test_ood-00264` find_then_read: fails tool  | 'Can you track down the notes-2026 file under drafts and print it?' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026"}}'
- `mt_test_ood-00279` find_then_read: fails tool  | 'Somewhere in archive there is a file named results. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "archive/results"}}'
- `mt_test_ood-00302` find_then_read: called '{"name": "fs_list", "arguments": {"path": "research"}}' | 'Can you track down the agenda file under research and print it?'
- `mt_test_ood-00303` find_then_read: fails tool  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "notes-2026"}}'
- `mt_test_ood-00830` search_then_save: fails tool  | 'Grab whatever the corpus ranks first for cancellation of requests and file it under drafts/results.md. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "docs/cancellation-requests.md"}}'
- `mt_test_ood-00839` search_then_save: fails json no call | 'Query the index on the SSRF egress guard; the top chunk should end up in research/readme.toml. Cheers.' -> 'The top chunk from the query does not end up in `research/readme.toml`. Instead, it is from `docs/ssrf-egress-guard.md`, which states:\n\n"The'
- `mt_test_ood-00851` search_then_save: fails tool  | 'Query the index on cancellation of requests; the top chunk should end up in scripts/readme.md.' -> '{"name": "fs_read", "arguments": {"path": "scripts/readme.md"}}'
- `mt_test_ood-00860` search_then_save: fails json  | 'Hey there. Grab whatever the corpus ranks first for the soak test and file it under research/outline.txt.' -> '{"name": "fs_write", "arguments": {"content": "[cos 0.763  bm25 4.04  fusion 0.033] docs/soak-test.md\nThe soak test runs the server for six '
- `mt_test_ood-00863` search_then_save: fails tool  | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "docs/structured-tool-output.md"}}'
- `mt_test_ood-00866` search_then_save: fails tool  | 'Okay, next: Grab whatever the corpus ranks first for the HNSW index and file it under drafts/checklist.md.' -> '{"name": "fs_read", "arguments": {"path": "drafts/checklist.md"}}'
