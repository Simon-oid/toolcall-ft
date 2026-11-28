# hand6-ft-1.5b-v8-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.905 [0.810, 0.976] |
| L4 args | 0.738 [0.595, 0.857] |
| abstain | 0.938 [0.844, 1.000] |
| decision | 0.973 [0.932, 1.000] |
| step right | 0.770 [0.676, 0.865] |
| answer grounded | 0.800 [0.633, 0.933] |
| episode right | 0.562 [0.375, 0.719] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 1.00 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 1.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.67 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 1.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 1.00 |
| missing_file_fallback_search | 3 | 0.67 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 1.00 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 1.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 1.00 |

Failures (first 12):

- `test_hand6-001` find_and_read_changelog: fails tool  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "fs_list", "arguments": {"path": "docs/changelog.md"}}'
- `test_hand6-008` check_size_then_read: reply lacks the tool's fact | "how big is env.yaml and can you show me what's inside?" -> 'The contents of env.yaml:\n\npython: 3.11\ndependencies:\n  - torch>=2.1\n  - transformers\n  - datasets\ndev:\n  - pytest'
- `test_hand6-013` drill_down_two_levels: fails args  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_list", "arguments": {"path": "experiments/run-042"}}'
- `test_hand6-016` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_list", "arguments": {"path": "debug"}}'
- `test_hand6-017` search_refine_search: fails args  | 'what port does the debug server listen on' -> '{"name": "crag_search", "arguments": {"query": "port of the debug server"}}'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "north: 120\\nsouth: 98\\neast: 142\\ngrand total: 360\\n"}}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to research/architecture.md: The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_list", "arguments": {"path": "ops/terraform"}}'
- `test_hand6-040` paginated_read: fails args  | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> '{"name": "fs_read", "arguments": {"path": "var/app.log", "offset": 50, "limit": 21}}'
- `test_hand6-042` paginated_read: reply lacks the tool's fact | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> 'Here are lines 61 to 70:\n\n2026-11-20 09:12:12 INFO  request handled in 27ms\n2026-11-20 09:12:13 INFO  healthcheck ok\n2026-11-20 09:12:14 WAR'
- `test_hand6-046` read_makefile_fix_target: fails args  | 'the build target in Makefile uses python3.9, change it to python3.11' -> '{"name": "fs_read", "arguments": {"path": "build/Makefile"}}'
- `test_hand6-058` error_already_seen: called '{"name": "fs_stat", "arguments": {"path": "archive/old_notes.txt"}}' | "hmm ok, is there any chance it's just empty?"
