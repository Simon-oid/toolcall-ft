# hand6-ft-1.5b-v4-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v4-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.667 [0.524, 0.810] |
| L1 json | 0.643 [0.500, 0.786] |
| L2 schema | 0.643 [0.500, 0.786] |
| L3 tool | 0.548 [0.405, 0.690] |
| L4 args | 0.405 [0.262, 0.548] |
| abstain | 0.844 [0.719, 0.969] |
| decision | 0.743 [0.635, 0.838] |
| step right | 0.500 [0.392, 0.608] |
| answer grounded | 0.600 [0.433, 0.767] |
| episode right | 0.281 [0.125, 0.438] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.33 |
| check_perms_then_read | 3 | 0.33 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.75 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.33 |
| find_and_read_changelog | 3 | 0.00 |
| followup_line_count | 1 | 0.00 |
| followup_read_crag_hit | 2 | 1.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.00 |
| missing_file_fallback_search | 3 | 0.00 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.67 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 0.67 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.00 |
| write_then_verify | 3 | 0.67 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails args  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "fs_list", "arguments": {"path": "docs/changelog"}}'
- `test_hand6-001` find_and_read_changelog: fails json no call | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry in the docs/ folder is changelog.md, which has 2340 bytes.'
- `test_hand6-002` find_and_read_changelog: reply lacks the tool's fact | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry from the changelog is dated November 18, 2026. It mentions fixing UTF-8 handling in export and bumping the dependency on lz'
- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The file that contains the information about rate limiting is `config/policies.md`. It states: "All API endpoints enforce a rate limit of 20'
- `test_hand6-005` crag_then_read_source: called '{"name": "fs_read", "arguments": {"path": "config/policies.md"}}' | 'find anything about rate limiting and show me the actual file it comes from'
- `test_hand6-007` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> 'The file `env.yaml` is 87 bytes in size. Here are the contents:\n\n```\nFOO=bar\nBAZ=baz\n```'
- `test_hand6-010` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> 'The file src/constants.py has the following values:\n\n- MAX_RETRIES: 3\n- TIMEOUT_SEC: 30\n- BUFFER_KB: 256'
- `test_hand6-013` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'I found the file `params.json` in the experiments folder. It contains:'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "I can't check the port that the debug server listens on: my tools can only search and inspect the document index, and list, read, stat or wr"
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The documentation states that you can enable debug mode by setting the `DEBUG` environment variable to `1`.'
- `test_hand6-020` read_csv_write_summary: fails json  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "total: 360, 333"}'
- `test_hand6-023` check_index_then_search: fails json no call | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> 'There are 1420 chunks in the document index. Here is one of them, along with its path:\n\n[cos 0.59  bm25  fusion  data/knowledge.db/1.txt] 1.'
