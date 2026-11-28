# mt8-ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.995 [0.984, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.997 [0.990, 1.000] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.991 [0.972, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.98 |
| miss_listed_absent | 23 | 1.00 |
| offtopic_no_pointer | 24 | 1.00 |
| read_miss_list | 44 | 1.00 |
| reword_exhausted | 24 | 1.00 |
| search_not_guess | 24 | 1.00 |
| search_pointer | 36 | 1.00 |
| search_reword | 33 | 1.00 |
| subdir_exhausted | 40 | 1.00 |

Failures (first 12):

- `mt8_test_id-00904` list_into_subdir: fails args  | 'Get me results out of research.' -> '{"name": "fs_read", "arguments": {"path": "research/results.md"}}'

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.994 [0.985, 1.000] |
| L1 json | 0.994 [0.985, 1.000] |
| L2 schema | 0.994 [0.985, 1.000] |
| L3 tool | 0.973 [0.955, 0.988] |
| L4 args | 0.958 [0.934, 0.979] |
| abstain | 0.989 [0.972, 1.000] |
| decision | 0.992 [0.984, 0.998] |
| step right | 0.959 [0.942, 0.975] |
| answer grounded | 0.961 [0.933, 0.989] |
| episode right | 0.889 [0.839, 0.933] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.96 |
| miss_listed_absent | 49 | 0.98 |
| offtopic_no_pointer | 40 | 0.95 |
| read_miss_list | 76 | 1.00 |
| reword_exhausted | 40 | 0.97 |
| search_not_guess | 40 | 0.95 |
| search_pointer | 60 | 0.95 |
| search_reword | 51 | 0.96 |
| subdir_exhausted | 67 | 0.91 |

Failures (first 12):

- `mt8_test_ood-00535` miss_listed_absent: reply lacks the tool's fact | 'Could you pull up scripts/results.py?' -> 'No results under scripts: it only contains invoice.py.'
- `mt8_test_ood-00949` list_into_subdir: fails tool  | 'Can you find results in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `mt8_test_ood-00951` list_into_subdir: fails tool  | 'Can you find results in research and show it?' -> '{"name": "fs_list", "arguments": {"path": "research/wip/results"}}'
- `mt8_test_ood-00958` list_into_subdir: fails tool  | 'Can you find agenda in research and show it? Please check.' -> '{"name": "crag_search", "arguments": {"query": "agenda"}}'
- `mt8_test_ood-00977` list_into_subdir: fails tool  | 'Can you find invoice in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "invoice"}}'
- `mt8_test_ood-01307` subdir_exhausted: reply lacks the tool's fact | "Fetch the results file that's in scripts." -> 'No results for scripts or in scripts/legacy.'
- `mt8_test_ood-01314` subdir_exhausted: reply lacks the tool's fact | "Fetch the results file that's in archive." -> 'No results for archive or in archive/legacy.'
- `mt8_test_ood-01325` subdir_exhausted: reply lacks the tool's fact | 'Hey there. Display research/results.txt, please.' -> 'No results for research or in research/attic: the folder is empty.'
- `mt8_test_ood-01327` subdir_exhausted: fails args  | "Okay, next: Fetch the proposal file that's in drafts." -> '{"name": "fs_list", "arguments": {"path": "attic"}}'
- `mt8_test_ood-01329` subdir_exhausted: fails tool  | 'Can you find checklist in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt8_test_ood-01369` subdir_exhausted: fails tool  | 'One more thing: Can you find agenda in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "agenda"}}'
- `mt8_test_ood-01604` search_reword: fails json no call | 'Check the knowledge base on machine-readable results, a.k.a. structured tool output.' -> 'I searched the docs for machine-readable results, but nothing matched.'
