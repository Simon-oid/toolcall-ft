# hand6-dpo3-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.857 [0.738, 0.952] |
| L1 json | 0.857 [0.738, 0.952] |
| L2 schema | 0.738 [0.595, 0.857] |
| L3 tool | 0.571 [0.429, 0.714] |
| L4 args | 0.476 [0.333, 0.619] |
| abstain | 0.938 [0.844, 1.000] |
| decision | 0.892 [0.811, 0.959] |
| step right | 0.527 [0.405, 0.635] |
| answer grounded | 0.567 [0.400, 0.733] |
| episode right | 0.312 [0.156, 0.469] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 0.33 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.50 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.33 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.00 |
| followup_size_of_it | 2 | 1.00 |
| list_then_stat_largest | 3 | 0.67 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 1.00 |
| paginated_read | 3 | 0.00 |
| read_csv_write_summary | 3 | 0.67 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.67 |
| same_folder_different_file | 2 | 1.00 |
| search_and_save_answer | 3 | 0.67 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.00 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 0.00 |
| verify_written_file | 2 | 1.00 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 1.00 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails schema {'path': '/additionalProperties', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "crag_search", "arguments": {"query": "the latest entry from the changelog", "additionalProperties": false}}'
- `test_hand6-001` find_and_read_changelog: fails tool  | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> '{"name": "crag_search", "arguments": {"query": "the latest entry from the docs/ folder"}}'
- `test_hand6-004` crag_then_read_source: fails tool  | 'find anything about rate limiting and show me the actual file it comes from' -> '{"name": "crag_search", "arguments": {"query": "config/policies.md"}}'
- `test_hand6-005` crag_then_read_source: reply lacks the tool's fact | 'find anything about rate limiting and show me the actual file it comes from' -> 'The file at config/policies.md says:\n\nAll API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-008` check_size_then_read: reply lacks the tool's fact | "how big is env.yaml and can you show me what's inside?" -> 'The contents of env.yaml:\n\npython: 3.11\ndependencies:\n  - torch>=2.1\n  - transformers\n  - datasets\ndev:\n  - pytest'
- `test_hand6-009` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "crag_search", "arguments": {"query": "src/constants.py has a MAX_RETRIES value, double it"}}'
- `test_hand6-010` read_edit_write: fails tool  | 'the file src/constants.py has a MAX_RETRIES value, double it' -> '{"name": "crag_search", "arguments": {"query": "the file src/constants.py has a MAX_RETRIES value, double it"}}'
- `test_hand6-013` drill_down_two_levels: fails schema {'path': '/path', 'keyword': 'additionalProperties', 'message': 'unexpected property'} | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "crag_search", "arguments": {"query": "the readme", "path": "experiments"}}'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'The readme is in experiments/run-043/README.md:metrics.csv.'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "I can't check the running processes: there is no tool to look that up. You can use the cRAG index to search for information about your opera"
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'According to docs/faq.md: Set DEBUG=1 in your environment.'
- `test_hand6-018` search_refine_search: reply lacks the tool's fact | 'what port does the debug server listen on' -> 'According to docs/faq.md (ourkeptional): Set DEBUG=1 in your environment.'
