# hand6-dpo2-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 0.976 [0.929, 1.000] |
| L2 schema | 0.976 [0.929, 1.000] |
| L3 tool | 0.810 [0.690, 0.929] |
| L4 args | 0.714 [0.571, 0.857] |
| abstain | 0.719 [0.562, 0.875] |
| decision | 0.878 [0.797, 0.946] |
| step right | 0.608 [0.500, 0.716] |
| answer grounded | 0.467 [0.300, 0.633] |
| episode right | 0.281 [0.125, 0.438] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 0.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 0.67 |
| crag_then_read_source | 3 | 0.67 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.33 |
| find_and_read_changelog | 3 | 1.00 |
| followup_line_count | 1 | 0.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.67 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.67 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 1.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.00 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 0.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 1.00 |

Failures (first 12):

- `test_hand6-005` crag_then_read_source: reply lacks the tool's fact | 'find anything about rate limiting and show me the actual file it comes from' -> 'config/policies.md says:\n\nAll API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-008` check_size_then_read: reply lacks the tool's fact | "how big is env.yaml and can you show me what's inside?" -> 'The contents of env.yaml:\n\npython: 3.11\ndependencies:\n  - torch>=2.1\n  - transformers\n  - datasets\ndev:\n  - pytest'
- `test_hand6-009` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_stat", "arguments": {"path": "src/constants.py"}}'
- `test_hand6-013` drill_down_two_levels: fails args  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_list", "arguments": {"path": "experiments/run-042"}}'
- `test_hand6-016` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_list", "arguments": {"path": "debug"}}'
- `test_hand6-017` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_write", "arguments": {"path": "docs/debug.conf", "content": "Set DEBUG=1 in your environment."}}'
- `test_hand6-018` search_refine_search: reply lacks the tool's fact | 'what port does the debug server listen on' -> 'docs/faq.md says: Set DEBUG=1 in your environment.'
- `test_hand6-020` read_csv_write_summary: fails json  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "north: 120\\nsouth: 98\\neast: 142\\ngrand total: 360\\n"})'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to data/knowledge.db: The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_read", "arguments": {"path": "ops/migration guide"}}'
- `test_hand6-027` missing_file_fallback_search: called '{"name": "fs_write", "arguments": {"path": "ops/migration guide", "content": "Step 1: run pg_dump on the source.\\nStep 2' | 'read the migration guide, it should be in ops/'
- `test_hand6-033` compare_two_configs: reply lacks the tool's fact | 'compare the timeout value in config/prod.yaml vs config/staging.yaml' -> 'The config/prod.yaml file has this content:\n\ntimeout_ms: 5000\nretries: 2\nlog_level: warn'
