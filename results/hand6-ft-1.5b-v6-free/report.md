# hand6-ft-1.5b-v6-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.905 [0.810, 0.976] |
| L1 json | 0.905 [0.810, 0.976] |
| L2 schema | 0.881 [0.762, 0.976] |
| L3 tool | 0.786 [0.643, 0.905] |
| L4 args | 0.667 [0.524, 0.810] |
| abstain | 0.875 [0.750, 0.969] |
| decision | 0.892 [0.811, 0.959] |
| step right | 0.608 [0.500, 0.716] |
| answer grounded | 0.500 [0.333, 0.667] |
| episode right | 0.375 [0.219, 0.562] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 1.00 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 0.67 |
| drill_down_two_levels | 4 | 0.50 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 0.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.67 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.67 |
| read_makefile_fix_target | 3 | 0.33 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 1.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.00 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 1.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.33 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails tool  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "crag_search", "arguments": {"query": "the changelog"}}'
- `test_hand6-002` find_and_read_changelog: reply lacks the tool's fact | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry is in docs/changelog.md: \n\n- fixed UTF-8 handling in export\n- bumped dependency on lz4 to 1.10'
- `test_hand6-005` crag_then_read_source: reply lacks the tool's fact | 'find anything about rate limiting and show me the actual file it comes from' -> 'The docs say: All API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-010` read_edit_write: fails args  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_write", "arguments": {"path": "src/constants.py", "content": "MAX_RETRIES = 6"}}'
- `test_hand6-013` drill_down_two_levels: fails tool  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_read", "arguments": {"path": "experiments/README"}}'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'Here is experiments/run-043/README.md:'
- `test_hand6-016` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_list", "arguments": {"path": "server"}}'
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'According to docs/faq.md: Set DEBUG=1 in your environment.'
- `test_hand6-018` search_refine_search: reply lacks the tool's fact | 'what port does the debug server listen on' -> 'According to docs/faq.md: DEBUG=1 in your environment.'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "north: 120\\nsouth: 98\\neast: 142\\n"}}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to the index (research/architecture.md): The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_read", "arguments": {"path": "ops/migration_guide"}}'
