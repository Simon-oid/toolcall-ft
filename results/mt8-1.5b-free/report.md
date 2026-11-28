# mt8-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.466 [0.397, 0.540] |
| L1 json | 0.466 [0.397, 0.540] |
| L2 schema | 0.413 [0.344, 0.481] |
| L3 tool | 0.333 [0.270, 0.402] |
| L4 args | 0.280 [0.217, 0.344] |
| abstain | 0.843 [0.769, 0.907] |
| decision | 0.603 [0.545, 0.657] |
| step right | 0.293 [0.242, 0.343] |
| answer grounded | 0.315 [0.231, 0.398] |
| episode right | 0.074 [0.028, 0.130] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.04 |
| miss_listed_absent | 23 | 0.39 |
| offtopic_no_pointer | 24 | 0.42 |
| read_miss_list | 44 | 0.18 |
| reword_exhausted | 24 | 0.46 |
| search_not_guess | 24 | 0.54 |
| search_pointer | 36 | 0.39 |
| search_reword | 33 | 0.48 |
| subdir_exhausted | 40 | 0.10 |

Failures (first 12):

- `mt8_test_id-00246` read_miss_list: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'Read scripts/agenda.py.' -> '{"name": "fs_read", "arguments": {"limit": null, "offset": null, "path": "scripts/agenda.py"}}'
- `mt8_test_id-00247` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> 'The file `agenda.py` does not exist in the specified directory.'
- `mt8_test_id-00248` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> "I found the following files in the 'scripts' directory:\n\n1. agenda-final.md\n2. invoice.py\n3. outline.toml\n4. proposal.txt\n\nNone of these fil"
- `mt8_test_id-00249` read_miss_list: called '{"name": "fs_read", "arguments": {"path": "scripts/agenda.py"}}' | 'Read scripts/agenda.py.'
- `mt8_test_id-00250` read_miss_list: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | "What's in research/readme.py?" -> '{"name": "fs_read", "arguments": {"path": "research/readme.py", "limit": null, "offset": null}}'
- `mt8_test_id-00251` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'The file `readme.py` does not exist in the specified path. Please check the file path and try again.'
- `mt8_test_id-00252` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'The `readme.py` file does not exist in the directory `research`. The files present in the `research` directory are:\n- `agenda.toml`\n- `notes'
- `mt8_test_id-00255` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> 'The file `checklist.md` does not exist in the specified directory.'
- `mt8_test_id-00256` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> "I found the following files in the 'data/raw' directory:\n\n1. checklist-new.py\n2. notes-2026.txt\n3. readme.txt\n\nNone of these files match 'ch"
- `mt8_test_id-00257` read_miss_list: called '{"name": "fs_read", "arguments": {"path": "data/raw/notes-2026.txt"}}' | 'One more thing: Show me data/raw/checklist.md.'
- `mt8_test_id-00258` read_miss_list: fails args  | 'Open drafts/checklist.md for me. Please check.' -> '{"name": "fs_read", "arguments": {"path": "drafts/checklist.md", "offset": 1, "limit": 10}}'
- `mt8_test_id-00259` read_miss_list: fails json no call | 'Open drafts/checklist.md for me. Please check.' -> "The file `drafts/checklist.md` does not exist in the specified directory. Please check the path or create the file if it's intended to be th"

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.437 [0.383, 0.491] |
| L1 json | 0.437 [0.383, 0.491] |
| L2 schema | 0.413 [0.362, 0.467] |
| L3 tool | 0.347 [0.296, 0.398] |
| L4 args | 0.326 [0.278, 0.377] |
| abstain | 0.867 [0.817, 0.911] |
| decision | 0.588 [0.545, 0.630] |
| step right | 0.344 [0.304, 0.385] |
| answer grounded | 0.378 [0.306, 0.450] |
| episode right | 0.072 [0.039, 0.111] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.15 |
| miss_listed_absent | 49 | 0.41 |
| offtopic_no_pointer | 40 | 0.30 |
| read_miss_list | 76 | 0.29 |
| reword_exhausted | 40 | 0.47 |
| search_not_guess | 40 | 0.42 |
| search_pointer | 60 | 0.50 |
| search_reword | 51 | 0.61 |
| subdir_exhausted | 67 | 0.18 |

Failures (first 12):

- `mt8_test_ood-00291` read_miss_list: fails json no call | 'Poke around scripts for it.' -> 'I found a file named notes-2026_2026.md in the scripts directory. Let me read its contents for you.'
- `mt8_test_ood-00292` read_miss_list: reply lacks the tool's fact | 'Poke around scripts for it.' -> 'I found a file named notes-2026_2026.md in the scripts directory. Let me read its contents for you.'
- `mt8_test_ood-00293` read_miss_list: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'Display archive/checklist.py, please.' -> '{"name": "fs_read", "arguments": {"path": "archive/checklist.py", "limit": null, "offset": null}}'
- `mt8_test_ood-00294` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> 'The file `archive/checklist.py` does not exist in the directory.'
- `mt8_test_ood-00295` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> "I found the following files in the 'archive' directory:\n\n1. checklist.md\n2. invoice.md\n3. results.md\n\nNone of these files match 'checklist.p"
- `mt8_test_ood-00297` read_miss_list: fails tool  | 'Could you pull up scripts/proposal.py?' -> '{"name": "fs_list", "arguments": {"path": "scripts/proposal.py"}}'
- `mt8_test_ood-00298` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> 'The file `scripts/proposal.py` does not exist in the directory.'
- `mt8_test_ood-00299` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> 'I found the following files in the "scripts" directory:\n\n1. checklist.md\n2. outline.py\n3. proposal-final.md\n4. readme.toml\n\nNone of these fi'
- `mt8_test_ood-00301` read_miss_list: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'Display archive/checklist.toml, please.' -> '{"name": "fs_read", "arguments": {"limit": null, "offset": null, "path": "checklist.toml"}}'
- `mt8_test_ood-00302` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'The file `archive/checklist.toml` does not exist in the specified directory.'
- `mt8_test_ood-00303` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'I found the file `checklist_old.py` and `results.txt` in the `archive` directory. If you need to display `checklist_old.py`, you can use the'
- `mt8_test_ood-00304` read_miss_list: reply lacks the tool's fact | 'Display archive/checklist.toml, please.' -> 'I\'m sorry, but I don\'t have any information about a file named "checklist_old.py" in the "archive" directory. Could you please provide more '
