# hand6-grpo-1.5b-v7-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: grpo-1.5b-v7-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-39-g8902c62-dirty · date: 2026-11-27 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 0.929 [0.833, 1.000] |
| L4 args | 0.810 [0.690, 0.929] |
| abstain | 0.969 [0.906, 1.000] |
| decision | 0.986 [0.959, 1.000] |
| step right | 0.824 [0.730, 0.905] |
| answer grounded | 0.833 [0.700, 0.967] |
| episode right | 0.688 [0.531, 0.844] |

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
| empty_index | 1 | 1.00 |
| error_already_seen | 1 | 1.00 |
| explore_subdir_from_root | 3 | 1.00 |
| find_and_read_changelog | 3 | 1.00 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 1.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 1.00 |
| missing_file_fallback_search | 3 | 0.67 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 1.00 |
| read_makefile_fix_target | 3 | 1.00 |
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

- `test_hand6-013` drill_down_two_levels: fails args  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_list", "arguments": {"path": "experiments/run-042"}}'
- `test_hand6-016` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_list", "arguments": {"path": "server"}}'
- `test_hand6-017` search_refine_search: fails tool  | 'what port does the debug server listen on' -> '{"name": "fs_read", "arguments": {"path": "docs/faq.md"}}'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "region,q1,q2\\nnorth,120,135\\ntotal,278,275\\nsouth,98,110\\neas'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'According to research/architecture.md: The sentence encoder outputs 768-dimensional vectors projected down to 384 for retrieval.'
- `test_hand6-026` missing_file_fallback_search: fails tool  | 'read the migration guide, it should be in ops/' -> '{"name": "fs_list", "arguments": {"path": "ops/terraform"}}'
- `test_hand6-040` paginated_read: fails args  | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> '{"name": "fs_read", "arguments": {"path": "var/app.log", "offset": 50, "limit": 21}}'
- `test_hand6-042` paginated_read: reply lacks the tool's fact | 'the log at var/app.log is huge, show me lines 50 to 60 and then 61 to 70' -> 'Here are lines 61 to 70:\n\n2026-11-20 09:12:12 INFO  request handled in 27ms\n2026-11-20 09:12:13 INFO  healthcheck ok\n2026-11-20 09:12:14 WAR'
- `test_hand6-057` answer_from_context: reply lacks the tool's fact | 'and what port is the database on?' -> 'The server listens on port 8080, as configured in app/settings.toml.'
- `test_hand6-068` search_no_results: fails args  | 'can you dig deeper?' -> '{"name": "crag_search", "arguments": {"query": "kubernetes pod autoscaling", "k": 10}}'
- `test_hand6-069` search_no_results: reply lacks the tool's fact | 'can you dig deeper?' -> 'From the index: HPA is the Horizontal Pod Autoscaler.'
- `test_hand6-070` write_sibling_file: fails args  | 'create ch2.md in the same folder with a chapter about configuration' -> '{"name": "fs_write", "arguments": {"path": "chapters/ch2.md", "content": "This is what chapters/ch2.md contains."}}'
