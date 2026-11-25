# hand6-dpo3-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.905 [0.810, 0.976] |
| L1 json | 0.905 [0.810, 0.976] |
| L2 schema | 0.762 [0.619, 0.881] |
| L3 tool | 0.381 [0.238, 0.524] |
| L4 args | 0.333 [0.190, 0.476] |
| abstain | 0.906 [0.781, 1.000] |
| decision | 0.905 [0.838, 0.959] |
| step right | 0.473 [0.365, 0.581] |
| answer grounded | 0.633 [0.467, 0.800] |
| episode right | 0.250 [0.094, 0.406] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 0.67 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.50 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.33 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.00 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.33 |
| read_csv_write_summary | 3 | 0.33 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.33 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 0.33 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 0.50 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.67 |

Failures (first 12):

- `test_hand6-001` find_and_read_changelog: fails tool  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand6-002` find_and_read_changelog: reply lacks the tool's fact | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'Here is docs/changelog.md, the latest entry from the docs: #3: fixed UTF-8 handling in export, bumped dependency on lz4 to 1.10.'
- `test_hand6-003` crag_then_read_source: fails tool  | 'find anything about rate limiting and show me the actual file it comes from' -> '{"name": "crag_stats", "arguments": {}}'
- `test_hand6-005` crag_then_read_source: reply lacks the tool's fact | 'find anything about rate limiting and show me the actual file it comes from' -> 'The docs say: All API endpoints enforce a rate limit of 200 requests per minute per user. (config/policies.md)'
- `test_hand6-007` check_size_then_read: fails args  | "how big is env.yaml and can you show me what's inside?" -> '{"name": "fs_read", "arguments": {"path": "env.yaml", "limit": 87}}'
- `test_hand6-009` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "fs_stat", "arguments": {"path": "src/constants.py"}}'
- `test_hand6-010` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "crag_search", "arguments": {"query": "MAX_RETRIES"}}'
- `test_hand6-013` drill_down_two_levels: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "crag_search", "arguments": {"query": "readme", "path": "experiments"}}'
- `test_hand6-014` drill_down_two_levels: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "crag_search", "arguments": {"query": "README.md", "path": "experiments/run-043"}}'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "To answer that, I need one detail first. Which machine's log should I read?"
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'According to docs/faq.md (line 3): Set DEBUG=1 in your environment. So you just have to add that to your environment variables to enable the'
- `test_hand6-019` read_csv_write_summary: fails tool  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_stat", "arguments": {"path": "data/sales.csv"}}'
