# mt7-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-25 · cases: 892

## mt7_test_id (190 need a call, 144 need none, 144 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.837 [0.784, 0.889] |
| L1 json | 0.832 [0.779, 0.884] |
| L2 schema | 0.821 [0.768, 0.874] |
| L3 tool | 0.716 [0.653, 0.779] |
| L4 args | 0.637 [0.568, 0.705] |
| abstain | 0.729 [0.653, 0.799] |
| decision | 0.790 [0.746, 0.832] |
| step right | 0.605 [0.551, 0.656] |
| answer grounded | 0.562 [0.479, 0.639] |
| episode right | 0.319 [0.243, 0.396] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 55 | 0.75 |
| empty_then_asked | 12 | 0.00 |
| list_then_stat | 36 | 0.64 |
| missing_then_asked | 12 | 0.25 |
| read_edit_write | 36 | 0.72 |
| read_miss_then_list | 48 | 0.25 |
| read_next_page | 24 | 0.88 |
| search_dead_end | 24 | 0.54 |
| search_then_read_source | 36 | 0.78 |
| size_from_listing | 12 | 0.08 |
| user_corrects | 24 | 0.88 |
| write_then_check | 15 | 0.87 |

Failures (first 12):

- `mt7_test_id-00313` drill_down: fails args  | 'The readme file is a couple of folders down inside archive. Find it and read it.' -> '{"name": "fs_read", "arguments": {"path": "archive/attic/readme.txt", "offset": 1, "limit": 1000}}'
- `mt7_test_id-00318` drill_down: called '{"name": "fs_list", "arguments": {"path": "research/wip"}}' | "Somewhere under research, in a subfolder, there's a invoice file. Open it."
- `mt7_test_id-00323` drill_down: called '{"name": "fs_read", "arguments": {"path": "archive/wip/legacy/notes-2026.txt"}}' | 'One more thing: Dig through archive until you find the notes-2026 file, then show it to me.'
- `mt7_test_id-00325` drill_down: fails tool  | 'I put results in a nested folder under drafts; read it out.' -> '{"name": "fs_read", "arguments": {"path": "drafts/notes-2026.md"}}'
- `mt7_test_id-00326` drill_down: fails tool  | 'I put results in a nested folder under drafts; read it out.' -> '{"name": "fs_read", "arguments": {"path": "drafts/attic/invoice.toml"}}'
- `mt7_test_id-00327` drill_down: fails json no call | 'I put results in a nested folder under drafts; read it out.' -> 'The contents of the "stash" folder under "attic" in the "drafts" folder are two files: "checklist.toml" and "results.md". \n\nWould you like t'
- `mt7_test_id-00330` drill_down: fails json no call | 'Browse into archive and its subfolders to find results, and print what it says. Please check.' -> 'The `archive` directory contains the following entries:\n\n- `attic`: a directory\n- `proposal.py`: a file, 24 bytes in size\n\nWould you like to'
- `mt7_test_id-00337` drill_down: reply lacks the tool's fact | "Go down the folders in drafts until you hit the readme file. What's in it? Much appreciated." -> 'The `readme.md` file in the `wip` directory of `drafts/attic` contains the following information:\n\n- Lunch is scheduled for noon on Friday.\n'
- `mt7_test_id-00340` drill_down: fails args  | 'Okay, next: The proposal file is a couple of folders down inside scripts. Find it and read it.' -> '{"name": "fs_read", "arguments": {"path": "scripts/attic/proposal.txt", "offset": 1, "limit": 100}}'
- `mt7_test_id-00347` drill_down: fails tool  | 'Dig through research until you find the proposal file, then show it to me.' -> '{"name": "crag_search", "arguments": {"query": "proposal file", "k": 5}}'
- `mt7_test_id-00348` drill_down: fails tool  | 'Dig through research until you find the proposal file, then show it to me.' -> '{"name": "fs_read", "arguments": {"path": "research/invoice.py"}}'
- `mt7_test_id-00351` drill_down: fails tool  | 'I put readme in a nested folder under archive; read it out. Cheers.' -> '{"name": "fs_read", "arguments": {"path": "archive/nested_folder/readme"}}'

## mt7_test_ood (318 need a call, 240 need none, 240 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.783 [0.736, 0.827] |
| L1 json | 0.783 [0.736, 0.827] |
| L2 schema | 0.780 [0.733, 0.824] |
| L3 tool | 0.676 [0.623, 0.726] |
| L4 args | 0.560 [0.506, 0.613] |
| abstain | 0.767 [0.713, 0.821] |
| decision | 0.776 [0.740, 0.810] |
| step right | 0.573 [0.532, 0.615] |
| answer grounded | 0.592 [0.529, 0.654] |
| episode right | 0.304 [0.246, 0.362] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 88 | 0.66 |
| empty_then_asked | 20 | 0.05 |
| list_then_stat | 60 | 0.62 |
| missing_then_asked | 20 | 0.50 |
| read_edit_write | 60 | 0.75 |
| read_miss_then_list | 80 | 0.20 |
| read_next_page | 40 | 0.88 |
| search_dead_end | 40 | 0.45 |
| search_then_read_source | 60 | 0.75 |
| size_from_listing | 20 | 0.05 |
| user_corrects | 40 | 0.78 |
| write_then_check | 30 | 0.77 |

Failures (first 12):

- `mt7_test_ood-00369` drill_down: called '{"name": "crag_search", "arguments": {"query": "results", "k": 5}}' | 'results is buried in data/raw somewhere, not at the top. Fetch its contents. Please check.'
- `mt7_test_ood-00372` drill_down: fails args  | 'Walk the tree under scripts, locate agenda, and tell me what the file says.' -> '{"name": "fs_read", "arguments": {"path": "scripts/attic/agenda.md", "offset": 1, "limit": 1000}}'
- `mt7_test_ood-00374` drill_down: fails tool  | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> '{"name": "crag_search", "arguments": {"query": "outline", "k": 5}}'
- `mt7_test_ood-00375` drill_down: fails tool  | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> '{"name": "crag_search", "arguments": {"query": "outline", "k": 5}}'
- `mt7_test_ood-00376` drill_down: fails args  | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> '{"name": "fs_list", "arguments": {"path": "drafts/wip"}}'
- `mt7_test_ood-00380` drill_down: fails tool  | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/notes-2026.txt"}}'
- `mt7_test_ood-00381` drill_down: fails args  | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> '{"name": "fs_list", "arguments": {"path": "data/raw/wip/readme.py"}}'
- `mt7_test_ood-00384` drill_down: fails tool  | 'readme is buried in archive somewhere, not at the top. Fetch its contents.' -> '{"name": "crag_search", "arguments": {"query": "readme file location", "k": 5}}'
- `mt7_test_ood-00389` drill_down: fails tool  | 'Walk the tree under archive, locate invoice, and tell me what the file says. Much appreciated.' -> '{"name": "fs_read", "arguments": {"path": "archive/readme.txt"}}'
- `mt7_test_ood-00394` drill_down: fails tool  | 'Okay, next: checklist is buried in data/raw somewhere, not at the top. Fetch its contents.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/results.md"}}'
- `mt7_test_ood-00398` drill_down: fails tool  | 'Okay, next: Walk the tree under drafts, locate results, and tell me what the file says.' -> '{"name": "fs_read", "arguments": {"path": "drafts/agenda.py"}}'
- `mt7_test_ood-00399` drill_down: fails json no call | 'Okay, next: Walk the tree under drafts, locate results, and tell me what the file says.' -> 'The directory `drafts/stash` contains the following files:\n\n- `proposal.txt`\n- `results.md`\n\nWould you like to read the contents of one of t'
