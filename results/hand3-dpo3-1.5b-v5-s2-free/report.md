# hand3-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.412 [0.265, 0.588] |
| L1 json | 0.412 [0.265, 0.588] |
| L2 schema | 0.412 [0.265, 0.588] |
| L3 tool | 0.412 [0.265, 0.588] |
| L4 args | 0.412 [0.265, 0.588] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.583 [0.438, 0.729] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 0.62 |
| crag_stats | 3 | 0.67 |
| fs_list | 8 | 0.75 |
| fs_read | 7 | 0.14 |
| fs_stat | 4 | 0.00 |
| fs_write | 4 | 0.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand3-003` fs_list: fails json no call | "show me what's in taxes" -> 'Which folder should I look in? taxes.'
- `test_hand3-004` fs_list: fails json no call | 'contents of the receipts folder pls' -> 'Which subfolder should I list the contents of? receipts.'
- `test_hand3-009` fs_read: fails json no call | 'read thesis/abstract.md, just the first 12 lines' -> 'Which file should I read those lines from? thesis/abstract.md.'
- `test_hand3-010` fs_read: fails json no call | 'show line 4 of todo/today.md' -> 'Which file should I read those lines from? todo/today.md.'
- `test_hand3-011` fs_read: fails json no call | 'cat recipes/carbonara.md' -> 'I can do that once I know more. What should the file be called?'
- `test_hand3-012` fs_read: fails json no call | 'open taxes/2025.csv from line 20' -> 'Which file should I read from? taxes/2025.csv. Which lines should I read them at? Line 20.'
- `test_hand3-013` fs_read: fails json no call | 'lines 5 to 9 of backups/log.txt please' -> 'Which file should I read those lines from?'
- `test_hand3-014` fs_read: fails json no call | 'print homework/essay.txt' -> 'I can do that once I know more. What should I write in homework/essay.txt?'
- `test_hand3-020` crag_search: fails json no call | 'pls search for the threat model' -> 'What should I look up: the threat model?'
- `test_hand3-021` crag_search: fails json no call | "i'd like the passages on reciprocal rank fusion, cheers. just two" -> 'Which folder should I search in?'
- `test_hand3-022` crag_search: fails json no call | 'can u check the docs re symlink escapes' -> 'I can do that once I know more. What should I look up: `docs` or `symlink escapes`?'
- `test_hand3-024` crag_stats: fails json no call | 'is the document index empty or not' -> 'I can do that once I know more. What should I look up?'
