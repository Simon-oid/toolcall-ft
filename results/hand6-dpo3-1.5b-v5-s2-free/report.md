# hand6-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.048 [0.000, 0.119] |
| L1 json | 0.048 [0.000, 0.119] |
| L2 schema | 0.048 [0.000, 0.119] |
| L3 tool | 0.024 [0.000, 0.071] |
| L4 args | 0.024 [0.000, 0.071] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.459 [0.351, 0.568] |
| step right | 0.338 [0.230, 0.446] |
| answer grounded | 0.733 [0.567, 0.900] |
| episode right | 0.156 [0.031, 0.281] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 0.00 |
| check_index_then_search | 3 | 0.33 |
| check_perms_then_read | 3 | 0.33 |
| check_size_then_read | 3 | 0.00 |
| compare_two_configs | 3 | 0.33 |
| crag_then_read_source | 3 | 0.33 |
| drill_down_two_levels | 4 | 0.25 |
| empty_index | 1 | 0.00 |
| error_already_seen | 1 | 0.00 |
| explore_subdir_from_root | 3 | 0.33 |
| find_and_read_changelog | 3 | 0.33 |
| followup_line_count | 1 | 1.00 |
| followup_read_crag_hit | 2 | 0.50 |
| followup_size_of_it | 2 | 0.50 |
| list_then_stat_largest | 3 | 0.00 |
| missing_file_fallback_search | 3 | 0.33 |
| open_the_second | 2 | 0.50 |
| paginated_read | 3 | 0.00 |
| read_csv_write_summary | 3 | 0.33 |
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.33 |
| same_folder_different_file | 2 | 0.50 |
| search_and_save_answer | 3 | 0.33 |
| search_no_results | 2 | 0.00 |
| search_refine_search | 3 | 0.33 |
| thanks_no_action | 1 | 1.00 |
| topic_change_no_call | 1 | 1.00 |
| user_disputes_result | 1 | 1.00 |
| verify_written_file | 2 | 0.50 |
| write_sibling_file | 2 | 0.50 |
| write_then_verify | 3 | 0.33 |

Failures (first 12):

- `test_hand6-000` find_and_read_changelog: fails json no call | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'Which file should I look in the docs/ folder?'
- `test_hand6-001` find_and_read_changelog: fails json no call | 'I need the latest entry from the changelog somewhere in the docs/ folder' -> 'I found it in docs: changelog.md. It says: This is the latest entry from the changelog.'
- `test_hand6-003` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'Happy to help. What should I look up: rate limiting?'
- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The docs say: All API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-006` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> 'Which folder should I look in? (e.g., home, work)'
- `test_hand6-007` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> "The file is 87 bytes. What should I do with it? I can read its contents, but I can't change the name or location. Which part of env.yaml sho"
- `test_hand6-008` check_size_then_read: reply lacks the tool's fact | "how big is env.yaml and can you show me what's inside?" -> 'The contents of env.yaml:\n\npython: 3.11\ndependencies:\n  - torch>=2.1\n  - transformers\n  - datasets\ndev:\n  - pytest'
- `test_hand6-009` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> 'What should the new value be?'
- `test_hand6-010` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> 'The contents of src/constants.py:\n\nMAX_RETRIES = 3\nTIMEOUT_SEC = 30\nBUFFER_KB = 256\n\nsrc/constants.py has a MAX_RETRIES value, which is 3. I'
- `test_hand6-012` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'Which folder do you mean? experiments or something else?'
- `test_hand6-013` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'I found what I mean: experiments/run-042. Let me check that folder to see if it contains a file called readme. {"name": "fs_read", "argument'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'The contents of experiments/run-043/README.md:metrics.csv is 3200 bytes. It says: metrics.csv is 3200 bytes. The contents of experiments/run'
