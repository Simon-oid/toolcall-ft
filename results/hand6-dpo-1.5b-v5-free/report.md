# hand6-dpo-1.5b-v5-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 74

## test_hand6 (42 need a call, 32 need none, 32 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.738 [0.595, 0.857] |
| L1 json | 0.714 [0.571, 0.833] |
| L2 schema | 0.714 [0.571, 0.833] |
| L3 tool | 0.667 [0.524, 0.810] |
| L4 args | 0.595 [0.452, 0.738] |
| abstain | 0.938 [0.844, 1.000] |
| decision | 0.824 [0.730, 0.905] |
| step right | 0.635 [0.527, 0.743] |
| answer grounded | 0.667 [0.500, 0.833] |
| episode right | 0.438 [0.281, 0.625] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_which_file | 1 | 1.00 |
| answer_from_context | 1 | 1.00 |
| check_index_then_search | 3 | 0.67 |
| check_perms_then_read | 3 | 1.00 |
| check_size_then_read | 3 | 0.67 |
| compare_two_configs | 3 | 1.00 |
| crag_then_read_source | 3 | 0.33 |
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
| read_edit_write | 3 | 0.33 |
| read_makefile_fix_target | 3 | 0.33 |
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

- `test_hand6-004` crag_then_read_source: fails json no call | 'find anything about rate limiting and show me the actual file it comes from' -> 'The docs say: All API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-005` crag_then_read_source: reply lacks the tool's fact | 'find anything about rate limiting and show me the actual file it comes from' -> 'config/policies.md says:\n\nAll API endpoints enforce a rate limit of 200 requests per minute per user.'
- `test_hand6-007` check_size_then_read: fails json no call | "how big is env.yaml and can you show me what's inside?" -> "The file is 87 bytes. Here's what I found in env.yaml:\n\n```yaml\nfoo: bar\nbaz: qux\n```\n\nI can save this to a new file if you'd like. What sho"
- `test_hand6-009` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> 'I can do that once I know more. What should the new value be?'
- `test_hand6-010` read_edit_write: fails json no call | 'the file src/constants.py has a MAX_RETRIES value, double it' -> "I can't change src/constants.py: it's empty. I'll save the new value to a new file instead. What should the new value be?"
- `test_hand6-013` drill_down_two_levels: fails tool  | 'find me the readme inside the experiments folder, it should be nested somewhere' -> '{"name": "fs_read", "arguments": {"path": "experiments/run-042"}}'
- `test_hand6-014` drill_down_two_levels: fails json no call | 'find me the readme inside the experiments folder, it should be nested somewhere' -> 'The contents of experiments/run-043:\n\nmetrics.csv\nREADME.md\ncheckpoint.pt'
- `test_hand6-016` search_refine_search: fails json no call | 'what port does the debug server listen on' -> "I can't check the running processes: my tools can only search and inspect the document index, and list, read, stat or write files in the san"
- `test_hand6-017` search_refine_search: fails json no call | 'what port does the debug server listen on' -> 'The documentation says to set the variable DEBUG to 1 to enable debug mode. That means that the debug server listens on port 5005 by default'
- `test_hand6-018` search_refine_search: reply lacks the tool's fact | 'what port does the debug server listen on' -> 'According to docs/faq.md: Set DEBUG=1 in your environment.'
- `test_hand6-020` read_csv_write_summary: fails json  | 'read data/sales.csv and create a file called data/sales_total.txt with just the grand total' -> '{"name": "fs_write", "arguments": {"path": "data/sales_total.txt", "content": "120+135+98+110+142+158=763"}'
- `test_hand6-024` check_index_then_search: reply lacks the tool's fact | 'first tell me how many documents are in the index, then look up "embedding dimension"' -> "Here's what I found in docs/research/architecture.md: The sentence encoder outputs 768-dimensional vectors projected down to 384 for retriev"
