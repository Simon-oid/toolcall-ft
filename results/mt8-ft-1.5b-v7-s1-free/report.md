# mt8-ft-1.5b-v7-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.746 [0.683, 0.810] |
| L1 json | 0.746 [0.683, 0.810] |
| L2 schema | 0.746 [0.683, 0.810] |
| L3 tool | 0.693 [0.624, 0.757] |
| L4 args | 0.661 [0.593, 0.725] |
| abstain | 0.657 [0.565, 0.741] |
| decision | 0.714 [0.663, 0.764] |
| step right | 0.636 [0.582, 0.690] |
| answer grounded | 0.593 [0.500, 0.685] |
| episode right | 0.213 [0.139, 0.296] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.94 |
| miss_listed_absent | 23 | 0.52 |
| offtopic_no_pointer | 24 | 0.50 |
| read_miss_list | 44 | 0.68 |
| reword_exhausted | 24 | 0.79 |
| search_not_guess | 24 | 0.46 |
| search_pointer | 36 | 0.50 |
| search_reword | 33 | 0.61 |
| subdir_exhausted | 40 | 0.53 |

Failures (first 12):

- `mt8_test_id-00247` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> "scripts/agenda.py doesn't exist."
- `mt8_test_id-00248` read_miss_list: fails args  | 'Read scripts/agenda.py.' -> '{"name": "fs_read", "arguments": {"path": "scripts/outline.toml"}}'
- `mt8_test_id-00251` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'There is no file at research/readme.py: it does not exist.'
- `mt8_test_id-00255` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> 'There is no file at data/raw/checklist.md: it does not exist.'
- `mt8_test_id-00259` read_miss_list: fails json no call | 'Open drafts/checklist.md for me. Please check.' -> 'I checked, and drafts/checklist.md does not exist.'
- `mt8_test_id-00260` read_miss_list: fails args  | 'Open drafts/checklist.md for me. Please check.' -> '{"name": "fs_read", "arguments": {"path": "drafts/checklist_old.md"}}'
- `mt8_test_id-00263` read_miss_list: fails json no call | 'Print drafts/proposal.toml.' -> 'There is no file at drafts/proposal.toml: it does not exist.'
- `mt8_test_id-00264` read_miss_list: fails args  | 'Print drafts/proposal.toml.' -> '{"name": "fs_read", "arguments": {"path": "drafts/results.toml"}}'
- `mt8_test_id-00266` read_miss_list: fails json no call | 'It must be there under another name.' -> "archive/results.py doesn't exist, as the last check showed."
- `mt8_test_id-00270` read_miss_list: fails json no call | 'Read archive/outline.toml.' -> 'There is no file at archive/outline.toml: it does not exist.'
- `mt8_test_id-00274` read_miss_list: fails json no call | "Check what's in archive then." -> 'archive contains these files:\n\n- checklist.py, 24 bytes\n- notes-2026.md, 20 bytes\n- proposal.toml, 24 bytes\n- readme.txt, 16 bytes'
- `mt8_test_id-00280` read_miss_list: fails json no call | 'Open data/raw/outline.md for me. Cheers.' -> 'There is no file at data/raw/outline.md: it exists at data/raw/outline.md.'

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.734 [0.686, 0.781] |
| L1 json | 0.734 [0.686, 0.781] |
| L2 schema | 0.731 [0.683, 0.778] |
| L3 tool | 0.629 [0.578, 0.680] |
| L4 args | 0.617 [0.566, 0.668] |
| abstain | 0.667 [0.600, 0.733] |
| decision | 0.710 [0.669, 0.749] |
| step right | 0.617 [0.574, 0.658] |
| answer grounded | 0.617 [0.544, 0.689] |
| episode right | 0.139 [0.089, 0.189] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.78 |
| miss_listed_absent | 49 | 0.41 |
| offtopic_no_pointer | 40 | 0.55 |
| read_miss_list | 76 | 0.78 |
| reword_exhausted | 40 | 0.62 |
| search_not_guess | 40 | 0.47 |
| search_pointer | 60 | 0.62 |
| search_reword | 51 | 0.59 |
| subdir_exhausted | 67 | 0.51 |

Failures (first 12):

- `mt8_test_ood-00294` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> 'There is no file at archive/checklist.py: it does not exist.'
- `mt8_test_ood-00298` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> "scripts/proposal.py doesn't exist."
- `mt8_test_ood-00302` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'There is no file at archive/checklist.toml: it does not exist.'
- `mt8_test_ood-00306` read_miss_list: fails json no call | 'Could you pull up archive/readme.md?' -> 'There is no file at archive/readme.md: it does not exist.'
- `mt8_test_ood-00313` read_miss_list: fails json no call | 'Okay, next: Could you pull up research/outline.txt?' -> 'There is no file at research/outline.txt: it does not exist.'
- `mt8_test_ood-00317` read_miss_list: fails json no call | 'Display drafts/notes-2026.py, please.' -> 'There is no file at drafts/notes-2026.py: it might be drafts/notes-2026.'
- `mt8_test_ood-00321` read_miss_list: fails json no call | 'Could you pull up research/agenda.toml?' -> 'There is no file at research/agenda.toml: it does not exist.'
- `mt8_test_ood-00325` read_miss_list: fails json no call | 'Display archive/outline.py, please.' -> 'There is no file at archive/outline.py: it does not exist.'
- `mt8_test_ood-00329` read_miss_list: fails json no call | 'Could you pull up archive/outline.txt?' -> 'There is no file at archive/outline.txt: it does not exist.'
- `mt8_test_ood-00333` read_miss_list: fails json no call | 'Okay, next: Display research/results.toml, please.' -> 'There is no file at research/results.toml: it does not exist.'
- `mt8_test_ood-00337` read_miss_list: fails json no call | 'Could you pull up scripts/agenda.toml? Cheers.' -> "scripts/agenda.toml doesn't exist."
- `mt8_test_ood-00341` read_miss_list: fails json no call | 'Display archive/invoice.md, please.' -> 'There is no file at archive/invoice.md: it does not exist.'
