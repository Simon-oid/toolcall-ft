# hand4-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 40

## test_hand4 (20 need a call, 20 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 0.750 [0.550, 0.950] |
| L3 tool | 0.350 [0.150, 0.550] |
| L4 args | 0.350 [0.150, 0.550] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 16 | 1.00 |
| crag_search | 5 | 0.00 |
| crag_stats | 2 | 1.00 |
| fs_list | 5 | 0.20 |
| fs_read | 3 | 0.67 |
| fs_stat | 2 | 1.00 |
| fs_write | 3 | 0.00 |
| no_tool | 2 | 1.00 |
| unsupported | 2 | 1.00 |

Failures (first 12):

- `test_hand4-016` fs_list: fails tool  | "what's in invoices" -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-017` fs_list: fails schema  | 'anything inside downloads?' -> '{"name": "downloads", "arguments": {}}'
- `test_hand4-018` fs_list: fails schema  | 'list music/jazz' -> '{"name": "music/jazz", "arguments": {}}'
- `test_hand4-019` fs_list: fails schema  | "peek at drafts, what's there" -> '{"name": "drafts", "arguments": {}}'
- `test_hand4-021` crag_search: fails tool  | 'search the docs for backpressure, please. just one' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-022` crag_search: fails tool  | 'find the passages about mmap. top 2' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-023` crag_search: fails tool  | 'what do the docs say on vector quantization? three results' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-024` crag_search: fails tool  | 'look for rate limiting in the index' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-025` crag_search: fails tool  | 'anything about BM25 saturation? give me 4' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand4-026` fs_write: fails schema  | "write 'buy milk' to lists/groceries.txt" -> '{"name": "fs_prompt", "arguments": {"message": "What should the file be called?"}}'
- `test_hand4-027` fs_write: fails schema  | "put 'meeting moved to 3pm' in work/notes.md" -> '{"name": "fs_prompt", "arguments": {"prompt": "What should the file be called?"}}'
- `test_hand4-028` fs_write: fails tool  | "save the line 'v4 ready' into logs/status.txt" -> '{"name": "fs_stat", "arguments": {"path": "logs/status.txt"}}'
