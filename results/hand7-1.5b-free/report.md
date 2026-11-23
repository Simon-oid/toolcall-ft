# hand7-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.583 [0.417, 0.750] |
| L1 json | 0.583 [0.417, 0.750] |
| L2 schema | 0.500 [0.333, 0.667] |
| L3 tool | 0.389 [0.222, 0.556] |
| L4 args | 0.278 [0.139, 0.417] |
| abstain | 0.867 [0.733, 0.967] |
| decision | 0.712 [0.606, 0.818] |
| step right | 0.409 [0.288, 0.530] |
| answer grounded | 0.556 [0.370, 0.741] |
| episode right | 0.233 [0.100, 0.400] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 0.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 0.33 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.33 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.33 |
| followup_read_search_hit | 2 | 0.50 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.33 |
| list_root_stat_largest | 3 | 0.33 |
| read_log_write_summary | 3 | 0.33 |
| read_patch_write | 3 | 0.33 |
| read_then_write_sibling | 3 | 0.67 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 0.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 0.00 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.33 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.25 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 0.67 |

Failures (first 12):

- `test_hand7-000` search_then_read_full: fails tool  | 'find documentation about connection pooling and show me the source file' -> '{"name": "fs_list", "arguments": {"path": "docs"}}'
- `test_hand7-001` search_then_read_full: fails json no call | 'find documentation about connection pooling and show me the source file' -> 'The documentation about connection pooling is available at `infra/db-pool.md`. It states that the connection pool is capped at 20 connection'
- `test_hand7-002` search_then_read_full: reply lacks the tool's fact | 'find documentation about connection pooling and show me the source file' -> 'The source file for the documentation about connection pooling is `infra/db-pool.md`. It states that the connection pool is capped at 20 con'
- `test_hand7-003` stat_then_list: fails tool  | "check if the archive/ directory exists and what's in it" -> '{"name": "fs_list", "arguments": {"path": "archive/"}}'
- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'The `archive/` directory exists and it is a directory with the following properties:\n- Size: 0 bytes\n- Last modified: October 30, 2026, 4:00'
- `test_hand7-007` list_miss_then_search: fails json no call | 'I need the onboarding checklist, it should be in hr/' -> 'The onboarding checklist is available in the following files:\n\n1. leave-policy.md\n2. expense-form.md\n\nThese files are located in the hr dire'
- `test_hand7-008` list_miss_then_search: reply lacks the tool's fact | 'I need the onboarding checklist, it should be in hr/' -> 'The onboarding checklist is available in the wiki/new-hire.md file.'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "crag_search", "arguments": {"query": "change retry delay in services/worker.toml to 2000ms"}}'
- `test_hand7-010` read_patch_write: fails json no call | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> 'The current configuration of the `worker.toml` file is as follows:\n\n```toml\n[worker]\nretry_delay_ms = 500\nmax_attempts = 5\nbatch_size = 32\n`'
- `test_hand7-013` stats_then_search: fails json no call | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The knowledge base is stored in the database file `data/knowledge.db`. It contains 2860 chunks of text. There are 74 files in the database. '
- `test_hand7-016` write_and_readback: fails args  | 'create a file at tmp/health.json containing {"status":"ok","version":"1.4.2"} and then read it back so I can verify' -> '{"name": "fs_read", "arguments": {"limit": 100, "offset": 1, "path": "tmp/health.json"}}'
- `test_hand7-019` three_level_drill: fails json no call | 'find the error codes table somewhere inside api/' -> 'The directory "api" contains two subdirectories, "v1" and "v2". There is also a file named "overview.md" inside the "api" directory.'
