# hand6-ft-1.5b-v4-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v4-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-19-g183477c · date: 2026-11-22 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.667 [0.524, 0.810] |
| L1 json | 0.667 [0.524, 0.810] |
| L2 schema | 0.643 [0.500, 0.786] |
| L3 tool | 0.500 [0.357, 0.643] |
| L4 args | 0.310 [0.167, 0.452] |
| abstain | 0.781 [0.625, 0.906] |
| decision | 0.716 [0.608, 0.811] |
| step right | 0.432 [0.324, 0.541] |
| answer grounded | 0.567 [0.400, 0.733] |
| episode right | 0.250 [0.094, 0.406] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.33 |
| check_perms_then_read | 3 | 0.33 |
| check_size_then_read | 3 | 0.00 |
| compare_two_configs | 3 | 0.67 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.25 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.67 |
| find_and_read_changelog | 3 | 0.00 |
| followup_line_count | 1 | 0.00 |
| followup_read_crag_hit | 2 | 1.00 |
| followup_size_of_it | 2 | 0.50 |
| list_then_stat_largest | 3 | 0.00 |
| missing_file_fallback_search | 3 | 0.00 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.67 |
| read_makefile_fix_target | 3 | 0.33 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 0.33 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 1.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.67 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails args  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "fs_list", "arguments": {"path": "docs/changelog"}}'
- `test_hand6-001` find_and_read_changelog: fails json no call | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry in the docs/ folder is changelog.md, which has been updated recently.'
- `test_hand6-002` find_and_read_changelog: reply lacks the tool's fact | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'The latest entry from the changelog is dated November 18, 2026. It includes a fix for UTF-8 handling in export and a bump to dependency on l'
- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The file that contains the information about rate limiting is `config/policies.md`. It states that all API endpoints enforce a rate limit of'
- `test_hand6-005` crag_then_read_source: called '{"name": "fs_read", "arguments": {"path": "config/policies.md", "offset": 10, "limit": 5}}' | 'find anything about rate limiting and show me the actual file it comes from'
- `test_hand6-006` check_size_then_read: fails tool  | "how big is env.yaml and can you show me what's inside?" -> '{"name": "fs_read", "arguments": {"path": "env.yaml"}}'
- `test_hand6-007` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> 'The file `env.yaml` is 87 bytes in size. Here are the details:\n\n- Type: File\n- Size: 87 bytes\n- Modified: September 14, 2026 at 8:30 AM UTC\n'
- `test_hand6-008` check_size_then_read: called '{"name": "fs_read", "arguments": {"path": "requirements.txt"}}' | "how big is env.yaml and can you show me what's inside?"
- `test_hand6-010` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> "The file src/constants.py has the following values:\n\n- MAX_RETRIES: 3\n- TIMEOUT_SEC: 30\n- BUFFER_KB: 256\n\nI've doubled the value of MAX_RETR"
- `test_hand6-012` drill_down_two_levels: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "crag_search", "arguments": {"query": "readme", "path": "experiments"}}'
- `test_hand6-013` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'I found the file `params.json` in the experiments folder. It has 110 lines of text.'
- `test_hand6-015` drill_down_two_levels: called '{"name": "fs_read", "arguments": {"path": "experiments/run-043/metrics.csv"}}' | 'find me the readme inside the experiments folder, it should be nested somewhere'
