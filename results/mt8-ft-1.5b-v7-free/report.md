# mt8-ft-1.5b-v7-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.730 [0.667, 0.794] |
| L1 json | 0.730 [0.667, 0.794] |
| L2 schema | 0.725 [0.661, 0.788] |
| L3 tool | 0.646 [0.577, 0.709] |
| L4 args | 0.619 [0.550, 0.688] |
| abstain | 0.806 [0.731, 0.880] |
| decision | 0.758 [0.707, 0.805] |
| step right | 0.633 [0.579, 0.687] |
| answer grounded | 0.657 [0.565, 0.741] |
| episode right | 0.213 [0.139, 0.296] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.80 |
| miss_listed_absent | 23 | 0.35 |
| offtopic_no_pointer | 24 | 0.58 |
| read_miss_list | 44 | 0.73 |
| reword_exhausted | 24 | 0.75 |
| search_not_guess | 24 | 0.54 |
| search_pointer | 36 | 0.64 |
| search_reword | 33 | 0.64 |
| subdir_exhausted | 40 | 0.50 |

Failures (first 12):

- `mt8_test_id-00247` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> 'There is no file at scripts/agenda.py: it does not exist.'
- `mt8_test_id-00251` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'There is no file at research/readme.py: it does not exist.'
- `mt8_test_id-00255` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> 'There is no file at data/raw/checklist.md: it does not exist.'
- `mt8_test_id-00259` read_miss_list: fails json no call | 'Open drafts/checklist.md for me. Please check.' -> 'I checked, and drafts/checklist.md does not exist.'
- `mt8_test_id-00263` read_miss_list: fails json no call | 'Print drafts/proposal.toml.' -> 'There is no file at drafts/proposal.toml: it does not exist.'
- `mt8_test_id-00266` read_miss_list: fails json no call | 'It must be there under another name.' -> 'I checked, and archive/results.py does not exist.'
- `mt8_test_id-00267` read_miss_list: fails json no call | 'It must be there under another name.' -> 'The file is actually archive/results-new.txt:\n\nnotes-2026.py: 19 lines\noutline.py: 38 lines\nproposal.toml: 37 lines\nresults-new.txt: 19 line'
- `mt8_test_id-00270` read_miss_list: fails json no call | 'Read archive/outline.toml.' -> 'There is no file at archive/outline.toml: it does not exist.'
- `mt8_test_id-00280` read_miss_list: fails json no call | 'Open data/raw/outline.md for me. Cheers.' -> 'There is no file at data/raw/outline.md: it does not exist.'
- `mt8_test_id-00284` read_miss_list: fails json no call | 'Print archive/checklist.md.' -> 'There is no file at archive/checklist.md: it does not exist.'
- `mt8_test_id-00287` read_miss_list: fails json no call | 'It must be there under another name.' -> "I can't find drafts/results.md, so I can't do that."
- `mt8_test_id-00288` read_miss_list: fails json no call | 'It must be there under another name.' -> 'I found this file: drafts/results_old.toml.'

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.695 [0.644, 0.743] |
| L1 json | 0.695 [0.644, 0.743] |
| L2 schema | 0.689 [0.638, 0.740] |
| L3 tool | 0.620 [0.569, 0.671] |
| L4 args | 0.605 [0.551, 0.659] |
| abstain | 0.761 [0.700, 0.822] |
| decision | 0.718 [0.679, 0.755] |
| step right | 0.628 [0.588, 0.669] |
| answer grounded | 0.672 [0.606, 0.739] |
| episode right | 0.167 [0.117, 0.222] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.77 |
| miss_listed_absent | 49 | 0.31 |
| offtopic_no_pointer | 40 | 0.62 |
| read_miss_list | 76 | 0.75 |
| reword_exhausted | 40 | 0.75 |
| search_not_guess | 40 | 0.50 |
| search_pointer | 60 | 0.65 |
| search_reword | 51 | 0.63 |
| subdir_exhausted | 67 | 0.52 |

Failures (first 12):

- `mt8_test_ood-00290` read_miss_list: fails json no call | 'Poke around scripts for it.' -> "scripts/notes-2026.txt doesn't exist, as the last check showed."
- `mt8_test_ood-00294` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> 'There is no file at archive/checklist.py: it does not exist.'
- `mt8_test_ood-00298` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> 'There is no file at scripts/proposal.py: it does not exist.'
- `mt8_test_ood-00302` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'There is no file at archive/checklist.toml: it does not exist.'
- `mt8_test_ood-00306` read_miss_list: fails json no call | 'Could you pull up archive/readme.md?' -> 'There is no file at archive/readme.md: it does not exist.'
- `mt8_test_ood-00313` read_miss_list: fails json no call | 'Okay, next: Could you pull up research/outline.txt?' -> 'There is no file at research/outline.txt: it does not exist.'
- `mt8_test_ood-00317` read_miss_list: fails json no call | 'Display drafts/notes-2026.py, please.' -> 'There is no file at drafts/notes-2026.py: it does not exist.'
- `mt8_test_ood-00321` read_miss_list: fails json no call | 'Could you pull up research/agenda.toml?' -> 'There is no file at research/agenda.toml: it does not exist.'
- `mt8_test_ood-00322` read_miss_list: fails args  | 'Could you pull up research/agenda.toml?' -> '{"name": "fs_read", "arguments": {"path": "research/invoice.toml"}}'
- `mt8_test_ood-00325` read_miss_list: fails json no call | 'Display archive/outline.py, please.' -> 'There is no file at archive/outline.py: it does not exist.'
- `mt8_test_ood-00329` read_miss_list: fails json no call | 'Could you pull up archive/outline.txt?' -> 'There is no file at archive/outline.txt: it does not exist.'
- `mt8_test_ood-00333` read_miss_list: fails json no call | 'Okay, next: Display research/results.toml, please.' -> 'There is no file at research/results.toml: it does not exist.'
