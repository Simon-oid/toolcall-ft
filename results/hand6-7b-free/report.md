# hand6-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.881 [0.786, 0.976] |
| L1 json | 0.881 [0.786, 0.976] |
| L2 schema | 0.881 [0.786, 0.976] |
| L3 tool | 0.738 [0.595, 0.857] |
| L4 args | 0.619 [0.476, 0.762] |
| abstain | 0.875 [0.750, 0.969] |
| decision | 0.878 [0.797, 0.946] |
| step right | 0.676 [0.568, 0.784] |
| answer grounded | 0.733 [0.567, 0.900] |
| episode right | 0.438 [0.281, 0.625] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.33 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 1.00 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.67 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 1.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 1.00 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.67 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 0.67 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.67 |

Failures (first 12):

- `test_hand6-001` find_and_read_changelog: fails args  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "fs_read", "arguments": {"offset": 1, "limit": 1, "path": "docs/changelog.md"}}'
- `test_hand6-003` crag_then_read_source: fails args  | 'find anything about rate limiting and show me the actual file it comes from' -> '{"name": "crag_search", "arguments": {"query": "rate limiting", "k": 5}}'
- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The rate limiting policy is described in the file `config/policies.md`. According to the document, all API endpoints enforce a rate limit of'
- `test_hand6-010` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_stat", "arguments": {"path": "src/constants.py"}}'
- `test_hand6-013` drill_down_two_levels: fails args  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_list", "arguments": {"path": "experiments/run-042"}}'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "The debug server's port is not stored in the file system or the document index that I have access to. Typically, this information would be s"
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The debug server listens on port 5000. You can enable debug mode by setting the environment variable `DEBUG=1`.'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"content": "318\\n", "path": "data/sales_total.txt"}}'
- `test_hand6-023` check_index_then_search: fails tool  | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'The embedding dimension in the index is 768 dimensions. This information was confirmed by searching for "embedding dimension" in the index.'
- `test_hand6-025` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_read", "arguments": {"path": "ops/migration-guide.md"}}'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_list", "arguments": {"path": "ops/terraform"}}'
