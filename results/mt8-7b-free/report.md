# mt8-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.545 [0.476, 0.614] |
| L1 json | 0.545 [0.476, 0.614] |
| L2 schema | 0.545 [0.476, 0.614] |
| L3 tool | 0.407 [0.339, 0.476] |
| L4 args | 0.386 [0.317, 0.455] |
| abstain | 0.907 [0.852, 0.954] |
| decision | 0.677 [0.623, 0.727] |
| step right | 0.441 [0.384, 0.498] |
| answer grounded | 0.537 [0.444, 0.630] |
| episode right | 0.130 [0.074, 0.194] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.35 |
| miss_listed_absent | 23 | 0.57 |
| offtopic_no_pointer | 24 | 0.54 |
| read_miss_list | 44 | 0.41 |
| reword_exhausted | 24 | 0.58 |
| search_not_guess | 24 | 0.50 |
| search_pointer | 36 | 0.50 |
| search_reword | 33 | 0.64 |
| subdir_exhausted | 40 | 0.12 |

Failures (first 12):

- `mt8_test_id-00247` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> 'The file `scripts/agenda.py` does not exist in the sandboxed file tree. Please check the file path and try again.'
- `mt8_test_id-00248` read_miss_list: fails json no call | 'Read scripts/agenda.py.' -> 'It seems there is no `agenda.py` file in the `scripts` directory. The available files are `agenda-final.md`, `invoice.py`, `outline.toml`, a'
- `mt8_test_id-00249` read_miss_list: reply lacks the tool's fact | 'Read scripts/agenda.py.' -> 'It seems there might be a misunderstanding. The file `agenda-final.md` does not appear to contain Python script. If you are looking for `age'
- `mt8_test_id-00250` read_miss_list: fails tool  | "What's in research/readme.py?" -> '{"name": "fs_stat", "arguments": {"path": "research/readme.py"}}'
- `mt8_test_id-00251` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'It seems there is no file named `readme.py` in the `research` directory. Could you please double-check the filename or provide more context?'
- `mt8_test_id-00252` read_miss_list: fails json no call | "What's in research/readme.py?" -> 'It seems there is no `readme.py` file in the `research` directory. The files listed there are `agenda.toml`, `notes-2026.md`, `readme_v2.txt'
- `mt8_test_id-00253` read_miss_list: reply lacks the tool's fact | "What's in research/readme.py?" -> "It seems there isn't a `readme.py` file in the `research` directory. The files listed there are `agenda.toml`, `notes-2026.md`, `readme_v2.t"
- `mt8_test_id-00255` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> 'It seems that the file `data/raw/checklist.md` does not exist in the sandboxed file tree. Could you please verify the path or provide the co'
- `mt8_test_id-00256` read_miss_list: fails json no call | 'One more thing: Show me data/raw/checklist.md.' -> 'It seems that the file `checklist.md` does not exist in the `data/raw` directory. The files present are `checklist-new.py`, `notes-2026.txt`'
- `mt8_test_id-00259` read_miss_list: fails json no call | 'Open drafts/checklist.md for me. Please check.' -> 'The file `drafts/checklist.md` does not exist. Would you like to create it or would you like to write to a different file?'
- `mt8_test_id-00260` read_miss_list: fails json no call | 'Open drafts/checklist.md for me. Please check.' -> 'It seems there is no file named `checklist.md` in the `drafts` directory. The available files are `agenda.py`, `checklist_old.py`, `outline.'
- `mt8_test_id-00261` read_miss_list: reply lacks the tool's fact | 'Open drafts/checklist.md for me. Please check.' -> 'It seems there is no file named `checklist.md` in the `drafts` directory. The available files are `agenda.py`, `checklist_old.py`, `outline.'

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.476 [0.422, 0.530] |
| L1 json | 0.476 [0.422, 0.530] |
| L2 schema | 0.476 [0.422, 0.530] |
| L3 tool | 0.431 [0.377, 0.485] |
| L4 args | 0.416 [0.365, 0.470] |
| abstain | 0.933 [0.894, 0.967] |
| decision | 0.636 [0.595, 0.677] |
| step right | 0.502 [0.459, 0.545] |
| answer grounded | 0.661 [0.589, 0.728] |
| episode right | 0.161 [0.111, 0.217] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.41 |
| miss_listed_absent | 49 | 0.65 |
| offtopic_no_pointer | 40 | 0.68 |
| read_miss_list | 76 | 0.53 |
| reword_exhausted | 40 | 0.55 |
| search_not_guess | 40 | 0.45 |
| search_pointer | 60 | 0.53 |
| search_reword | 51 | 0.75 |
| subdir_exhausted | 67 | 0.18 |

Failures (first 12):

- `mt8_test_ood-00291` read_miss_list: fails json no call | 'Poke around scripts for it.' -> 'The directory scripts contains the following files:\n\n- agenda.toml\n- notes-2026_2026.md\n- readme.txt\n- results.py\n\nNone of these files match'
- `mt8_test_ood-00294` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> 'It seems that the file `checklist.py` in the `archive` directory does not exist. Could you please provide more details or verify the path?'
- `mt8_test_ood-00295` read_miss_list: fails json no call | 'Display archive/checklist.py, please.' -> 'It seems there is no `checklist.py` file in the `archive` directory. The files listed are `checklist.md`, `invoice.md`, and `results.md`. \n\n'
- `mt8_test_ood-00298` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> 'It seems that the file `scripts/proposal.py` does not exist in the sandboxed file tree. Could you please verify the path or provide more det'
- `mt8_test_ood-00299` read_miss_list: fails json no call | 'Could you pull up scripts/proposal.py?' -> 'It seems there is no `proposal.py` file in the `scripts` directory. The files listed are `checklist.md`, `outline.py`, `proposal-final.md`, '
- `mt8_test_ood-00302` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'It seems the file `archive/checklist.toml` does not exist in the sandboxed file tree. Could you please verify the path or provide more detai'
- `mt8_test_ood-00303` read_miss_list: fails json no call | 'Display archive/checklist.toml, please.' -> 'I see that there is no `checklist.toml` file in the `archive` directory. The files present are `checklist_old.py` and `results.txt`. Could y'
- `mt8_test_ood-00306` read_miss_list: fails json no call | 'Could you pull up archive/readme.md?' -> 'It seems there is no file named `readme.md` in the `archive` directory. Could you please provide more details or check the file path?'
- `mt8_test_ood-00307` read_miss_list: fails json no call | 'Could you pull up archive/readme.md?' -> 'It seems there is no `readme.md` file in the `archive` directory. The files listed are `agenda.md`, `outline.txt`, `readme-new.toml`, and `r'
- `mt8_test_ood-00310` read_miss_list: fails json no call | 'Go and see what scripts actually has.' -> 'The scripts directory contains two files: proposal.txt and readme.toml. There is no readme.py in this directory.'
- `mt8_test_ood-00313` read_miss_list: fails json no call | 'Okay, next: Could you pull up research/outline.txt?' -> 'It seems that the file `research/outline.txt` does not exist in the current directory. Would you like to try another file, or perhaps create'
- `mt8_test_ood-00314` read_miss_list: fails json no call | 'Okay, next: Could you pull up research/outline.txt?' -> 'It seems there is no `outline.txt` file in the `research` directory. The files listed are `checklist.txt`, `outline.toml`, `proposal.txt`, a'
