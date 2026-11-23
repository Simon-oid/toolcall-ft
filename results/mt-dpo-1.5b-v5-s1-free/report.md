# mt-dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.973 [0.947, 0.993] |
| L1 json | 0.973 [0.947, 0.993] |
| L2 schema | 0.973 [0.947, 0.993] |
| L3 tool | 0.973 [0.947, 0.993] |
| L4 args | 0.960 [0.927, 0.987] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.985 [0.970, 0.996] |
| step right | 0.974 [0.952, 0.993] |
| answer grounded | 0.990 [0.969, 1.000] |
| episode right | 0.942 [0.892, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 1.00 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 0.92 |
| followup_save | 24 | 0.96 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 0.92 |
| search_then_save | 36 | 0.97 |
| stats_then_search | 34 | 1.00 |

Failures (first 12):

- `mt_test_id-00817` search_then_save: fails json no call | 'Hey there. Find the passage about log redaction and store it in archive/outline.txt.' -> 'Sure, but I need one detail first. What should I look up?'
- `mt_test_id-01105` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/results.txt.' -> 'Sure, but I need one detail first. Which folder should I save it in?'
- `mt_test_id-01123` list_then_write: fails json no call | 'Put the names of the files in archive into data/raw/checklist.md.' -> 'Sure, but I need one detail first. Which folder should I save it in?'
- `mt_test_id-01129` list_then_write: fails json no call | 'One more thing: Record which files are in drafts in the file scripts/readme.md.' -> 'I can do that once I know more. Which files should I save in drafts?'
- `mt_test_id-01624` followup_read: fails args  | 'Read the second one.' -> '{"name": "fs_read", "arguments": {"path": "notes-2026.md"}}'
- `mt_test_id-01628` followup_read: fails args  | "What's in the third file?" -> '{"name": "fs_read", "arguments": {"path": "research/results.py"}}'
- `mt_test_id-02025` followup_save: reply lacks the tool's fact | 'Store it as data/raw/outline.txt.' -> 'Saved to docs/soak-test.md: The soak test runs the server for six hours under steady load.'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.893 [0.853, 0.929] |
| L1 json | 0.877 [0.833, 0.917] |
| L2 schema | 0.877 [0.833, 0.917] |
| L3 tool | 0.833 [0.786, 0.877] |
| L4 args | 0.829 [0.782, 0.873] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.940 [0.918, 0.962] |
| step right | 0.905 [0.876, 0.931] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.800 [0.745, 0.855] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 0.97 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 0.90 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.77 |
| search_then_save | 60 | 0.88 |
| stats_then_search | 54 | 0.69 |

Failures (first 12):

- `mt_test_ood-00829` search_then_save: fails json no call | 'Grab whatever the corpus ranks first for cancellation of requests and file it under drafts/results.md. Much appreciated.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00841` search_then_save: fails json no call | 'One more thing: Grab whatever the corpus ranks first for the HNSW index and file it under archive/agenda.txt.' -> 'I can do that once I know more. What should I search the docs for?'
- `mt_test_ood-00847` search_then_save: fails json no call | 'Grab whatever the corpus ranks first for structured tool output and file it under research/invoice.toml. Please check.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00859` search_then_save: fails json no call | 'Hey there. Grab whatever the corpus ranks first for the soak test and file it under research/outline.txt.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00862` search_then_save: fails json no call | 'Query the index on structured tool output; the top chunk should end up in archive/readme.toml. Much appreciated.' -> 'Sure, but I need one detail first: what topic should archive/readme.toml contain?'
- `mt_test_ood-00865` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for the HNSW index and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-00871` search_then_save: fails json no call | 'Okay, next: Grab whatever the corpus ranks first for structured tool output and file it under drafts/checklist.md.' -> 'I can do that once I know more. What should I look up?'
- `mt_test_ood-01135` list_then_write: fails json no call | 'Hey there. Catalogue the files under drafts and store the catalogue in research/results.txt.' -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research: [\\"article1\\", \\"paper2\\", \\"thesis3\\"]"}}'
- `mt_test_ood-01144` list_then_write: fails json no call | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> 'I can do that once I know more. What should the file contain?'
- `mt_test_ood-01145` list_then_write: fails json no call | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> 'I can do that once I know more. What text should the file contain?'
- `mt_test_ood-01150` list_then_write: fails json  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/agenda.toml", "content": "archive: books, papers, notes, images, videos"})'
