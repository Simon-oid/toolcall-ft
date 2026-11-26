# mt7-ft-1.5b-v7-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-26 · cases: 892

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
| step right | 0.970 [0.952, 0.985] |
| answer grounded | 0.993 [0.979, 1.000] |
| episode right | 0.931 [0.889, 0.965] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 55 | 1.00 |
| empty_then_asked | 12 | 1.00 |
| list_then_stat | 36 | 0.81 |
| missing_then_asked | 12 | 1.00 |
| read_edit_write | 36 | 1.00 |
| read_miss_then_list | 48 | 1.00 |
| read_next_page | 24 | 1.00 |
| search_dead_end | 24 | 1.00 |
| search_then_read_source | 36 | 1.00 |
| size_from_listing | 12 | 0.92 |
| user_corrects | 24 | 0.92 |
| write_then_check | 15 | 1.00 |

Failures (first 12):

- `mt7_test_id-01648` size_from_listing: reply lacks the tool's fact | 'And readme.toml, how many bytes?' -> 'The listing says readme.toml is 37 bytes.'
- `mt7_test_id-02195` list_then_stat: fails args  | 'When was the biggest file in scripts last modified?' -> '{"name": "fs_stat", "arguments": {"path": "scripts/results.txt"}}'
- `mt7_test_id-02198` list_then_stat: fails args  | 'Find the smallest file in research and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "research/outline.md"}}'
- `mt7_test_id-02201` list_then_stat: fails args  | "What's the modification date of the smallest file in research?" -> '{"name": "fs_stat", "arguments": {"path": "research/README.md"}}'
- `mt7_test_id-02204` list_then_stat: fails args  | 'In data/raw, which file is the smallest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "data/raw/outline.py"}}'
- `mt7_test_id-02216` list_then_stat: fails args  | 'Find the smallest file in drafts and tell me when it last changed.' -> '{"name": "fs_stat", "arguments": {"path": "drafts/readme.md"}}'
- `mt7_test_id-02222` list_then_stat: fails args  | 'In archive, which file is the biggest, and when was it last touched?' -> '{"name": "fs_stat", "arguments": {"path": "archive/notes-2026.py"}}'
- `mt7_test_id-02228` list_then_stat: fails args  | 'Look in research and get me the last-modified date of the biggest file.' -> '{"name": "fs_stat", "arguments": {"path": "research/propose.md"}}'
- `mt7_test_id-02638` user_corrects: fails args  | 'Not that one, the copy under research.' -> '{"name": "fs_read", "arguments": {"path": "research/archive/notes-2026.toml"}}'
- `mt7_test_id-02644` user_corrects: fails tool  | 'Hmm, no. Try scripts instead.' -> '{"name": "fs_list", "arguments": {"path": "scripts"}}'

## mt7_test_ood (318 need a call, 240 need none, 240 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.972 [0.953, 0.987] |
| L1 json | 0.972 [0.953, 0.987] |
| L2 schema | 0.972 [0.953, 0.987] |
| L3 tool | 0.918 [0.887, 0.947] |
| L4 args | 0.874 [0.836, 0.909] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.984 [0.973, 0.993] |
| step right | 0.919 [0.896, 0.941] |
| answer grounded | 0.979 [0.958, 0.996] |
| episode right | 0.812 [0.762, 0.863] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 88 | 0.94 |
| empty_then_asked | 20 | 0.80 |
| list_then_stat | 60 | 0.78 |
| missing_then_asked | 20 | 1.00 |
| read_edit_write | 60 | 0.95 |
| read_miss_then_list | 80 | 0.88 |
| read_next_page | 40 | 1.00 |
| search_dead_end | 40 | 1.00 |
| search_then_read_source | 60 | 0.92 |
| size_from_listing | 20 | 1.00 |
| user_corrects | 40 | 0.95 |
| write_then_check | 30 | 0.90 |

Failures (first 12):

- `mt7_test_ood-00394` drill_down: fails tool  | 'Okay, next: checklist is buried in data/raw somewhere, not at the top. Fetch its contents.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/legacy/checklist.txt"}}'
- `mt7_test_ood-00419` drill_down: fails tool  | 'proposal is buried in research somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "research proposal"}}'
- `mt7_test_ood-00436` drill_down: fails tool  | 'Hey there. proposal is buried in drafts somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "drafts proposal"}}'
- `mt7_test_ood-00442` drill_down: fails tool  | 'Walk the tree under scripts, locate readme, and tell me what the file says.' -> '{"name": "fs_read", "arguments": {"path": "scripts/wip/outline.toml"}}'
- `mt7_test_ood-00445` drill_down: fails tool  | 'Okay, next: invoice is buried in research somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "invoice"}}'
- `mt7_test_ood-00706` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in. Please check.' -> 'I can do that once I know more. Which folder should I look in?'
- `mt7_test_ood-00721` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full.' -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt7_test_ood-00730` search_then_read_source: fails json no call | 'Track down structured tool output in the knowledge base and pull up the original file it lives in.' -> 'Sure, but I need one detail first. What should I look up?'
- `mt7_test_ood-00733` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full. Cheers.' -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt7_test_ood-00757` search_then_read_source: fails json no call | 'Run a doc search on structured tool output; whichever file ranks first, read it to me in full. Much appreciated.' -> 'Sure, but I need one detail first. Which folder should I look in?'
- `mt7_test_ood-01092` read_miss_then_list: fails tool  | 'Get me the invoice file from data/raw; try data/raw/invoice.py first.' -> '{"name": "fs_list", "arguments": {"path": "data/raw"}}'
- `mt7_test_ood-01100` read_miss_then_list: fails tool  | 'Hey there. Get me the results file from drafts; try drafts/results.txt first.' -> '{"name": "fs_list", "arguments": {"path": "drafts"}}'
