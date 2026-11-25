# hand7-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.806 [0.667, 0.917] |
| L1 json | 0.806 [0.667, 0.917] |
| L2 schema | 0.694 [0.556, 0.833] |
| L3 tool | 0.611 [0.444, 0.778] |
| L4 args | 0.528 [0.361, 0.694] |
| abstain | 0.967 [0.900, 1.000] |
| decision | 0.879 [0.788, 0.955] |
| step right | 0.621 [0.500, 0.727] |
| answer grounded | 0.704 [0.519, 0.852] |
| episode right | 0.467 [0.300, 0.633] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 0.67 |
| count_from_listing | 1 | 1.00 |
| double_search_refine | 3 | 0.00 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.33 |
| followup_read_search_hit | 2 | 0.50 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.67 |
| list_root_stat_largest | 3 | 0.67 |
| read_log_write_summary | 3 | 0.67 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.00 |
| search_then_read_full | 3 | 0.33 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 1.00 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.50 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-001` search_then_read_full: fails schema  | 'find documentation about connection pooling and show me the source file' -> '{"name": "crag_read", "arguments": {"path": "infra/db-pool.md"}}'
- `test_hand7-002` search_then_read_full: reply lacks the tool's fact | 'find documentation about connection pooling and show me the source file' -> 'Here is infra/db-pool.md: The connection pool is capped at 20 connections with a 30-second idle timeout.'
- `test_hand7-007` list_miss_then_search: fails args  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "crag_search", "arguments": {"query": "the onboarding checklist", "k": 1}}'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "crag_search", "arguments": {"query": "the retry delay in services/worker.toml is 500ms"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'From the index (db: data/knowledge.db): \n\nTLS certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal'
- `test_hand7-019` three_level_drill: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find the error codes table somewhere inside api/' -> '{"name": "crag_search", "arguments": {"query": "the error codes table", "path": "api"}}'
- `test_hand7-020` three_level_drill: fails json no call | 'find the error codes table somewhere inside api/' -> 'The file error-codes.md is in api/v2.'
- `test_hand7-022` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> '<tool_call>\n{"name": "crag_search", "arguments": {"query": "the CI pipeline timeout setting"}}'
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'According to docs/faq.md: GitHub Actions with self-hosted runners.'
- `test_hand7-024` double_search_refine: reply lacks the tool's fact | 'find the CI pipeline timeout setting' -> 'According to docs/faq.md (line 2): GitHub Actions with self-hosted runners.'
- `test_hand7-025` compare_envs: fails tool  | 'compare the Python version in envs/dev.yaml and envs/prod.yaml' -> '{"name": "crag_search", "arguments": {"query": "the Python version", "k": 1}}'
- `test_hand7-028` read_log_write_summary: fails args  | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> '{"name": "fs_read", "arguments": {"path": "logs/deploy.log", "limit": 10}}'
