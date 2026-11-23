# hand6-dpo-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.952 [0.881, 1.000] |
| L1 json | 0.929 [0.833, 1.000] |
| L2 schema | 0.929 [0.833, 1.000] |
| L3 tool | 0.786 [0.667, 0.905] |
| L4 args | 0.690 [0.548, 0.833] |
| abstain | 0.906 [0.781, 1.000] |
| decision | 0.932 [0.865, 0.986] |
| step right | 0.716 [0.608, 0.811] |
| answer grounded | 0.733 [0.567, 0.900] |
| episode right | 0.469 [0.312, 0.656] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 1.00 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 1.00 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.67 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.67 |
| missing_file_fallback_search | 3 | 0.67 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 1.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 1.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 1.00 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails tool  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "crag_search", "arguments": {"query": "the latest entry from the changelog"}}'
- `test_hand6-009` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_stat", "arguments": {"path": "src/constants.py"}}'
- `test_hand6-010` read_edit_write: fails args  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_write", "arguments": {"path": "src/constants.py", "content": "MAX_RETRIES = 6"}}'
- `test_hand6-013` drill_down_two_levels: fails tool  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_read", "arguments": {"path": "experiments/run-042/readme"}}'
- `test_hand6-016` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_list", "arguments": {"path": "debug"}}'
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "The documentation says to set the variable DEBUG to 1. That's how you enable debug mode."
- `test_hand6-020` read_csv_write_summary: fails json  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "total: 460"}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'From the index (research/architecture.md): The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_read", "arguments": {"path": "ops/deploy.sh"}}'
- `test_hand6-040` paginated_read: fails args  | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> '{"name": "fs_read", "arguments": {"path": "var/app.log", "offset": 50, "limit": 21}}'
- `test_hand6-042` paginated_read: reply lacks the tool's fact | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> 'The relevant lines from var/app.log:\n\n2026-11-20 09:12:01 INFO  request handled in 42ms\n2026-11-20 09:12:02 WARN  connection pool near capac'
- `test_hand6-045` list_then_stat_largest: reply lacks the tool's fact | 'which file in assets/ is the biggest? I need its exact byte size and modification date' -> 'assets/hero-banner.jpg is 48,000 bytes. It was last changed on 2026-08-19.'
