# mt7-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-25 · cases: 892

## mt7_test_id (190 need a call, 144 need none, 144 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.484 [0.416, 0.558] |
| L1 json | 0.484 [0.416, 0.558] |
| L2 schema | 0.468 [0.400, 0.542] |
| L3 tool | 0.337 [0.268, 0.405] |
| L4 args | 0.237 [0.179, 0.300] |
| abstain | 0.757 [0.688, 0.826] |
| decision | 0.602 [0.548, 0.656] |
| step right | 0.314 [0.263, 0.365] |
| answer grounded | 0.417 [0.340, 0.493] |
| episode right | 0.139 [0.083, 0.194] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 55 | 0.33 |
| empty_then_asked | 12 | 0.08 |
| list_then_stat | 36 | 0.08 |
| missing_then_asked | 12 | 0.08 |
| read_edit_write | 36 | 0.22 |
| read_miss_then_list | 48 | 0.23 |
| read_next_page | 24 | 0.62 |
| search_dead_end | 24 | 0.50 |
| search_then_read_source | 36 | 0.19 |
| size_from_listing | 12 | 0.00 |
| user_corrects | 24 | 0.71 |
| write_then_check | 15 | 0.80 |

Failures (first 12):

- `mt7_test_id-00311` drill_down: fails args  | 'The readme file is a couple of folders down inside archive. Find it and read it.' -> '{"name": "fs_list", "arguments": {"path": "archive/README.md"}}'
- `mt7_test_id-00312` drill_down: fails json no call | 'The readme file is a couple of folders down inside archive. Find it and read it.' -> 'The readme file is located in the "attic" folder. Here is the content:\n\n- [cos 0.65  bm25  fusion  attic/README.md] README.md\n  - This is th'
- `mt7_test_id-00315` drill_down: fails json no call | "Somewhere under research, in a subfolder, there's a invoice file. Open it." -> "I don't have direct access to files on your computer or the internet. However, I can help you search for the invoice file using the cRAG ind"
- `mt7_test_id-00316` drill_down: fails json no call | "Somewhere under research, in a subfolder, there's a invoice file. Open it." -> 'The directory "research" contains the following files and subdirectories:\n\n- proposal.py\n- wip\n\nTo find the invoice file, I will search the '
- `mt7_test_id-00317` drill_down: fails json no call | "Somewhere under research, in a subfolder, there's a invoice file. Open it." -> 'The invoice file is located in the subfolder `research/wip/invoice.txt`.'
- `mt7_test_id-00318` drill_down: reply lacks the tool's fact | "Somewhere under research, in a subfolder, there's a invoice file. Open it." -> 'The invoice file is located in the "research/wip" directory. Here is the content:\n\n[cosine 0.65  bm25 0.75  fusion 0.85] research/wip/invoic'
- `mt7_test_id-00319` drill_down: fails json no call | 'One more thing: Dig through archive until you find the notes-2026 file, then show it to me.' -> "I'm sorry, but I don't have direct access to your file system or archives. I can only retrieve information from the documents indexed by the"
- `mt7_test_id-00320` drill_down: fails json no call | 'One more thing: Dig through archive until you find the notes-2026 file, then show it to me.' -> 'I found the file you\'re looking for. It\'s named "notes-2026" and it\'s located in the "archive" directory. Here\'s the content of the file:\n\n*'
- `mt7_test_id-00321` drill_down: fails args  | 'One more thing: Dig through archive until you find the notes-2026 file, then show it to me.' -> '{"name": "fs_list", "arguments": {"path": "archive/legacy"}}'
- `mt7_test_id-00322` drill_down: fails json no call | 'One more thing: Dig through archive until you find the notes-2026 file, then show it to me.' -> 'The notes-2026.txt file has been found in the archive/wip/legacy directory. Here it is:\n\n[cosine 0.65  bm25 0.75  fusion 0.85] archive/wip/l'
- `mt7_test_id-00324` drill_down: fails args  | 'I put results in a nested folder under drafts; read it out.' -> '{"name": "fs_list", "arguments": {"path": "drafts/nested"}}'
- `mt7_test_id-00325` drill_down: fails json no call | 'I put results in a nested folder under drafts; read it out.' -> 'The directory "drafts" contains the following files:\n\n1. "attic" (size: 4096 bytes)\n2. "notes-2026.md" (size: 40 bytes)'

## mt7_test_ood (318 need a call, 240 need none, 240 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.481 [0.428, 0.535] |
| L1 json | 0.481 [0.428, 0.535] |
| L2 schema | 0.450 [0.396, 0.503] |
| L3 tool | 0.299 [0.248, 0.349] |
| L4 args | 0.214 [0.170, 0.258] |
| abstain | 0.708 [0.650, 0.767] |
| decision | 0.579 [0.538, 0.620] |
| step right | 0.306 [0.269, 0.346] |
| answer grounded | 0.429 [0.367, 0.492] |
| episode right | 0.129 [0.087, 0.171] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| drill_down | 88 | 0.26 |
| empty_then_asked | 20 | 0.05 |
| list_then_stat | 60 | 0.18 |
| missing_then_asked | 20 | 0.10 |
| read_edit_write | 60 | 0.20 |
| read_miss_then_list | 80 | 0.11 |
| read_next_page | 40 | 0.65 |
| search_dead_end | 40 | 0.57 |
| search_then_read_source | 60 | 0.25 |
| size_from_listing | 20 | 0.00 |
| user_corrects | 40 | 0.75 |
| write_then_check | 30 | 0.63 |

Failures (first 12):

- `mt7_test_ood-00367` drill_down: fails json no call | 'results is buried in data/raw somewhere, not at the top. Fetch its contents. Please check.' -> 'The directory `data/raw` contains the following files:\n\n- `checklist.py` (18 bytes)\n- `wip` (4096 bytes)'
- `mt7_test_ood-00368` drill_down: fails json no call | 'results is buried in data/raw somewhere, not at the top. Fetch its contents. Please check.' -> 'The contents of the directory `data/raw/wip` are as follows:\n\n- `agenda.py` (42 lines)\n- `results.toml` (38 lines)'
- `mt7_test_ood-00369` drill_down: reply lacks the tool's fact | 'results is buried in data/raw somewhere, not at the top. Fetch its contents. Please check.' -> 'The results are located in the directory `data/raw/wip`. Here are the contents:\n\n- `checklist.py` (18 bytes)\n- `agenda.py` (42 bytes)\n- `res'
- `mt7_test_ood-00371` drill_down: fails json no call | 'Walk the tree under scripts, locate agenda, and tell me what the file says.' -> 'The directory `scripts` contains the following files:\n- `attic`\n- `readme.txt`\n\nThe `readme.txt` file says: "agenda".'
- `mt7_test_ood-00372` drill_down: fails json no call | 'Walk the tree under scripts, locate agenda, and tell me what the file says.' -> 'The file `agenda.md` in the `scripts/attic` directory contains the following text:\n\n[cosine 0.65  bm25 0.75  fusion 0.85] scripts/attic/agen'
- `mt7_test_ood-00374` drill_down: fails tool  | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> '{"name": "crag_search", "arguments": {"query": "outline is buried in drafts somewhere, not at the top", "k": 10}}'
- `mt7_test_ood-00375` drill_down: fails json no call | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> 'I found the following files and directories in the "drafts" directory:\n\n1. `readme.py`\n2. A directory named `stash`\n\nCould you please specif'
- `mt7_test_ood-00377` drill_down: fails json no call | 'outline is buried in drafts somewhere, not at the top. Fetch its contents. Please check.' -> 'The outline is buried in drafts, not at the top. Here are the contents:\n\n1. **notes-2026.txt**\n2. **agenda.py**\n3. **outline.toml**'
- `mt7_test_ood-00379` drill_down: fails args  | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> '{"name": "fs_list", "arguments": {"path": "data/raw/agenda"}}'
- `mt7_test_ood-00380` drill_down: fails json no call | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> 'The directory `data/raw` contains the following files:\n\n- `notes-2026.txt` with size 24 bytes.'
- `mt7_test_ood-00381` drill_down: fails json no call | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> 'The directory `data/raw/wip` contains the following files:\n- `notes-2026.txt`\n- `wip/legacy`\n\nThe file `data/raw/wip/legacy` contains the fo'
- `mt7_test_ood-00382` drill_down: fails json no call | 'Hey there. Walk the tree under data/raw, locate agenda, and tell me what the file says.' -> 'The file `agenda.txt` under the directory `data/raw/wip/legacy` contains the following text:\n\n[cosine 0.65  bm25 0.75  fusion 0.85] agenda.t'
