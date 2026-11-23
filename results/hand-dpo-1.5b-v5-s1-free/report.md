# hand-dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.897 [0.795, 0.974] |
| L1 json | 0.897 [0.795, 0.974] |
| L2 schema | 0.897 [0.795, 0.974] |
| L3 tool | 0.897 [0.795, 0.974] |
| L4 args | 0.795 [0.667, 0.923] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.926 [0.852, 0.981] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.50 |
| crag_stats | 4 | 0.75 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.90 |
| fs_stat | 5 | 0.80 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-000` crag_search: fails json no call | "hey, I'm debugging a flaky test — can you check what the docs say about the handler timeout watchdog?" -> 'Sure, but I need one detail first. What should I look up specifically?'
- `test_hand-005` crag_search: fails args  | 'search: json schema subset supported keywords' -> '{"name": "crag_search", "arguments": {"query": "supported keywords"}}'
- `test_hand-006` crag_search: fails json no call | 'Can u look up how the elicitation handler works' -> 'Sure, but I need one detail first. Which file should I read?'
- `test_hand-007` crag_search: fails args  | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> '{"name": "crag_search", "arguments": {"query": "the replay fixtures are captured"}}'
- `test_hand-009` crag_stats: fails json no call | 'how many documents did we index, roughly?' -> 'I can do that once I know more. Which tool should I use to check the index size?'
- `test_hand-012` fs_list: fails args  | 'what files do I have in the sandbox?' -> '{"name": "fs_list", "arguments": {"path": "sandbox"}}'
- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path": "README"}}'
- `test_hand-029` fs_stat: fails json no call | 'when did I last touch recipes/pasta.md?' -> 'I can do that once I know more. Which file should I check the modification time for?'
