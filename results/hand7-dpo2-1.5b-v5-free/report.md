# hand7-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.972 [0.917, 1.000] |
| L1 json | 0.944 [0.861, 1.000] |
| L2 schema | 0.944 [0.861, 1.000] |
| L3 tool | 0.750 [0.611, 0.889] |
| L4 args | 0.667 [0.500, 0.806] |
| abstain | 0.533 [0.367, 0.700] |
| decision | 0.773 [0.667, 0.864] |
| step right | 0.561 [0.439, 0.682] |
| answer grounded | 0.444 [0.259, 0.630] |
| episode right | 0.233 [0.100, 0.400] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 0.00 |
| answer_in_history | 1 | 0.00 |
| compare_envs | 3 | 0.67 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.33 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.67 |
| followup_read_search_hit | 2 | 1.00 |
| general_knowledge | 1 | 0.00 |
| list_miss_then_search | 3 | 0.67 |
| list_root_stat_largest | 3 | 0.67 |
| read_log_write_summary | 3 | 0.33 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 0.00 |
| resolve_ordinal_first | 2 | 0.50 |
| resolve_pronoun_it | 1 | 0.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 0.67 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.33 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.75 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-002` search_then_read_full: called '{"name": "fs_write", "arguments": {"path": "infra/db-pool.md", "content": "Max connections: 20\\nIdle timeout: 30s\\nMin i' | 'find documentation about connection pooling and show me the source file'
- `test_hand7-003` stat_then_list: fails tool  | "check if the archive/ directory exists and what's in it" -> '{"name": "fs_list", "arguments": {"path": "archive/"}}'
- `test_hand7-005` stat_then_list: called '{"name": "fs_write", "arguments": {"path": "archive/backup.txt", "content": "dump-2026-09.sql.gz\\ndump-2026-10.sql.gz\\nl' | "check if the archive/ directory exists and what's in it"
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/leave-policy.md"}}'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "fs_write", "arguments": {"path": "services/worker.toml", "content": "retry_delay = 2000ms"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'Ops/TLS rotation: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-019` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_read", "arguments": {"path": "api/error_codes_table.md"}}'
- `test_hand7-023` double_search_refine: fails tool  | 'find the CI pipeline timeout setting' -> '{"name": "fs_write", "arguments": {"path": "ci/pipeline_timeout_setting.txt", "content": "GitHub Actions with self-hosted runners."}}'
- `test_hand7-024` double_search_refine: reply lacks the tool's fact | 'find the CI pipeline timeout setting' -> 'docs/faq.md says: GitHub Actions with self-hosted runners.'
- `test_hand7-027` compare_envs: called '{"name": "tools\\/crag_search", "arguments": {"query": "the Python version in envs/dev.yaml and envs/prod.yaml"}}' | 'compare the Python version in envs/dev.yaml and envs/prod.yaml'
- `test_hand7-028` read_log_write_summary: fails args  | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> '{"name": "fs_read", "arguments": {"path": "logs/deploy.log", "offset": 1, "limit": 11}}'
- `test_hand7-029` read_log_write_summary: fails json  | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> '{"name": "fs_write", "arguments": {"path": "logs/deploy-summary.txt", "content": "deploying tag v3.8.1\\npulling image registry.internal/app:'
