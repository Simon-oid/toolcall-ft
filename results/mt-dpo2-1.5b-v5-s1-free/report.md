# mt-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.973 [0.947, 0.993] |
| L2 schema | 0.973 [0.947, 0.993] |
| L3 tool | 0.967 [0.933, 0.993] |
| L4 args | 0.960 [0.927, 0.987] |
| abstain | 0.842 [0.775, 0.908] |
| decision | 0.930 [0.900, 0.959] |
| step right | 0.907 [0.874, 0.941] |
| answer grounded | 0.979 [0.948, 1.000] |
| episode right | 0.800 [0.725, 0.867] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.97 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 0.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 0.58 |
| list_then_write | 36 | 1.00 |
| search_then_save | 36 | 0.92 |
| stats_then_search | 34 | 0.88 |

Failures (first 12):

- `mt_test_id-00503` check_then_read: fails tool  | "See if there's a file at drafts/checklist.txt; if there is, show it." -> '{"name": "crag_search", "arguments": {"query": "drafts/checklist.txt"}}'
- `mt_test_id-00793` search_then_save: fails json  | 'Search the docs for rate limiting at accept and save the best passage to archive/notes-2026.txt.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}'
- `mt_test_id-00805` search_then_save: fails json  | 'Check the knowledge base for rate limiting at accept and put the best hit in data/raw/results.toml.' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "path": "accept"}'
- `mt_test_id-00821` search_then_save: fails args  | 'Get me the most relevant chunk on the HNSW index from the index, then save it as scripts/invoice.toml. Please check.' -> '{"name": "fs_write", "arguments": {"path": "scripts/invoice.toml", "content": "Tools can return structuredContent alongside the text content'
- `mt_test_id-01389` stats_then_search: called '{"name": "crag_search", "arguments": {"query": "the soak test"}}' | 'First make sure documents are indexed, then find the soak test.'
- `mt_test_id-01393` stats_then_search: fails json  | 'Confirm the index has chunks and then search for structured tool output.' -> '{"name": "crag_stats", "arguments": {}'
- `mt_test_id-01394` stats_then_search: called '{"name": "crag_search", "arguments": {"query": "structured tool output"}}' | 'Confirm the index has chunks and then search for structured tool output.'
- `mt_test_id-01413` stats_then_search: fails json  | 'See whether the index is populated; if so, look for cancellation of requests.' -> '{"name": "crag_stats", "arguments": {}'
- `mt_test_id-02152` followup_ask: called '{"name": "fs_write", "arguments": {"path": "data/processed.txt", "content": "agenda.toml\\nchecklist.py\\nresults.toml\\n"}' | 'Save that.'
- `mt_test_id-02153` followup_ask: called '{"name": "fs_write", "arguments": {"path": "docs/notes.txt", "content": "pick up the parcel\\nrerun the benchmark"}}' | 'Write it to a file.'
- `mt_test_id-02154` followup_ask: called '{"name": "fs_write", "arguments": {"path": "docs/hnsw-index-impl.md", "content": "HNSW is not implemented; the exact sca' | 'Put that in a file for me.'
- `mt_test_id-02155` followup_ask: called '{"name": "fs_write", "arguments": {"path": "docs/test.txt", "content": "The soak test runs the server for six hours unde' | 'Store the result.'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.929 [0.893, 0.956] |
| L2 schema | 0.921 [0.885, 0.952] |
| L3 tool | 0.893 [0.853, 0.929] |
| L4 args | 0.889 [0.849, 0.925] |
| abstain | 0.815 [0.760, 0.865] |
| decision | 0.918 [0.894, 0.942] |
| step right | 0.854 [0.821, 0.887] |
| answer grounded | 0.944 [0.906, 0.975] |
| episode right | 0.700 [0.635, 0.765] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.95 |
| find_then_read | 60 | 0.97 |
| followup_ask | 20 | 0.05 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 0.97 |
| followup_stat | 40 | 0.95 |
| followup_thanks | 20 | 0.50 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.74 |

Failures (first 12):

- `mt_test_ood-00246` find_then_read: fails tool  | 'Can you track down the results file under research and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "k": 1}}'
- `mt_test_ood-00276` find_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Can you track down the results file under drafts and print it?' -> '{"name": "crag_search", "arguments": {"query": "the results file", "path": "drafts"}}'
- `mt_test_ood-00528` check_then_read: fails tool  | 'Is there a research/proposal.md? Read it out if so.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt_test_ood-00548` check_then_read: fails tool  | 'Only if research/readme.txt is present, display its contents. Much appreciated.' -> '{"name": "crag_search", "arguments": {"query": "research/readme.txt is present"}}'
- `mt_test_ood-00560` check_then_read: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Okay, next: Only if archive/outline.md is present, display its contents.' -> '{"name": "crag_stats", "arguments": {"path": "archive/outline.md"}}'
- `mt_test_ood-01138` list_then_write: fails json  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "an inventory of research"})'
- `mt_test_ood-01139` list_then_write: fails json  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "agenda.md\\noutline.txt\\nresults.md\\n"})'
- `mt_test_ood-01144` list_then_write: fails json  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/drafts", "content": "an inventory of drafts"})'
- `mt_test_ood-01145` list_then_write: fails json  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/readme.py", "content": "notes-2026.toml\\nreadme.py\\n"})'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive\\ninventory\\nof\\ndata\\nraw\\nagenda\\n.toml\\n"}}'
- `mt_test_ood-01156` list_then_write: fails json  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "an inventory of drafts"})'
- `mt_test_ood-01162` list_then_write: fails json  | 'I want drafts/checklist.toml to hold an inventory of data/raw.' -> '{"name": "fs_write", "arguments": {"path": "drafts/checklist.toml", "content": "data/raw\\n"})'
