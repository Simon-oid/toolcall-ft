# hand3-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.853 [0.735, 0.971] |
| L3 tool | 0.382 [0.235, 0.559] |
| L4 args | 0.382 [0.235, 0.559] |
| abstain | 0.857 [0.643, 1.000] |
| decision | 0.958 [0.896, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 0.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 0.38 |
| fs_read | 7 | 0.29 |
| fs_stat | 4 | 0.75 |
| fs_write | 4 | 0.50 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.60 |

Failures (first 12):

- `test_hand3-000` fs_list: fails tool  | 'what does photos contain' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand3-004` fs_list: fails schema  | 'contents of the receipts folder pls' -> '{"name": "receipts", "arguments": {}}'
- `test_hand3-005` fs_list: fails schema  | "open projects and tell me what's there" -> '{"name": "projects", "arguments": {}}'
- `test_hand3-006` fs_list: fails schema  | 'ls thesis/chapters' -> '{"name": "thesis/chapters", "arguments": {}}'
- `test_hand3-007` fs_list: fails tool  | 'which files does homework have?' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand3-008` fs_read: fails tool  | "what's in photos/captions.txt?" -> '{"name": "fs_stat", "arguments": {"path": "photos/captions.txt"}}'
- `test_hand3-009` fs_read: fails tool  | 'read thesis/abstract.md, just the first 12 lines' -> '{"name": "fs_stat", "arguments": {"path": "thesis/abstract.md"}}'
- `test_hand3-012` fs_read: fails tool  | 'open taxes/2025.csv from line 20' -> '{"name": "fs_stat", "arguments": {"path": "taxes/2025.csv"}}'
- `test_hand3-013` fs_read: fails tool  | 'lines 5 to 9 of backups/log.txt please' -> '{"name": "fs_stat", "arguments": {"path": "backups/log.txt"}}'
- `test_hand3-014` fs_read: fails tool  | 'print homework/essay.txt' -> '{"name": "fs_stat", "arguments": {"path": "homework/essay.txt"}}'
- `test_hand3-015` crag_search: fails tool  | 'search the docs for the token bucket, please. only the best match' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand3-016` crag_search: fails tool  | 'look up fuzzing in the documentation, thanks. top 3 only' -> '{"name": "crag_stats", "arguments": {}}'
