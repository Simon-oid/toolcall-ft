# hand2-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: 4150f57-dirty · date: 2026-11-10 · cases: 48

## test_hand2 (32 need a call, 16 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.969 [0.906, 1.000] |
| L1 json | 0.969 [0.906, 1.000] |
| L2 schema | 0.938 [0.844, 1.000] |
| L3 tool | 0.938 [0.844, 1.000] |
| L4 args | 0.906 [0.812, 1.000] |
| abstain | 0.750 [0.500, 0.938] |
| decision | 0.896 [0.812, 0.979] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.80 |
| crag_search | 6 | 1.00 |
| crag_stats | 4 | 1.00 |
| fs_list | 5 | 1.00 |
| fs_read | 8 | 0.75 |
| fs_stat | 4 | 0.75 |
| fs_write | 5 | 1.00 |
| no_tool | 6 | 1.00 |
| unsupported | 5 | 0.40 |

Failures (first 12):

- `test_hand2-015` fs_read: fails args  | 'can you read invoices/2025/march.csv to me' -> '{"name": "fs_read", "arguments": {"path": "invoices/2025/march.csv", "offset": 1}}'
- `test_hand2-020` fs_read: fails schema {'path': '/limit', 'keyword': 'minimum', 'message': 'value below minimum'} | 'read exports/summary.txt from line 40 to the end' -> '{"name": "fs_read", "arguments": {"limit": -1, "offset": 40, "path": "exports/summary.txt"}}'
- `test_hand2-025` fs_stat: fails json no call | 'is exports a file or a folder?' -> 'I need the path to determine whether `exports` refers to a file or a folder. Could you please provide the path?'
- `test_hand2-038` unsupported: called '{"name": "fs_stat", "arguments": {"path": "keys.txt"}}' | 'move keys.txt into the trash folder and empty it'
- `test_hand2-040` unsupported: called '{"name": "fs_list", "arguments": {"path": "exports"}}' | 'zip the exports folder'
- `test_hand2-041` unsupported: called '{"name": "crag_search", "arguments": {"query": "AMD stock price today", "k": 5}}' | "what's the stock price of AMD today?"
- `test_hand2-045` ambiguous: called '{"name": "fs_list", "arguments": {"path": "."}}' | 'list it'
