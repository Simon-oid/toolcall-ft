# mt8-ft-1.5b-v8-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.974 [0.947, 0.995] |
| L4 args | 0.968 [0.942, 0.989] |
| abstain | 0.991 [0.972, 1.000] |
| decision | 0.990 [0.976, 1.000] |
| step right | 0.973 [0.953, 0.990] |
| answer grounded | 0.981 [0.954, 1.000] |
| episode right | 0.935 [0.889, 0.981] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.94 |
| miss_listed_absent | 23 | 1.00 |
| offtopic_no_pointer | 24 | 0.96 |
| read_miss_list | 44 | 0.98 |
| reword_exhausted | 24 | 1.00 |
| search_not_guess | 24 | 0.96 |
| search_pointer | 36 | 0.94 |
| search_reword | 33 | 1.00 |
| subdir_exhausted | 40 | 1.00 |

Failures (first 12):

- `mt8_test_id-00260` read_miss_list: fails args  | 'Open drafts/checklist.md for me. Please check.' -> '{"name": "fs_read", "arguments": {"path": "drafts/checklist_old.md"}}'
- `mt8_test_id-00902` list_into_subdir: fails tool  | 'Get me results out of research.' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `mt8_test_id-00904` list_into_subdir: fails json no call | 'Get me results out of research.' -> 'No research files, only folders.'
- `mt8_test_id-00928` list_into_subdir: fails json no call | 'Hey there. Get me results out of data/raw.' -> 'No results for data/raw, and in data/raw/stash too: no file matches.'
- `mt8_test_id-02064` search_pointer: reply lacks the tool's fact | 'Find the passage on the approximate neighbour search.' -> 'The HNSW index is not implemented: the search found docs/hnsw-index.md.'
- `mt8_test_id-02066` search_pointer: fails schema  | 'Anything in the index about machine-readable results?' -> '{"name": "structured_search", "arguments": {"query": "machine-readable results"}}'
- `mt8_test_id-02287` offtopic_no_pointer: called '{"name": "crag_search", "arguments": {"query": "structuredContent"}}' | 'What do the docs say about the salary spreadsheet?'
- `mt8_test_id-02494` search_not_guess: fails tool  | 'Remind me how subscriptions is set up.' -> '{"name": "fs_list", "arguments": {"path": "subscriptions"}}'

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.994 [0.985, 1.000] |
| L1 json | 0.994 [0.985, 1.000] |
| L2 schema | 0.994 [0.985, 1.000] |
| L3 tool | 0.979 [0.961, 0.994] |
| L4 args | 0.970 [0.949, 0.988] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.996 [0.990, 1.000] |
| step right | 0.969 [0.953, 0.982] |
| answer grounded | 0.967 [0.939, 0.989] |
| episode right | 0.917 [0.872, 0.956] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.96 |
| miss_listed_absent | 49 | 0.98 |
| offtopic_no_pointer | 40 | 1.00 |
| read_miss_list | 76 | 1.00 |
| reword_exhausted | 40 | 0.97 |
| search_not_guess | 40 | 0.97 |
| search_pointer | 60 | 0.97 |
| search_reword | 51 | 0.92 |
| subdir_exhausted | 67 | 0.96 |

Failures (first 12):

- `mt8_test_ood-00535` miss_listed_absent: reply lacks the tool's fact | 'Could you pull up scripts/results.py?' -> 'No results for scripts or in scripts: only invoice.py.'
- `mt8_test_ood-00949` list_into_subdir: fails tool  | 'Can you find results in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "research"}}'
- `mt8_test_ood-00951` list_into_subdir: fails json no call | 'Can you find results in research and show it?' -> 'No research-specific files, and no wip folder either.'
- `mt8_test_ood-00958` list_into_subdir: fails tool  | 'Can you find agenda in research and show it? Please check.' -> '{"name": "crag_search", "arguments": {"query": "agenda"}}'
- `mt8_test_ood-00977` list_into_subdir: fails tool  | 'Can you find invoice in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "invoice"}}'
- `mt8_test_ood-01325` subdir_exhausted: reply lacks the tool's fact | 'Hey there. Display research/results.txt, please.' -> "No research results file here, and attic doesn't have one either."
- `mt8_test_ood-01329` subdir_exhausted: fails tool  | 'Can you find checklist in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "checklist"}}'
- `mt8_test_ood-01369` subdir_exhausted: fails tool  | 'One more thing: Can you find agenda in research and show it?' -> '{"name": "crag_search", "arguments": {"query": "agenda"}}'
- `mt8_test_ood-01604` search_reword: fails json no call | 'Check the knowledge base on machine-readable results, a.k.a. structured tool output.' -> 'I searched the docs for machine-readable results, but nothing matched.'
- `mt8_test_ood-01618` search_reword: fails args  | 'Dig up the ranking score on SciFact in the docs. The documentation may say nDCG evaluation.' -> '{"name": "crag_search", "arguments": {"query": "the ranking score"}}'
- `mt8_test_ood-01623` search_reword: reply lacks the tool's fact | 'Check the knowledge base on the approximate neighbour search, a.k.a. the HNSW index.' -> 'The index has nothing on the HNSW index, only passages on the approximate neighbour search and log redaction.'
- `mt8_test_ood-01634` search_reword: reply lacks the tool's fact | 'Check the knowledge base on the approximate neighbour search, a.k.a. the HNSW index. Please check.' -> 'The index has nothing on the HNSW algorithm: only passages on the exact scan and subscriptions.'
