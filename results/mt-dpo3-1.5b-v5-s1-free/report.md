# mt-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.960 [0.927, 0.987] |
| L1 json | 0.953 [0.920, 0.987] |
| L2 schema | 0.927 [0.880, 0.967] |
| L3 tool | 0.880 [0.827, 0.927] |
| L4 args | 0.880 [0.827, 0.927] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.978 [0.959, 0.993] |
| step right | 0.933 [0.904, 0.963] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.850 [0.783, 0.908] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.94 |
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

- `mt_test_id-00210` find_then_read: fails json no call | 'One more thing: Open the outline file in data/raw.' -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "data/raw"}}.rmi\n<tool_call>'
- `mt_test_id-00214` find_then_read: fails tool  | 'Okay, next: Show me the agenda document that lives in research.' -> '{"name": "crag_search", "arguments": {"query": "the agenda document"}}'
- `mt_test_id-00219` find_then_read: fails json no call | "I don't remember the extension, but read the checklist file in scripts." -> '<tool_call>\n{"name": "fs_list", "arguments": {"path": "scripts"}};\n<tool_call>'
- `mt_test_id-00223` find_then_read: fails tool  | 'Find the file called notes-2026 in archive and show me what it says.' -> '{"name": "crag_search", "arguments": {"query": "notes-2026"}}'
- `mt_test_id-00241` find_then_read: fails tool  | 'One more thing: Find the file called checklist in archive and show me what it says.' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt_test_id-00503` check_then_read: fails tool  | "See if there's a file at drafts/checklist.txt; if there is, show it." -> '{"name": "crag_search", "arguments": {"query": "drafts/checklist.txt"}}'
- `mt_test_id-00519` check_then_read: fails tool  | "See if there's a file at research/checklist.md; if there is, show it." -> '{"name": "crag_search", "arguments": {"query": "research/checklist.md"}}'
- `mt_test_id-00793` search_then_save: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}}'
- `mt_test_id-00806` search_then_save: fails tool  | 'Check the knowledge base for rate limiting at accept and put the best hit in data/raw/results.toml.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting at put", "k": 1}}'
- `mt_test_id-00824` search_then_save: fails schema {'path': '/query', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Check the knowledge base for nDCG evaluation and put the best hit in data/raw/agenda.md. Cheers.' -> '{"name": "crag_stats", "arguments": {"query": "nDCG evaluation"}}'
- `mt_test_id-01108` list_then_write: fails tool  | 'Make data/raw/results.txt contain the file names from archive.' -> '{"name": "crag_search", "arguments": {"query": "archive", "k": 10}}'
- `mt_test_id-01123` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/checklist.md.' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "archive"}}'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.885 [0.845, 0.921] |
| L1 json | 0.881 [0.841, 0.921] |
| L2 schema | 0.821 [0.774, 0.869] |
| L3 tool | 0.687 [0.627, 0.742] |
| L4 args | 0.679 [0.619, 0.734] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.936 [0.912, 0.958] |
| step right | 0.816 [0.779, 0.852] |
| answer grounded | 0.988 [0.969, 1.000] |
| episode right | 0.635 [0.565, 0.700] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.88 |
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

- `mt_test_ood-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood-00247` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file"}}'
- `mt_test_ood-00252` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the proposal file under data/raw and print it?' -> '{"name": "crag_search", "arguments": {"query": "the proposal file", "path": "data/raw"}}'
- `mt_test_ood-00258` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the outline file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file", "path": "research"}}'
- `mt_test_ood-00259` find_then_read: fails tool  | 'Can you track down the outline file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file"}}'
- `mt_test_ood-00276` find_then_read: fails tool  | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood-00277` find_then_read: fails tool  | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "results file"}}'
- `mt_test_ood-00283` find_then_read: fails tool  | 'Can you track down the proposal file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "proposal file"}}'
- `mt_test_ood-00288` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the outline file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the outline file", "path": "scripts"}}'
- `mt_test_ood-00289` find_then_read: fails tool  | 'Can you track down the outline file under scripts and print it?' -> '{"name": "crag_search", "arguments": {"query": "outline file"}}'
- `mt_test_ood-00295` find_then_read: fails tool  | 'Can you track down the checklist file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt_test_ood-00300` find_then_read: fails json no call | 'Can you track down the agenda file under research and print it?' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the agenda"}};\n,{"name": "crag_read", "arguments": {"path": "research/agenda"}};'
