# mt8-ft-1.5b-v8-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 811

## mt8_test_id (189 need a call, 108 need none, 108 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.989 [0.974, 1.000] |
| L1 json | 0.989 [0.974, 1.000] |
| L2 schema | 0.984 [0.963, 1.000] |
| L3 tool | 0.979 [0.958, 0.995] |
| L4 args | 0.979 [0.958, 0.995] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.993 [0.983, 1.000] |
| step right | 0.983 [0.966, 0.997] |
| answer grounded | 0.991 [0.972, 1.000] |
| episode right | 0.954 [0.907, 0.991] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 49 | 0.96 |
| miss_listed_absent | 23 | 1.00 |
| offtopic_no_pointer | 24 | 1.00 |
| read_miss_list | 44 | 1.00 |
| reword_exhausted | 24 | 1.00 |
| search_not_guess | 24 | 0.96 |
| search_pointer | 36 | 0.97 |
| search_reword | 33 | 0.97 |
| subdir_exhausted | 40 | 1.00 |

Failures (first 12):

- `mt8_test_id-00904` list_into_subdir: fails json no call | 'Get me results out of research.' -> 'No research file in the folder, just legacy: checklist.md, results.md.'
- `mt8_test_id-00928` list_into_subdir: fails tool  | 'Hey there. Get me results out of data/raw.' -> '{"name": "fs_list", "arguments": {"path": "data/raw/stash/results.py"}}'
- `mt8_test_id-01576` search_reword: reply lacks the tool's fact | 'Maybe the docs call it the HNSW index.' -> "The index is not implemented: HNSW isn't listed."
- `mt8_test_id-02066` search_pointer: fails schema  | 'Anything in the index about machine-readable results?' -> '{"name": "structured_tool_output", "arguments": {}}'
- `mt8_test_id-02484` search_not_guess: fails json no call | 'What do we do about the SSRF egress guard? Much appreciated.' -> "I can't find a tool to solve this: the request is about the SSRF egress guard, not about the document index or the sandbox file tree."

## mt8_test_ood (334 need a call, 180 need none, 180 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.994 [0.985, 1.000] |
| L1 json | 0.994 [0.985, 1.000] |
| L2 schema | 0.994 [0.985, 1.000] |
| L3 tool | 0.991 [0.979, 1.000] |
| L4 args | 0.988 [0.976, 0.997] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.996 [0.990, 1.000] |
| step right | 0.984 [0.973, 0.994] |
| answer grounded | 0.978 [0.956, 0.994] |
| episode right | 0.956 [0.922, 0.983] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| list_into_subdir | 91 | 0.99 |
| miss_listed_absent | 49 | 1.00 |
| offtopic_no_pointer | 40 | 1.00 |
| read_miss_list | 76 | 1.00 |
| reword_exhausted | 40 | 1.00 |
| search_not_guess | 40 | 0.95 |
| search_pointer | 60 | 1.00 |
| search_reword | 51 | 0.92 |
| subdir_exhausted | 67 | 0.99 |

Failures (first 12):

- `mt8_test_ood-00951` list_into_subdir: fails tool  | 'Can you find results in research and show it?' -> '{"name": "fs_list", "arguments": {"path": "research/wip/results"}}'
- `mt8_test_ood-01325` subdir_exhausted: reply lacks the tool's fact | 'Hey there. Display research/results.txt, please.' -> 'No results under research or in research/attic: the file is a directory, not a plain text file.'
- `mt8_test_ood-01604` search_reword: fails json no call | 'Check the knowledge base on machine-readable results, a.k.a. structured tool output.' -> 'I searched the docs for machine-readable results, but nothing matched.'
- `mt8_test_ood-01618` search_reword: fails args  | 'Dig up the ranking score on SciFact in the docs. The documentation may say nDCG evaluation.' -> '{"name": "crag_search", "arguments": {"query": "the ranking score"}}'
- `mt8_test_ood-01623` search_reword: reply lacks the tool's fact | 'Check the knowledge base on the approximate neighbour search, a.k.a. the HNSW index.' -> 'The index has nothing on the approximate neighbour search, only passages on the HNSW index and log redaction.'
- `mt8_test_ood-01634` search_reword: reply lacks the tool's fact | 'Check the knowledge base on the approximate neighbour search, a.k.a. the HNSW index. Please check.' -> 'The index has no matching chunks for the approximate neighbour search, only passages on the HNSW index and subscriptions, log redaction.'
- `mt8_test_ood-02504` search_not_guess: fails json no call | "What's our approach to structured tool output? Much appreciated." -> "We aim to provide clear, concise, and accurate information in the responses we generate. When a tool can't answer a question directly, we'll"
- `mt8_test_ood-02523` search_not_guess: reply lacks the tool's fact | 'Hey there. Explain the HNSW index as this codebase does it.' -> 'The search found nothing about the HNSW index, only passages on the cancellation requests system and subscriptions.'
