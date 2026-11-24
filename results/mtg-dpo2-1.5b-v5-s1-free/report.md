# mtg-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 722

## mt_test_id_g (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.973 [0.947, 0.993] |
| L2 schema | 0.973 [0.947, 0.993] |
| L3 tool | 0.967 [0.933, 0.993] |
| L4 args | 0.960 [0.927, 0.987] |
| abstain | 0.842 [0.775, 0.908] |
| decision | 0.930 [0.900, 0.959] |
| step right | 0.870 [0.830, 0.911] |
| answer grounded | 0.875 [0.802, 0.938] |
| episode right | 0.725 [0.642, 0.800] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.72 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 0.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 0.96 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 0.58 |
| list_then_write | 36 | 0.97 |
| search_then_save | 36 | 0.92 |
| stats_then_search | 34 | 0.88 |

Failures (first 12):

- `mt_test_id_g-00495` check_then_read: reply lacks the tool's fact | 'If research/invoice.toml exists, show me what it says.' -> 'research/invoice.toml says:\n\nall tests passing'
- `mt_test_id_g-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'The contents of drafts/notes-2026.md:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00503` check_then_read: fails tool  | "See if there's a file at drafts/checklist.txt; if there is, show it." -> '{"name": "crag_search", "arguments": {"query": "drafts/checklist.txt"}}'
- `mt_test_id_g-00505` check_then_read: reply lacks the tool's fact | "See if there's a file at drafts/checklist.txt; if there is, show it." -> 'The contents of drafts/checklist.txt:\n\npick up the parcel'
- `mt_test_id_g-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'archive/results.md says:\n\nall tests passing\nrerun the benchmark'
- `mt_test_id_g-00511` check_then_read: reply lacks the tool's fact | 'If data/raw/readme.txt exists, show me what it says.' -> 'The contents of data/raw/readme.txt:\n\nrerun the benchmark\nbudget approved'
- `mt_test_id_g-00514` check_then_read: reply lacks the tool's fact | 'Check whether drafts/results.txt is there, and read it if it is.' -> 'The contents of drafts/results.txt:\n\nbudget approved'
- `mt_test_id_g-00521` check_then_read: reply lacks the tool's fact | "See if there's a file at research/checklist.md; if there is, show it." -> 'The contents of research/checklist.md:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_id_g-00524` check_then_read: reply lacks the tool's fact | 'Verify that data/raw/proposal.txt exists and then read it to me.' -> 'The contents of data/raw/proposal.txt:\n\nrerun the benchmark\nlunch at noon on Friday'
- `mt_test_id_g-00793` search_then_save: fails json  | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}'
- `mt_test_id_g-00805` search_then_save: fails json  | 'Check the knowledge base for rate limiting at accept and put the best hit in data/raw/results.toml.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}'
- `mt_test_id_g-00821` search_then_save: fails args  | 'Get me the most relevant chunk on the HNSW index from the index, then save it as scripts/invoice.toml. Please check.' -> '{"name": "fs_write", "arguments": {"path": "scripts/invoice.toml", "content": "Tools can return structuredContent alongside the text content'

## mt_test_ood_g (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.929 [0.893, 0.956] |
| L2 schema | 0.921 [0.885, 0.952] |
| L3 tool | 0.893 [0.853, 0.929] |
| L4 args | 0.889 [0.849, 0.925] |
| abstain | 0.815 [0.760, 0.865] |
| decision | 0.918 [0.894, 0.942] |
| step right | 0.812 [0.774, 0.847] |
| answer grounded | 0.825 [0.762, 0.881] |
| episode right | 0.620 [0.555, 0.685] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.64 |
| find_then_read | 60 | 0.97 |
| followup_ask | 20 | 0.05 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.95 |
| followup_stat | 40 | 0.95 |
| followup_thanks | 20 | 0.50 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.74 |

Failures (first 12):

- `mt_test_ood_g-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood_g-00276` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "path": "drafts"}}'
- `mt_test_ood_g-00527` check_then_read: reply lacks the tool's fact | 'Only if drafts/outline.toml is present, display its contents. Cheers.' -> 'The contents of drafts/outline.toml:\n\npick up the parcel\nlunch at noon on Friday'
- `mt_test_ood_g-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood_g-00530` check_then_read: reply lacks the tool's fact | 'Is there a research/proposal.md? Read it out if so.' -> 'The contents of research/proposal.md:\n\nbudget approved\nall tests passing'
- `mt_test_ood_g-00533` check_then_read: reply lacks the tool's fact | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> 'Here is data/raw/readme.toml:\n\nrerun the benchmark\nall tests passing'
- `mt_test_ood_g-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'The contents of data/raw/invoice.txt:\n\nrerun the benchmark'
- `mt_test_ood_g-00541` check_then_read: reply lacks the tool's fact | 'One more thing: Is there a scripts/invoice.md? Read it out if so.' -> 'scripts/invoice.md says:\n\nrerun the benchmark\npick up the parcel'
- `mt_test_ood_g-00544` check_then_read: reply lacks the tool's fact | 'Only if archive/results.py is present, display its contents. Cheers.' -> 'archive/results.py says:\n\nbudget approved\nlunch at noon on Friday'
- `mt_test_ood_g-00547` check_then_read: reply lacks the tool's fact | 'Is there a archive/readme.txt? Read it out if so.' -> 'The contents of archive/readme.txt:\n\nall tests passing\nbudget approved'
- `mt_test_ood_g-00548` check_then_read: fails tool  | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "research/readme.txt is present"}}'
- `mt_test_ood_g-00550` check_then_read: reply lacks the tool's fact | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> 'Here is research/readme.txt:\n\npick up the parcel\nbudget approved'
