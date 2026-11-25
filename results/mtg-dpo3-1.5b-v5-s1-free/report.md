# mtg-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.960 [0.927, 0.987] |
| L1 json | 0.953 [0.920, 0.987] |
| L2 schema | 0.927 [0.880, 0.967] |
| L3 tool | 0.880 [0.827, 0.927] |
| L4 args | 0.880 [0.827, 0.927] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.978 [0.959, 0.993] |
| step right | 0.904 [0.867, 0.937] |
| answer grounded | 0.917 [0.854, 0.969] |
| episode right | 0.800 [0.725, 0.867] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.69 |
| find_then_read | 36 | 0.86 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.96 |
| followup_save | 24 | 0.92 |
| followup_stat | 24 | 0.92 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.94 |
| search_then_save | 36 | 0.92 |
| stats_then_search | 34 | 0.97 |

Failures (first 12):

- `mt_test_id_g-00210` find_then_read: fails json no call | 'One more thing: Open the outline file in data/raw.' -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "data/raw"}}.rmi\n<tool_call>'
- `mt_test_id_g-00214` find_then_read: fails tool  | 'Okay, next: Show me the agenda document that lives in research.' -> '{"name": "crag_search", "arguments": {"query": "the agenda document"}}'
- `mt_test_id_g-00219` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "scripts"}};\n<tool_call>'
- `mt_test_id_g-00223` find_then_read: fails tool  | 'Find the file called notes-2026 in archive and show me what it says.' -> '{"name": "crag_search", "arguments": {"query": "notes-2026"}}'
- `mt_test_id_g-00241` find_then_read: fails tool  | 'One more thing: Find the file called checklist in archive and show me what it says.' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'The contents of research/invoice.toml:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00503` check_then_read: fails tool  | "See if there's a file at drafts/checklist.txt; if there is, show it." -> '{"name": "crag_search", "arguments": {"query": "drafts/checklist.txt"}}'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'The contents of archive/results.md:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.885 [0.845, 0.921] |
| L1 json | 0.881 [0.841, 0.921] |
| L2 schema | 0.821 [0.774, 0.869] |
| L3 tool | 0.687 [0.627, 0.742] |
| L4 args | 0.679 [0.619, 0.734] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.936 [0.912, 0.958] |
| step right | 0.779 [0.741, 0.816] |
| answer grounded | 0.881 [0.831, 0.931] |
| episode right | 0.585 [0.515, 0.650] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.59 |
| find_then_read | 60 | 0.78 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.93 |
| followup_save | 40 | 0.72 |
| followup_stat | 40 | 0.70 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.78 |
| search_then_save | 60 | 0.87 |
| stats_then_search | 54 | 0.70 |

Failures (first 12):

- `mt_test_ood_g-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood_g-00247` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file"}}'
- `mt_test_ood_g-00252` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the proposal file under data/raw and print it?' -> '{"name": "crag_search", "arguments": {"query": "the proposal file", "path": "data/raw"}}'
- `mt_test_ood_g-00258` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the outline file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file", "path": "research"}}'
- `mt_test_ood_g-00259` find_then_read: fails tool  | 'Can you track down the outline file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file"}}'
- `mt_test_ood_g-00276` find_then_read: fails tool  | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood_g-00277` find_then_read: fails tool  | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "results file"}}'
- `mt_test_ood_g-00283` find_then_read: fails tool  | 'Can you track down the proposal file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "proposal file"}}'
- `mt_test_ood_g-00288` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the outline file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file", "path": "scripts"}}'
- `mt_test_ood_g-00289` find_then_read: fails tool  | 'Can you track down the outline file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "outline file"}}'
- `mt_test_ood_g-00295` find_then_read: fails tool  | 'Can you track down the checklist file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt_test_ood_g-00300` find_then_read: fails json no call | 'Can you track down the agenda file under research and print it?' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the agenda"}};\n,{"name": "crag_read", "arguments": {"path": "research/agenda"}};'
