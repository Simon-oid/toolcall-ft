# hand4-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.500 [0.300, 0.700] |
| L1 json | 0.500 [0.300, 0.700] |
| L2 schema | 0.500 [0.300, 0.700] |
| L3 tool | 0.500 [0.300, 0.700] |
| L4 args | 0.500 [0.300, 0.700] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.750 [0.600, 0.875] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 1.00 |
| crag_search | 5 | 0.40 |
| crag_stats | 2 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 3 | 0.33 |
| fs_stat | 2 | 0.00 |
| fs_write | 3 | 0.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand4-023` crag_search: fails json no call | 'what do the docs say on vector quantization? three results' -> 'Which folder should I search in? (Type the path, or press enter to search the current folder.)'
- `test_hand4-024` crag_search: fails json no call | 'look for rate limiting in the index' -> 'Which folder should I search in? (I can do that once I know more.)'
- `test_hand4-025` crag_search: fails json no call | 'anything about BM25 saturation? give me 4' -> 'I can do that once I know more. What should I look up: the Wikipedia page on BM25 saturation, or something else?'
- `test_hand4-026` fs_write: fails json no call | "write 'buy milk' to lists/groceries.txt" -> 'Happy to help. What should I write in lists/groceries.txt?'
- `test_hand4-027` fs_write: fails json no call | "put 'meeting moved to 3pm' in work/notes.md" -> 'Happy to help. What should the file be called?'
- `test_hand4-028` fs_write: fails json no call | "save the line 'v4 ready' into logs/status.txt" -> 'Happy to help. What should I write in logs/status.txt?'
- `test_hand4-029` fs_read: fails json no call | 'cat config/settings.toml' -> 'I can do that once I know more. What should the file be called?'
- `test_hand4-030` fs_read: fails json no call | 'first 5 lines of logs/app.log' -> 'Which file should I read those lines from? logs/app.log.'
- `test_hand4-032` fs_stat: fails json no call | 'how big is music/track01.mp3' -> 'I can do that once I know more. What should I look up?'
- `test_hand4-033` fs_stat: fails json no call | 'when was invoices/march.pdf last modified?' -> 'I can do that once I know more. Which folder should I look in?'
