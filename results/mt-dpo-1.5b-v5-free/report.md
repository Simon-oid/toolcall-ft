# mt-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.933 [0.887, 0.967] |
| L1 json | 0.933 [0.887, 0.967] |
| L2 schema | 0.933 [0.887, 0.967] |
| L3 tool | 0.933 [0.887, 0.967] |
| L4 args | 0.920 [0.873, 0.960] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.963 [0.937, 0.981] |
| step right | 0.941 [0.911, 0.967] |
| answer grounded | 0.958 [0.917, 0.990] |
| episode right | 0.867 [0.800, 0.925] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 0.88 |
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

- `mt_test_id-00225` find_then_read: fails json no call | 'Read whatever invoice file is inside archive.' -> 'I can do that once I know more. Which folder should I look in?'
- `mt_test_id-00234` find_then_read: fails json no call | "Hey there. There's a proposal file somewhere in research; read it to me." -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt_test_id-00498` check_then_read: reply lacks the tool's fact | 'Hey there. Check whether drafts/notes-2026.md is there, and read it if it is.' -> 'I read drafts/notes-2026.md:\n\nlunch at noon on Friday'
- `mt_test_id-00508` check_then_read: reply lacks the tool's fact | 'Verify that archive/results.md exists and then read it to me.' -> 'archive/results.md says:\n\nThis is what archive/results.md contains.'
- `mt_test_id-00509` check_then_read: fails args  | 'If data/raw/readme.txt exists, show me what it says.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_id-00517` check_then_read: fails args  | 'Make sure data/raw/readme.md exists first, then open it.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_id-00808` search_then_save: fails json no call | 'Pull the top passage on structured tool output out of the docs and write it to scripts/results.toml.' -> 'I can do that once I know more. What should I write in scripts/results.toml?'
- `mt_test_id-00817` search_then_save: fails json no call | 'Hey there. Find the passage about log redaction and store it in archive/outline.txt.' -> 'I can do that once I know more. What should I look up first?'
- `mt_test_id-01105` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/results.txt.' -> 'I can do that once I know more. What should I write to data/raw/results.txt? Which folder should I search?'
- `mt_test_id-01108` list_then_write: fails json no call | 'Make data/raw/results.txt contain the file names from archive.' -> 'I can do that once I know more. What should I write in results.txt?'
- `mt_test_id-01111` list_then_write: fails json no call | 'Record which files are in archive in the file scripts/notes-2026.toml.' -> 'I can do that once I know more. What should I write in scripts/notes-2026.toml?'
- `mt_test_id-01123` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/checklist.md.' -> 'I can do that once I know more. What should I write in data/raw/checklist.md?'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.873 [0.829, 0.913] |
| L1 json | 0.873 [0.829, 0.913] |
| L2 schema | 0.861 [0.817, 0.901] |
| L3 tool | 0.841 [0.794, 0.885] |
| L4 args | 0.817 [0.770, 0.865] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.929 [0.905, 0.951] |
| step right | 0.892 [0.863, 0.920] |
| answer grounded | 0.981 [0.956, 1.000] |
| episode right | 0.805 [0.750, 0.860] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 0.93 |
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

- `mt_test_ood-00303` find_then_read: fails args  | 'Somewhere in research there is a file named notes-2026. What does it say?' -> '{"name": "fs_list", "arguments": {"path": "notes"}}'
- `mt_test_ood-00531` check_then_read: fails args  | 'Hey there. Only if data/raw/readme.toml is present, display its contents.' -> '{"name": "fs_stat", "arguments": {"path": "data/raw"}}'
- `mt_test_ood-00538` check_then_read: reply lacks the tool's fact | 'Only if data/raw/invoice.txt is present, display its contents.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00573` check_then_read: reply lacks the tool's fact | 'Only if scripts/agenda.py is present, display its contents.' -> 'Here is scripts/agenda.py:\n\ntests/2019-03-04: 18 lines\ntests/2019-03-05: 17 lines\ntests/2019-03-06: 16 lines\ntests/2019-03-07: 15 lines\ntest'
- `mt_test_ood-00579` check_then_read: reply lacks the tool's fact | 'Only if scripts/checklist.toml is present, display its contents. Cheers.' -> 'I can do that once I know more. What should I look up in the docs?'
- `mt_test_ood-00838` search_then_save: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Query the index on the SSRF egress guard; the top chunk should end up in research/readme.toml. Cheers.' -> '{"name": "crag_search", "arguments": {"query": "the SSRF egress guard", "path": "research"}}'
- `mt_test_ood-00841` search_then_save: fails json no call | 'One more thing: Grab whatever the corpus ranks first for the HNSW index and file it under archive/agenda.txt.' -> 'I can do that once I know more. What should I write in archive/agenda.txt?'
- `mt_test_ood-00859` search_then_save: fails json no call | 'Hey there. Grab whatever the corpus ranks first for the soak test and file it under research/outline.txt.' -> 'I can do that once I know more. What should I write in research/outline.txt?'
- `mt_test_ood-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00865` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for the HNSW index and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I write in drafts/checklist.md?'
- `mt_test_ood-00868` search_then_save: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'Query the index on the soak test; the top chunk should end up in scripts/outline.toml. Cheers.' -> '{"name": "crag_search", "arguments": {"query": "the soak test", "path": "scripts"}}'
- `mt_test_ood-00871` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for structured tool output and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I look up?'
