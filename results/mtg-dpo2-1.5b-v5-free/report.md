# mtg-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.980 [0.953, 1.000] |
| L2 schema | 0.973 [0.947, 0.993] |
| L3 tool | 0.973 [0.947, 0.993] |
| L4 args | 0.967 [0.933, 0.993] |
| abstain | 0.842 [0.775, 0.908] |
| decision | 0.930 [0.900, 0.959] |
| step right | 0.889 [0.852, 0.926] |
| answer grounded | 0.833 [0.760, 0.906] |
| episode right | 0.750 [0.675, 0.825] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.75 |
| find_then_read | 36 | 0.97 |
| followup_ask | 12 | 0.33 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 0.83 |
| followup_thanks | 12 | 0.92 |
| list_then_write | 36 | 0.94 |
| search_then_save | 36 | 0.89 |
| stats_then_search | 34 | 0.94 |

Failures (first 12):

- `mt_test_id_g-00218` find_then_read: called '{"name": "fs_write", "arguments": {"path": "archive/notes-2026.toml", "content": "rerun the benchmark\\n"}}' | "Okay, next: There's a notes-2026 file somewhere in archive; read it to me."
- `mt_test_id_g-00495` check_then_read: called '{"name": "crag_search", "arguments": {"query": "all tests passing"}}' | 'If research/invoice.toml exists, show me what it says.'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> '<tool_call>\n<tool_call>\n<tool_call>'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: called '{"name": "fs_write", "arguments": {"path": "archive/results.md", "content": "all tests passing\\nrerun the benchmark\\n"}}' | 'Verify that archive/results.md exists and then read it to me.'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'data/raw/readme.txt says:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: called '{"name": "fs_write", "arguments": {"path": "research/updated_checklist.md", "content": "rerun the benchmark\\npick up the' | "See if there's a file at research/checklist.md; if there is, show it."
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> '<tool_call>\n<tool_call>\n<tool_call>'
- `mt_test_id_g-00793` search_then_save: fails json  | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "docs", "subpaths": ["accept"]}'
- `mt_test_id_g-00803` search_then_save: fails json  | 'Get me the most relevant chunk on cancellation of requests from the index, then save it as data/raw/checklist.toml.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/checklist.toml", "content": "A notifications/cancelled message stops the handler at its'
- `mt_test_id_g-00805` search_then_save: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Check the knowledge base for rate limiting at accept and put the best hit in data/raw/results.toml.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting at accept", "path": "accept"}}'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.984 [0.968, 0.996] |
| L2 schema | 0.980 [0.960, 0.996] |
| L3 tool | 0.925 [0.889, 0.956] |
| L4 args | 0.905 [0.869, 0.940] |
| abstain | 0.755 [0.695, 0.815] |
| decision | 0.892 [0.863, 0.920] |
| step right | 0.812 [0.774, 0.847] |
| answer grounded | 0.750 [0.681, 0.812] |
| episode right | 0.620 [0.555, 0.685] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.69 |
| find_then_read | 60 | 0.92 |
| followup_ask | 20 | 0.05 |
| followup_read | 40 | 0.90 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 0.62 |
| followup_thanks | 20 | 0.90 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 0.93 |
| stats_then_search | 54 | 0.93 |

Failures (first 12):

- `mt_test_ood_g-00249` find_then_read: fails tool  | 'Somewhere in research there is a file named checklist. What does it say?' -> '{"name": "fs_read", "arguments": {"path": "research/checklist"}}'
- `mt_test_ood_g-00257` find_then_read: called '{"name": "fs_write", "arguments": {"path": "data/raw/invoice.txt", "content": "rerun the benchmark\\n"}}' | 'Hey there. Somewhere in data/raw there is a file named invoice. What does it say?'
- `mt_test_ood_g-00260` find_then_read: called '{"name": "fs_write", "arguments": {"path": "research/outline.md", "content": "all tests passing\\n"}}' | 'Can you track down the outline file under research and print it?'
- `mt_test_ood_g-00302` find_then_read: called '{"name": "fs_write", "arguments": {"path": "research/agenda.py", "content": "all tests passing\\nrerun the benchmark\\n"}}' | 'Can you track down the agenda file under research and print it?'
- `mt_test_ood_g-00303` find_then_read: fails tool  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_stat", "arguments": {"path": "research/notes-2026"}}'
- `mt_test_ood_g-00527` check_then_read: called '{"name": "fs_write", "arguments": {"path": "docs/notes.txt", "content": "pick up the parcel\\nlunch at noon on Friday\\n"}' | 'Only if drafts/outline.toml is present, display its contents. Cheers.'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'budget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> '<tool_call>\n<tool_call>'
- `mt_test_ood_g-00538` check_then_read: called '{"name": "crag_search", "arguments": {"query": "rerun the benchmark"}}' | 'Only if data/raw/invoice.txt is present, display its contents.'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'scripts/invoice.md says:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: called '{"name": "fs_write", "arguments": {"path": "archive/results.txt", "content": "budget approved\\nlunch at noon on Friday\\n' | 'Only if archive/results.py is present, display its contents. Cheers.'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'archive/readme.txt says:\n\nall tests passing\nbudget approved'
