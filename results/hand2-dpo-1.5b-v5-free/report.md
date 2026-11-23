# hand2-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.906 [0.781, 1.000] |
| L1 json | 0.906 [0.781, 1.000] |
| L2 schema | 0.906 [0.781, 1.000] |
| L3 tool | 0.906 [0.781, 1.000] |
| L4 args | 0.875 [0.750, 0.969] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.938 [0.854, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 0.75 |
| fs_list | 5 | 1.00 |
| fs_read | 8 | 0.88 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 0.80 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand2-009` crag_stats: fails json no call | 'Which embedding dimension is the retrieval index using?' -> "I can't check the index right now because I don't have a tool to look in it. The tools I do have let me search and inspect the document inde"
- `test_hand2-017` fs_read: fails args  | 'what does the first line of exports/summary.txt say?' -> '{"name": "fs_read", "arguments": {"path": "exports/summary.txt"}}'
- `test_hand2-025` fs_stat: fails json no call | 'is exports a file or a folder?' -> "_exports is not a file or a folder. It's an empty directory."
- `test_hand2-031` fs_write: fails json no call | 'new file exports/status.txt, text: ok' -> 'I can do that once I know more. What should the contents of status.txt be?'
