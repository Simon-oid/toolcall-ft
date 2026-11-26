# hand8-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-25 · cases: 90

## test_hand8 (47 need a call, 43 need none, 43 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.660 [0.511, 0.787] |
| L1 json | 0.660 [0.511, 0.787] |
| L2 schema | 0.596 [0.447, 0.723] |
| L3 tool | 0.426 [0.277, 0.574] |
| L4 args | 0.255 [0.128, 0.383] |
| abstain | 0.837 [0.721, 0.930] |
| decision | 0.744 [0.656, 0.833] |
| step right | 0.433 [0.333, 0.533] |
| answer grounded | 0.657 [0.486, 0.800] |
| episode right | 0.302 [0.163, 0.442] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_ambiguous_pronoun | 1 | 1.00 |
| base_list_then_read | 3 | 0.33 |
| base_offtopic_question | 1 | 0.00 |
| base_ordinal_second | 2 | 0.50 |
| base_pronoun_it | 1 | 1.00 |
| base_read_simple | 2 | 0.50 |
| base_same_folder | 2 | 0.50 |
| base_search_no_results | 2 | 0.00 |
| base_search_then_write | 3 | 0.33 |
| base_simple_search | 2 | 1.00 |
| base_stat_then_read | 3 | 0.00 |
| base_thanks_after_write | 1 | 1.00 |
| base_unsupported_after_read | 1 | 0.00 |
| f1_drill_to_nested_config | 4 | 0.25 |
| f1_search_read_follow_ref | 4 | 0.00 |
| f2_file_missing_list_parent | 3 | 0.33 |
| f2_search_miss_refine | 3 | 0.00 |
| f3_empty_index_abort | 1 | 0.00 |
| f3_file_gone_twice | 1 | 0.00 |
| f3_size_in_listing | 1 | 1.00 |
| f4_add_yaml_entry | 3 | 0.33 |
| f4_edit_toml_timeout | 3 | 0.33 |
| f5_check_permissions | 3 | 0.33 |
| f5_largest_file_mtime | 3 | 0.33 |
| f6_paginated_access_log | 2 | 0.50 |
| f6_specific_range | 2 | 0.50 |
| f7_wrong_env_correction | 2 | 0.50 |
| f7_wrong_folder_redirect | 2 | 1.00 |
| f8_write_bytes_from_history | 1 | 1.00 |
| f8_write_readback | 3 | 0.33 |
| new_ambiguous_mid_chain | 2 | 0.50 |
| new_ask_about_second_chunk | 1 | 1.00 |
| new_cannot_execute | 1 | 0.00 |
| new_conditional_age_check | 2 | 1.00 |
| new_greeting_no_action | 1 | 1.00 |
| new_infer_from_context | 1 | 1.00 |
| new_read_then_search_correct_value | 3 | 0.33 |
| new_search_then_save | 3 | 0.33 |
| new_stat_to_distinguish_type | 2 | 1.00 |
| new_two_requests_one_msg | 3 | 0.33 |
| new_unsupported_operation | 1 | 1.00 |
| new_user_changes_mind | 2 | 0.50 |
| new_write_then_search | 3 | 0.67 |

Failures (first 12):

- `test_hand8-000` f1_drill_to_nested_config: fails tool  | "somewhere inside platform/ there's a redis.conf, find it and show me what's inside" -> '{"name": "fs_read", "arguments": {"path": "platform/redis.conf"}}'
- `test_hand8-001` f1_drill_to_nested_config: fails json no call | "somewhere inside platform/ there's a redis.conf, find it and show me what's inside" -> "I found the Redis configuration file (redis.conf) inside the platform directory. Here's what's inside:\n\n1. **Overview.md**\n   - This file co"
- `test_hand8-002` f1_drill_to_nested_config: fails json no call | "somewhere inside platform/ there's a redis.conf, find it and show me what's inside" -> "I found the redis.conf file inside the platform/cache directory. Here's its content:\n\n[cos 0.56  bm25 0.72  fusion 0.68] platform/cache/redi"
- `test_hand8-004` f1_search_read_follow_ref: fails tool  | 'look up our logging policy and follow any file it references' -> '{"name": "fs_list", "arguments": {"path": "/logging"}}'
- `test_hand8-005` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'The logging policy states that all services must log to stdout in JSON format. You can find the schema for the log fields in `ops/log-schema'
- `test_hand8-006` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'The logging policy states that all services must log to stdout in JSON format. The retention period is 14 days in Loki, and alerts are trigg'
- `test_hand8-007` f1_search_read_follow_ref: reply lacks the tool's fact | 'look up our logging policy and follow any file it references' -> 'The logging policy states that all services must log to stdout in JSON format. The log schema is defined in `ops/log-schema.json`, which inc'
- `test_hand8-008` f2_file_missing_list_parent: fails schema {'path': '/limit', 'keyword': 'type', 'message': 'expected type integer'} | 'read the runbook at ops/incident-runbook.md' -> '{"name": "fs_read", "arguments": {"path": "ops/incident-runbook.md", "limit": null, "offset": null}}'
- `test_hand8-009` f2_file_missing_list_parent: fails json no call | 'read the runbook at ops/incident-runbook.md' -> 'The file `ops/incident-runbook.md` does not exist in the specified directory. Please check the file path and try again.'
- `test_hand8-011` f2_search_miss_refine: fails json no call | "what's the WAL mode setting for our database?" -> "I don't have direct access to the database configuration settings. However, you can check the WAL (Write-Ahead Logging) mode setting by exam"
- `test_hand8-012` f2_search_miss_refine: fails json no call | "what's the WAL mode setting for our database?" -> 'The Write-Ahead Logging (WAL) mode is used by the database.'
- `test_hand8-013` f2_search_miss_refine: reply lacks the tool's fact | "what's the WAL mode setting for our database?" -> 'The WAL mode is set to `WAL` (Write-Ahead Logging) in our database. This is a journaling method used by databases.'
