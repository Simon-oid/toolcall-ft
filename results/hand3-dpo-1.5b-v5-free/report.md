# hand3-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 48

## test_hand3 (34 need a call, 14 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.912 [0.794, 1.000] |
| L1 json | 0.912 [0.794, 1.000] |
| L2 schema | 0.912 [0.794, 1.000] |
| L3 tool | 0.912 [0.794, 1.000] |
| L4 args | 0.912 [0.794, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.938 [0.854, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 4 | 1.00 |
| crag_search | 8 | 1.00 |
| crag_stats | 3 | 1.00 |
| fs_list | 8 | 1.00 |
| fs_read | 7 | 1.00 |
| fs_stat | 4 | 0.50 |
| fs_write | 4 | 0.75 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand3-026` fs_stat: fails json no call | 'when did i last change thesis/abstract.md?' -> "I can't search the document index: my tools can only list, read, stat or write files in the sandbox."
- `test_hand3-028` fs_stat: fails json no call | 'is backups a folder or a file?' -> "It's not clear from the information provided whether backups is a folder or a file. I can search the document index to find out more, though"
- `test_hand3-031` fs_write: fails json no call | "save 'chapter 3 done' as thesis/progress.txt" -> 'I can do that once I know more. What should the file be called?'
