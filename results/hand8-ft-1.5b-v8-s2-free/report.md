# hand8-ft-1.5b-v8-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 90

## test_hand8 (47 need a call, 43 need none, 43 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.979 [0.936, 1.000] |
| L1 json | 0.979 [0.936, 1.000] |
| L2 schema | 0.979 [0.936, 1.000] |
| L3 tool | 0.915 [0.830, 0.979] |
| L4 args | 0.830 [0.723, 0.936] |
| abstain | 0.860 [0.744, 0.953] |
| decision | 0.922 [0.867, 0.978] |
| step right | 0.800 [0.711, 0.878] |
| answer grounded | 0.771 [0.629, 0.914] |
| episode right | 0.651 [0.512, 0.791] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_ambiguous_pronoun | 1 | 1.00 |
| base_list_then_read | 3 | 1.00 |
| base_offtopic_question | 1 | 1.00 |
| base_ordinal_second | 2 | 1.00 |
| base_pronoun_it | 1 | 0.00 |
| base_read_simple | 2 | 0.50 |
| base_same_folder | 2 | 1.00 |
| base_search_no_results | 2 | 0.50 |
| base_search_then_write | 3 | 0.67 |
| base_simple_search | 2 | 0.50 |
| base_stat_then_read | 3 | 1.00 |
| base_thanks_after_write | 1 | 1.00 |
| base_unsupported_after_read | 1 | 1.00 |
| f1_drill_to_nested_config | 4 | 1.00 |
| f1_search_read_follow_ref | 4 | 0.25 |
| f2_file_missing_list_parent | 3 | 1.00 |
| f2_search_miss_refine | 3 | 0.33 |
| f3_empty_index_abort | 1 | 1.00 |
| f3_file_gone_twice | 1 | 1.00 |
| f3_size_in_listing | 1 | 1.00 |
| f4_add_yaml_entry | 3 | 1.00 |
| f4_edit_toml_timeout | 3 | 1.00 |
| f5_check_permissions | 3 | 0.67 |
| f5_largest_file_mtime | 3 | 1.00 |
| f6_paginated_access_log | 2 | 1.00 |
| f6_specific_range | 2 | 1.00 |
| f7_wrong_env_correction | 2 | 0.50 |
| f7_wrong_folder_redirect | 2 | 1.00 |
| f8_write_bytes_from_history | 1 | 1.00 |
| f8_write_readback | 3 | 1.00 |
| new_ambiguous_mid_chain | 2 | 0.50 |
| new_ask_about_second_chunk | 1 | 1.00 |
| new_cannot_execute | 1 | 0.00 |
| new_conditional_age_check | 2 | 0.50 |
| new_greeting_no_action | 1 | 1.00 |
| new_infer_from_context | 1 | 0.00 |
| new_read_then_search_correct_value | 3 | 1.00 |
| new_search_then_save | 3 | 1.00 |
| new_stat_to_distinguish_type | 2 | 1.00 |
| new_two_requests_one_msg | 3 | 0.67 |
| new_unsupported_operation | 1 | 1.00 |
| new_user_changes_mind | 2 | 0.50 |
| new_write_then_search | 3 | 1.00 |

Failures (first 12):

- `test_hand8-005` f1_search_read_follow_ref: fails args  | 'look up our logging policy and follow any file it references' -> '{"name": "fs_read", "arguments": {"path": "ops/log-schema.json"}}'
- `test_hand8-006` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'The contents of ops/logging-policy.md:\n\n# Logging Policy\n\nAll services log to stdout in JSON.\nFields: see ops/log-schema.json.\nRetention: 14'
- `test_hand8-007` f1_search_read_follow_ref: reply lacks the tool's fact | 'look up our logging policy and follow any file it references' -> 'ops/log-schema.json says:\n\n{\n  "timestamp": "ISO-8601",\n  "level": "INFO|WARN|ERROR",\n  "service": "string",\n  "message": "string",\n  "trace'
- `test_hand8-011` f2_search_miss_refine: fails tool  | "what's the WAL mode setting for our database?" -> '{"name": "fs_stat", "arguments": {"path": "wals/config"}}'
- `test_hand8-012` f2_search_miss_refine: fails args  | "what's the WAL mode setting for our database?" -> '{"name": "crag_search", "arguments": {"query": "journaling"}}'
- `test_hand8-027` f5_check_permissions: fails tool  | 'list creds/ and tell me the permissions of the .pem file' -> '{"name": "fs_list", "arguments": {"path": "creds/openssl"}}'
- `test_hand8-033` f7_wrong_env_correction: fails args  | 'no sorry, I meant the staging one' -> '{"name": "fs_read", "arguments": {"path": "config/database_staging.yaml"}}'
- `test_hand8-043` new_two_requests_one_msg: reply lacks the tool's fact | 'read the license file at LICENSE and also check how many docs are in the crag index' -> 'The index has 980 chunks.'
- `test_hand8-045` new_conditional_age_check: called '{"name": "fs_stat", "arguments": {"path": "exports/report.pdf", "field": "modified"}}' | "check the modification date of exports/report.pdf — if it's older than 2026-10-01 let me know, otherwise just say it's recent"
- `test_hand8-047` new_user_changes_mind: called '{"name": "fs_list", "arguments": {"path": "src"}}' | 'actually read the changelog — wait no, just list the root directory'
- `test_hand8-055` new_cannot_execute: called '{"name": "fs_list", "arguments": {"path": "tests"}}' | 'run pytest on the tests/ folder and show me the output'
- `test_hand8-062` new_infer_from_context: called '{"name": "fs_read", "arguments": {"path": "gateway/routes.yaml"}}' | 'how many routes are defined?'
