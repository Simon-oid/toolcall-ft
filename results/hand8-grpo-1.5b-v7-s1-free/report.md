# hand8-grpo-1.5b-v7-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: grpo-1.5b-v7-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-39-g8902c62-dirty · date: 2026-11-27 · cases: 90

## test_hand8 (47 need a call, 43 need none, 43 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.957 [0.894, 1.000] |
| L1 json | 0.957 [0.894, 1.000] |
| L2 schema | 0.957 [0.894, 1.000] |
| L3 tool | 0.851 [0.745, 0.936] |
| L4 args | 0.830 [0.723, 0.936] |
| abstain | 0.860 [0.744, 0.953] |
| decision | 0.911 [0.844, 0.967] |
| step right | 0.789 [0.700, 0.867] |
| answer grounded | 0.743 [0.600, 0.886] |
| episode right | 0.651 [0.512, 0.791] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_ambiguous_pronoun | 1 | 1.00 |
| base_list_then_read | 3 | 1.00 |
| base_offtopic_question | 1 | 1.00 |
| base_ordinal_second | 2 | 1.00 |
| base_pronoun_it | 1 | 1.00 |
| base_read_simple | 2 | 0.50 |
| base_same_folder | 2 | 1.00 |
| base_search_no_results | 2 | 1.00 |
| base_search_then_write | 3 | 1.00 |
| base_simple_search | 2 | 0.50 |
| base_stat_then_read | 3 | 1.00 |
| base_thanks_after_write | 1 | 1.00 |
| base_unsupported_after_read | 1 | 1.00 |
| f1_drill_to_nested_config | 4 | 1.00 |
| f1_search_read_follow_ref | 4 | 0.50 |
| f2_file_missing_list_parent | 3 | 0.33 |
| f2_search_miss_refine | 3 | 0.00 |
| f3_empty_index_abort | 1 | 0.00 |
| f3_file_gone_twice | 1 | 0.00 |
| f3_size_in_listing | 1 | 1.00 |
| f4_add_yaml_entry | 3 | 1.00 |
| f4_edit_toml_timeout | 3 | 1.00 |
| f5_check_permissions | 3 | 1.00 |
| f5_largest_file_mtime | 3 | 1.00 |
| f6_paginated_access_log | 2 | 0.50 |
| f6_specific_range | 2 | 1.00 |
| f7_wrong_env_correction | 2 | 0.50 |
| f7_wrong_folder_redirect | 2 | 1.00 |
| f8_write_bytes_from_history | 1 | 1.00 |
| f8_write_readback | 3 | 1.00 |
| new_ambiguous_mid_chain | 2 | 0.50 |
| new_ask_about_second_chunk | 1 | 1.00 |
| new_cannot_execute | 1 | 0.00 |
| new_conditional_age_check | 2 | 1.00 |
| new_greeting_no_action | 1 | 1.00 |
| new_infer_from_context | 1 | 1.00 |
| new_read_then_search_correct_value | 3 | 0.67 |
| new_search_then_save | 3 | 1.00 |
| new_stat_to_distinguish_type | 2 | 1.00 |
| new_two_requests_one_msg | 3 | 0.67 |
| new_unsupported_operation | 1 | 1.00 |
| new_user_changes_mind | 2 | 0.50 |
| new_write_then_search | 3 | 0.67 |

Failures (first 12):

- `test_hand8-006` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'The contents of ops/logging-policy.md:\n\n# Logging Policy\n\nAll services log to stdout in JSON.\nFields: see ops/log-schema.json.\nRetention: 14'
- `test_hand8-007` f1_search_read_follow_ref: reply lacks the tool's fact | 'look up our logging policy and follow any file it references' -> 'ops/logging-policy.md says:\n\nAll services log to stdout in JSON.\nFields: see ops/log-schema.json.\nRetention: 14 days in Loki.\nAlert on ERROR'
- `test_hand8-009` f2_file_missing_list_parent: fails json no call | 'read the runbook at ops/incident-runbook.md' -> 'There is no file at ops/incident-runbook.md: it does not exist.'
- `test_hand8-010` f2_file_missing_list_parent: called '{"name": "fs_read", "arguments": {"path": "ops/playbook.md"}}' | 'read the runbook at ops/incident-runbook.md'
- `test_hand8-011` f2_search_miss_refine: fails tool  | "what's the WAL mode setting for our database?" -> '{"name": "fs_read", "arguments": {"path": "wal_mode.txt"}}'
- `test_hand8-012` f2_search_miss_refine: fails tool  | "what's the WAL mode setting for our database?" -> '{"name": "fs_read", "arguments": {"path": "docs/glossary.md"}}'
- `test_hand8-013` f2_search_miss_refine: reply lacks the tool's fact | "what's the WAL mode setting for our database?" -> 'The setting is: WAL mode.'
- `test_hand8-014` f3_empty_index_abort: reply lacks the tool's fact | 'search for backup procedures then' -> "There's nothing to search: the index has 0 chunks."
- `test_hand8-015` f3_file_gone_twice: called '{"name": "fs_read", "arguments": {"path": "inventory/stock.csv"}}' | 'hmm, try reading inventory/stock.csv one more time'
- `test_hand8-030` f6_paginated_access_log: reply lacks the tool's fact | 'next 15 please' -> 'Lines 16–30 of var/access.log: 10.0.0.2 GET /api/users/3 200 9ms, 10.0.0.9 POST /api/register 201 60ms, etc.'
- `test_hand8-033` f7_wrong_env_correction: fails args  | 'no sorry, I meant the staging one' -> '{"name": "fs_read", "arguments": {"path": "config/database_staging.yaml"}}'
- `test_hand8-043` new_two_requests_one_msg: reply lacks the tool's fact | 'read the license file at LICENSE and also check how many docs are in the crag index' -> 'The index has 980 chunks.'
