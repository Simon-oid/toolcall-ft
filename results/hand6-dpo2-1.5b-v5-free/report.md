# hand6-dpo2-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo2-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-27-gc51a5b5 · date: 2026-11-24 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.976 [0.929, 1.000] |
| L1 json | 0.929 [0.833, 1.000] |
| L2 schema | 0.929 [0.833, 1.000] |
| L3 tool | 0.810 [0.690, 0.929] |
| L4 args | 0.619 [0.476, 0.762] |
| abstain | 0.438 [0.281, 0.625] |
| decision | 0.743 [0.635, 0.838] |
| step right | 0.500 [0.392, 0.608] |
| answer grounded | 0.333 [0.167, 0.500] |
| episode right | 0.156 [0.031, 0.281] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 0.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 0.67 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.00 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 0.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.33 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 0.50 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 1.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 0.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.67 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails json  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "fs_list", "arguments": {"path": "docs/", "query": "the latest entry from the changelog"}'
- `test_hand6-002` find_and_read_changelog: called '{"name": "fs_write", "arguments": {"path": "docs/changes.md", "content": "fixed UTF-8 handling in export\\nbumped depende' | 'I need the latest entry from the changelog somewhere in the docs/ folder'
- `test_hand6-003` crag_then_read_source: fails args  | 'find anything about rate limiting and show me the actual file it comes from' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "k": 1}}'
- `test_hand6-005` crag_then_read_source: called '{"name": "fs_write", "arguments": {"path": "docs/limits.md", "content": "All API endpoints enforce a rate limit of 200 r' | 'find anything about rate limiting and show me the actual file it comes from'
- `test_hand6-008` check_size_then_read: called '{"name": "fs_write", "arguments": {"path": "env.yaml", "content": "python: 3.11\\ndependencies:\\n  - torch>=2.1\\n  - tran' | "how big is env.yaml and can you show me what's inside?"
- `test_hand6-009` read_edit_write: fails args  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_read", "arguments": {"path": "src/constants.py", "offset": 10, "limit": 25}}'
- `test_hand6-010` read_edit_write: fails args  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_write", "arguments": {"path": "src/constants.py", "content": "MAX_RETRIES = 6"}}'
- `test_hand6-013` drill_down_two_levels: fails tool  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_read", "arguments": {"path": "experiments/experiments.txt"}}'
- `test_hand6-016` search_refine_search: fails args  | 'what port does the debug server listen on' -> '{"name": "crag_search", "arguments": {"query": "the debug server listens on"}}'
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'DEBUG=1'
- `test_hand6-020` read_csv_write_summary: fails json  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "120\\n135\\n98\\n110\\n142\\n158\\n"}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to the index (research/architecture.md): The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
