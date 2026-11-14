# hand-gptoss120b-low-api

model: openai/gpt-oss-120b · gguf: gpt-oss-120b · decoding: hosted API, native tool calling, temperature 0 · llama.cpp: hosted API https://api.groq.com/openai/v1, reasoning_effort low · commit: v0.1.0-2-gbece5fc · date: 2026-11-14 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 0.949 [0.872, 1.000] |
| abstain | 0.867 [0.667, 1.000] |
| decision | 0.963 [0.907, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 0.80 |
| crag_search | 8 | 0.88 |
| crag_stats | 4 | 1.00 |
| fs_list | 6 | 1.00 |
| fs_read | 10 | 0.90 |
| fs_stat | 5 | 1.00 |
| fs_write | 6 | 1.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 0.80 |

Failures (first 12):

- `test_hand-005` crag_search: fails args  | 'search: json schema subset supported keywords' -> '{"name": "crag_search", "arguments": {"k":10,"query":"json schema subset supported keywords"}}'
- `test_hand-025` fs_read: fails args  | 'skim the first 3 lines of README' -> '{"name": "fs_read", "arguments": {"path":"README"}}'
- `test_hand-046` unsupported: called '{"name": "fs_read", "arguments": {"path":"shopping.md"}}' | 'rename shopping.md to groceries.md'
- `test_hand-051` ambiguous: called '{"name": "fs_list", "arguments": {"path":""}}' | "what's in the folder?"
