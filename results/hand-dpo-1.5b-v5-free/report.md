# hand-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.897 [0.795, 0.974] |
| L1 json | 0.897 [0.795, 0.974] |
| L2 schema | 0.897 [0.795, 0.974] |
| L3 tool | 0.872 [0.769, 0.974] |
| L4 args | 0.821 [0.692, 0.923] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.926 [0.852, 0.981] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.75 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.90 |
| fs_stat | 5 | 0.60 |
| fs_write | 6 | 0.83 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-001` crag_search: fails json no call | "what's the deal with Streamable HTTP in cMCP? look it up" -> 'I can do that once I know more. What should I look up specifically about Streamable HTTP in cMCP?'
- `test_hand-004` crag_search: fails json no call | 'Does the documentation mention anything about valgrind?' -> 'I can search the docs to check. What should I look up?'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path": "README"}}'
- `test_hand-029` fs_stat: fails json no call | 'when did I last touch recipes/pasta.md?' -> "I can't search the document index: my tools can only list, read, stat or write files in the sandbox."
- `test_hand-030` fs_stat: fails tool  | 'is photos/2026 a directory?' -> '{"name": "fs_list", "arguments": {"path": "photos/2026"}}'
- `test_hand-037` fs_write: fails json no call | 'overwrite reminders.txt so it contains just the word: done' -> 'I can do that once I know more. What should I write in reminders.txt?'
