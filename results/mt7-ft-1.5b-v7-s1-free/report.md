# mt7-ft-1.5b-v7-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-26 · cases: 892

## mt7_test_id (190 need a call, 144 need none, 144 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.995 [0.984, 1.000] |
| L4 args | 0.958 [0.926, 0.984] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.976 [0.958, 0.991] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.944 [0.903, 0.979] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 55 | 1.00 |
| empty_then_asked | 12 | 1.00 |
| list_then_stat | 36 | 0.83 |
| missing_then_asked | 12 | 1.00 |
| read_edit_write | 36 | 0.97 |
| read_miss_then_list | 48 | 1.00 |
| read_next_page | 24 | 1.00 |
| search_dead_end | 24 | 1.00 |
| search_then_read_source | 36 | 1.00 |
| size_from_listing | 12 | 1.00 |
| user_corrects | 24 | 0.96 |
| write_then_check | 15 | 1.00 |

Failures (first 12):

- `mt7_test_id-01892` read_edit_write: fails args  | 'Append the setting region = eu-west to drafts/invoice.env.' -> '{"name": "fs_write", "arguments": {"path": "drafts/invoice.env", "content": "verbosity = loud\\nmax_conn = 256\\batch_size = 32\\nregion = eu-w'
- `mt7_test_id-02198` list_then_stat: fails args  | 'Find the smallest file in research and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "research/outline.md"}}'
- `mt7_test_id-02201` list_then_stat: fails args  | "What's the modification date of the smallest file in research?" -> '{"name": "fs_stat", "arguments": {"path": "research/agenda.toml"}}'
- `mt7_test_id-02204` list_then_stat: fails args  | 'In data/raw, which file is the smallest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "data/raw/outline.py"}}'
- `mt7_test_id-02216` list_then_stat: fails args  | 'Find the smallest file in drafts and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "drafts/outline.toml"}}'
- `mt7_test_id-02219` list_then_stat: fails args  | "What's the modification date of the largest file in archive?" -> '{"name": "fs_stat", "arguments": {"path": "archive/notes-2026.py"}}'
- `mt7_test_id-02222` list_then_stat: fails args  | 'In archive, which file is the biggest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "archive/notes-2026.py"}}'
- `mt7_test_id-02644` user_corrects: fails tool  | 'Hmm, no. Try scripts instead.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'

## mt7_test_ood (318 need a call, 240 need none, 240 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.969 [0.947, 0.987] |
| L1 json | 0.965 [0.943, 0.984] |
| L2 schema | 0.962 [0.940, 0.981] |
| L3 tool | 0.912 [0.881, 0.943] |
| L4 args | 0.877 [0.840, 0.912] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.982 [0.970, 0.993] |
| step right | 0.928 [0.907, 0.950] |
| answer grounded | 0.996 [0.988, 1.000] |
| episode right | 0.842 [0.796, 0.887] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 88 | 0.98 |
| empty_then_asked | 20 | 0.95 |
| list_then_stat | 60 | 0.87 |
| missing_then_asked | 20 | 1.00 |
| read_edit_write | 60 | 0.78 |
| read_miss_then_list | 80 | 0.88 |
| read_next_page | 40 | 1.00 |
| search_dead_end | 40 | 1.00 |
| search_then_read_source | 60 | 0.97 |
| size_from_listing | 20 | 1.00 |
| user_corrects | 40 | 0.97 |
| write_then_check | 30 | 0.90 |

Failures (first 12):

- `mt7_test_ood-00419` drill_down: fails tool  | 'proposal is buried in research somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "proposal", "k": 1}}'
- `mt7_test_ood-00445` drill_down: fails tool  | 'Okay, next: invoice is buried in research somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "invoice", "k": 1}}'
- `mt7_test_ood-00706` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in. Please check.' -> 'I can do that once I know more. What should I look up?'
- `mt7_test_ood-00730` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in.' -> 'What should I look up?'
- `mt7_test_ood-01092` read_miss_then_list: fails tool  | 'Get me the invoice file from data/raw; try data/raw/invoice.py first.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt7_test_ood-01100` read_miss_then_list: fails tool  | 'Hey there. Get me the results file from drafts; try drafts/results.txt first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt7_test_ood-01108` read_miss_then_list: fails tool  | 'Get me the invoice file from data/raw; try data/raw/invoice.toml first.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt7_test_ood-01116` read_miss_then_list: fails tool  | 'Hey there. Get me the outline file from drafts; try drafts/outline.py first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt7_test_ood-01124` read_miss_then_list: fails tool  | 'Hey there. Get me the proposal file from scripts; try scripts/proposal.md first.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt7_test_ood-01132` read_miss_then_list: fails tool  | 'Get me the results file from drafts; try drafts/results.toml first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt7_test_ood-01140` read_miss_then_list: fails tool  | 'One more thing: Get me the agenda file from research; try research/agenda.txt first.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt7_test_ood-01148` read_miss_then_list: fails tool  | 'One more thing: Get me the outline file from research; try research/outline.toml first.' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
