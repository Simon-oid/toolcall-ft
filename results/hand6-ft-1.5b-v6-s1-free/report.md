# hand6-ft-1.5b-v6-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.881 [0.762, 0.976] |
| L1 json | 0.881 [0.762, 0.976] |
| L2 schema | 0.881 [0.762, 0.976] |
| L3 tool | 0.810 [0.690, 0.929] |
| L4 args | 0.714 [0.571, 0.833] |
| abstain | 0.938 [0.844, 1.000] |
| decision | 0.905 [0.838, 0.959] |
| step right | 0.716 [0.608, 0.811] |
| answer grounded | 0.700 [0.533, 0.867] |
| episode right | 0.531 [0.375, 0.719] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 1.00 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 1.00 |
| drill_down_two_levels | 4 | 0.50 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 1.00 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.67 |
| missing_file_fallback_search | 3 | 0.67 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 1.00 |
| read_makefile_fix_target | 3 | 0.67 |
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

- `test_hand6-013` drill_down_two_levels: fails tool  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_read", "arguments": {"path": "experiments/run-042/README"}}'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'Here is experiments/run-043/README.md:'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The debug server listens on port 8000.'
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The docs say: Set DEBUG=1 in your environment.'
- `test_hand6-018` search_refine_search: reply lacks the tool's fact | 'what port does the debug server listen on' -> 'According to docs/faq.md: Set DEBUG=1 in your environment.'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "north: 255\\nsouth: 208\\neast: 300\\n"}}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to research/architecture.md: The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_read", "arguments": {"path": "ops/migration_guide"}}'
- `test_hand6-029` write_then_verify: fails json no call | 'create a file called tmp/reminder.txt saying "submit report by Friday" and then confirm it exists' -> "It's in tmp/reminder.txt now: submit report by Friday."
- `test_hand6-030` write_then_verify: reply lacks the tool's fact | 'create a file called tmp/reminder.txt saying "submit report by Friday" and then confirm it exists' -> 'It\'s there now: tmp/reminder.txt says "submit report by Friday".'
- `test_hand6-040` paginated_read: fails args  | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> '{"name": "fs_read", "arguments": {"path": "var/app.log", "offset": 50, "limit": 21}}'
- `test_hand6-042` paginated_read: reply lacks the tool's fact | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> 'Here are lines 61 to 70 of var/app.log:\n\n2026-11-20 09:12:12 INFO  request handled in 27ms\n2026-11-20 09:12:13 INFO  healthcheck ok\n2026-11-'
