# mt7-ft-1.5b-v8-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 892

## mt7_test_id (190 need a call, 144 need none, 144 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.995 [0.984, 1.000] |
| L4 args | 0.953 [0.921, 0.979] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.964 [0.943, 0.982] |
| answer grounded | 0.979 [0.951, 1.000] |
| episode right | 0.917 [0.868, 0.958] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 55 | 1.00 |
| empty_then_asked | 12 | 1.00 |
| list_then_stat | 36 | 0.78 |
| missing_then_asked | 12 | 1.00 |
| read_edit_write | 36 | 0.97 |
| read_miss_then_list | 48 | 1.00 |
| read_next_page | 24 | 1.00 |
| search_dead_end | 24 | 1.00 |
| search_then_read_source | 36 | 1.00 |
| size_from_listing | 12 | 0.83 |
| user_corrects | 24 | 0.96 |
| write_then_check | 15 | 1.00 |

Failures (first 12):

- `mt7_test_id-01648` size_from_listing: reply lacks the tool's fact | 'And readme.toml, how many bytes?' -> 'readme.toml is 35 bytes.'
- `mt7_test_id-01651` size_from_listing: reply lacks the tool's fact | 'What does readme.py weigh in bytes?' -> "It's 40 bytes, according to the listing."
- `mt7_test_id-01920` read_edit_write: reply lacks the tool's fact | 'One more thing: Insert verbosity = quiet into data/raw/checklist.env.' -> 'Updated checklist: verbosity is now quiet.'
- `mt7_test_id-02198` list_then_stat: fails args  | 'Find the smallest file in research and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "research/outline.md"}}'
- `mt7_test_id-02201` list_then_stat: fails args  | "What's the modification date of the smallest file in research?" -> '{"name": "fs_stat", "arguments": {"path": "research/agenda.toml"}}'
- `mt7_test_id-02204` list_then_stat: fails args  | 'In data/raw, which file is the smallest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "data/raw/outline.py"}}'
- `mt7_test_id-02207` list_then_stat: fails args  | 'Check drafts: when did its smallest file last change?' -> '{"name": "fs_stat", "arguments": {"path": "drafts/checklist.py"}}'
- `mt7_test_id-02216` list_then_stat: fails args  | 'Find the smallest file in drafts and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "drafts/readme.md"}}'
- `mt7_test_id-02219` list_then_stat: fails args  | "What's the modification date of the largest file in archive?" -> '{"name": "fs_stat", "arguments": {"path": "archive/notes-2026.py"}}'
- `mt7_test_id-02222` list_then_stat: fails args  | 'In archive, which file is the biggest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "archive/notes-2026.py"}}'
- `mt7_test_id-02228` list_then_stat: fails args  | 'Look in research and get me the last-modified date of the biggest file.' -> '{"name": "fs_stat", "arguments": {"path": "research/propose.md"}}'
- `mt7_test_id-02644` user_corrects: fails tool  | 'Hmm, no. Try scripts instead.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'

## mt7_test_ood (318 need a call, 240 need none, 240 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.959 [0.937, 0.978] |
| L1 json | 0.959 [0.937, 0.978] |
| L2 schema | 0.959 [0.937, 0.978] |
| L3 tool | 0.918 [0.887, 0.947] |
| L4 args | 0.874 [0.836, 0.909] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.977 [0.964, 0.987] |
| step right | 0.923 [0.900, 0.944] |
| answer grounded | 0.988 [0.971, 1.000] |
| episode right | 0.825 [0.775, 0.871] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 88 | 1.00 |
| empty_then_asked | 20 | 0.95 |
| list_then_stat | 60 | 0.78 |
| missing_then_asked | 20 | 1.00 |
| read_edit_write | 60 | 0.88 |
| read_miss_then_list | 80 | 0.85 |
| read_next_page | 40 | 1.00 |
| search_dead_end | 40 | 1.00 |
| search_then_read_source | 60 | 0.92 |
| size_from_listing | 20 | 1.00 |
| user_corrects | 40 | 0.97 |
| write_then_check | 30 | 0.87 |

Failures (first 12):

- `mt7_test_ood-00706` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in. Please check.' -> 'I can do that once I know more. What should I look up?'
- `mt7_test_ood-00721` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full.' -> 'I can do that once I know more. Which topic should I search the docs for?'
- `mt7_test_ood-00730` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in.' -> 'I can do that once I know more. Which tool should I use?'
- `mt7_test_ood-00733` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full. Cheers.' -> 'I can do that once I know more. What should I look up?'
- `mt7_test_ood-00757` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full. Much appreciated.' -> 'I can do that once I know more. What should I look up?'
- `mt7_test_ood-01092` read_miss_then_list: fails tool  | 'Get me the invoice file from data/raw; try data/raw/invoice.py first.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt7_test_ood-01096` read_miss_then_list: fails tool  | 'Pull up research/proposal.py (could be a different extension, I forget).' -> '{"name": "fs_list", "arguments": {"path": "research"}}'
- `mt7_test_ood-01100` read_miss_then_list: fails tool  | 'Hey there. Get me the results file from drafts; try drafts/results.txt first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt7_test_ood-01108` read_miss_then_list: fails tool  | 'Get me the invoice file from data/raw; try data/raw/invoice.toml first.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt7_test_ood-01116` read_miss_then_list: fails tool  | 'Hey there. Get me the outline file from drafts; try drafts/outline.py first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
- `mt7_test_ood-01124` read_miss_then_list: fails tool  | 'Hey there. Get me the proposal file from scripts; try scripts/proposal.md first.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'
- `mt7_test_ood-01132` read_miss_then_list: fails tool  | 'Get me the results file from drafts; try drafts/results.toml first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
