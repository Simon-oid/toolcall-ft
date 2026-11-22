# hand6-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.571 [0.429, 0.714] |
| L1 json | 0.571 [0.429, 0.714] |
| L2 schema | 0.476 [0.333, 0.619] |
| L3 tool | 0.381 [0.238, 0.524] |
| L4 args | 0.262 [0.143, 0.405] |
| abstain | 0.906 [0.781, 1.000] |
| decision | 0.716 [0.608, 0.811] |
| step right | 0.432 [0.324, 0.541] |
| answer grounded | 0.633 [0.467, 0.800] |
| episode right | 0.219 [0.094, 0.375] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.33 |
| check_perms_then_read | 3 | 0.67 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 0.67 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.50 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.00 |
| missing_file_fallback_search | 3 | 0.00 |
| open_the_second | 2 | 0.50 |
| paginated_read | 3 | 0.00 |
| read_csv_write_summary | 3 | 0.33 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.33 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 0.00 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.67 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 0.50 |
| write_sibling_file | 2 | 1.00 |
| write_then_verify | 3 | 0.33 |

Failures (first 12):

- `test_hand6-001` find_and_read_changelog: fails json no call | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry in the changelog is in `docs/changelog.md`.'
- `test_hand6-002` find_and_read_changelog: reply lacks the tool's fact | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry in the changelog is dated November 18, 2026. It mentions fixing UTF-8 handling in the export and bumping the dependency on '
- `test_hand6-003` crag_then_read_source: fails tool  | 'find anything about rate limiting and show me the actual file it comes from' -> '{"name": "fs_list", "arguments": {"path": "rate_limiting"}}'
- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The rate limiting information is found in the file `config/policies.md`. The relevant content is:\n\n[cos 0.831  bm25 7.40  fusion 0.041] conf'
- `test_hand6-007` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> 'The file `env.yaml` is 87 bytes in size. Here is its content:\n\n```yaml\n# This is an example configuration file for your application.\n# It co'
- `test_hand6-009` read_edit_write: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_read", "arguments": {"path": "/path/to/src/constants.py", "limit": null, "offset": null}}'
- `test_hand6-010` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> 'The file `src/constants.py` contains the following values:\n- `MAX_RETRIES` is set to 3\n- `TIMEOUT_SEC` is set to 30\n- `BUFFER_KB` is set to '
- `test_hand6-013` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'The experiments folder contains two directories: `run-042` and `run-043`. To find the README inside the experiments folder, I will check the'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'The README.md file is located inside the experiments/run-043 folder.'
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The debug server listens on port 8000.'
- `test_hand6-019` read_csv_write_summary: fails tool  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"content": "Grand total: [total_sales]", "path": "data/sales_total.txt"}}'
- `test_hand6-020` read_csv_write_summary: fails args  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "north: 258, south: 208, east: 298"}}'
