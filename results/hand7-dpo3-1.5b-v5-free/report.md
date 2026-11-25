# hand7-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.917 [0.806, 1.000] |
| L1 json | 0.861 [0.750, 0.972] |
| L2 schema | 0.806 [0.667, 0.917] |
| L3 tool | 0.333 [0.194, 0.500] |
| L4 args | 0.333 [0.194, 0.500] |
| abstain | 0.900 [0.800, 1.000] |
| decision | 0.909 [0.833, 0.970] |
| step right | 0.485 [0.364, 0.606] |
| answer grounded | 0.630 [0.444, 0.815] |
| episode right | 0.333 [0.167, 0.500] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 0.67 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.00 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.33 |
| followup_read_search_hit | 2 | 0.50 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 1.00 |
| list_root_stat_largest | 3 | 0.00 |
| read_log_write_summary | 3 | 0.33 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 0.33 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 0.33 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.67 |
| stats_then_search | 3 | 0.33 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.50 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 0.33 |

Failures (first 12):

- `test_hand7-000` search_then_read_full: fails tool  | 'find documentation about connection pooling and show me the source file' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand7-002` search_then_read_full: reply lacks the tool's fact | 'find documentation about connection pooling and show me the source file' -> 'Here is infra/db-pool.md, the closest chunk to what I found in the docs (infra/db-pool.md):\n\nThe connection pool is capped at 20 connections'
- `test_hand7-005` stat_then_list: called '{"name": "fs_list", "arguments": {"path": "archive"}}' | "check if the archive/ directory exists and what's in it"
- `test_hand7-010` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "crag_search", "arguments": {"query": "services/worker.toml"}}'
- `test_hand7-013` stats_then_search: fails tool  | 'how big is the knowledge base? then look up anything about TLS certificates' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> "Here's what I found in docs/000indexops/ops/tls-rotation.md: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover"
- `test_hand7-015` write_and_readback: fails json  | 'create a file at tmp/health.json containing {"status":"ok","version":"1.4.2"} and then read it back so I can verify' -> '{"name": "fs_write", "arguments": {"path": "tmp/health.json", "content": "{\\"status\\":\\"ok\\",\\"version\\":\\"1.4.2\\""}}}'
- `test_hand7-016` write_and_readback: fails tool  | 'create a file at tmp/health.json containing {"status":"ok","version":"1.4.2"} and then read it back so I can verify' -> '{"name": "fs_stat", "arguments": {"path": "tmp/health.json"}}'
- `test_hand7-019` three_level_drill: fails json  | 'find the error codes table somewhere inside api/' -> '{"name": "crag_search", "arguments": {"query": "error codes table", "k": 5}'
- `test_hand7-020` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "crag_search", "arguments": {"query": "error codes table"}}'
- `test_hand7-022` double_search_refine: fails tool  | 'find the CI pipeline timeout setting' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'From the search results (docs/faq.md): Q: What CI do we use? A: GitHub Actions with self-hosted runners. So it says: GitHub Actions with sel'
