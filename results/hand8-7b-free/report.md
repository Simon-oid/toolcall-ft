# hand8-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-25 · cases: 90

## test_hand8 (47 need a call, 43 need none, 43 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.830 [0.723, 0.936] |
| L1 json | 0.830 [0.723, 0.936] |
| L2 schema | 0.830 [0.723, 0.936] |
| L3 tool | 0.745 [0.617, 0.872] |
| L4 args | 0.447 [0.298, 0.596] |
| abstain | 0.884 [0.791, 0.977] |
| decision | 0.856 [0.778, 0.922] |
| step right | 0.622 [0.522, 0.722] |
| answer grounded | 0.857 [0.743, 0.971] |
| episode right | 0.419 [0.279, 0.558] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_ambiguous_pronoun | 1 | 1.00 |
| base_list_then_read | 3 | 0.67 |
| base_offtopic_question | 1 | 1.00 |
| base_ordinal_second | 2 | 0.50 |
| base_pronoun_it | 1 | 1.00 |
| base_read_simple | 2 | 0.50 |
| base_same_folder | 2 | 1.00 |
| base_search_no_results | 2 | 0.00 |
| base_search_then_write | 3 | 0.33 |
| base_simple_search | 2 | 0.50 |
| base_stat_then_read | 3 | 1.00 |
| base_thanks_after_write | 1 | 1.00 |
| base_unsupported_after_read | 1 | 0.00 |
| f1_drill_to_nested_config | 4 | 0.75 |
| f1_search_read_follow_ref | 4 | 0.25 |
| f2_file_missing_list_parent | 3 | 0.67 |
| f2_search_miss_refine | 3 | 0.00 |
| f3_empty_index_abort | 1 | 0.00 |
| f3_file_gone_twice | 1 | 0.00 |
| f3_size_in_listing | 1 | 1.00 |
| f4_add_yaml_entry | 3 | 0.33 |
| f4_edit_toml_timeout | 3 | 0.67 |
| f5_check_permissions | 3 | 1.00 |
| f5_largest_file_mtime | 3 | 1.00 |
| f6_paginated_access_log | 2 | 1.00 |
| f6_specific_range | 2 | 0.00 |
| f7_wrong_env_correction | 2 | 0.50 |
| f7_wrong_folder_redirect | 2 | 1.00 |
| f8_write_bytes_from_history | 1 | 1.00 |
| f8_write_readback | 3 | 0.67 |
| new_ambiguous_mid_chain | 2 | 0.50 |
| new_ask_about_second_chunk | 1 | 1.00 |
| new_cannot_execute | 1 | 0.00 |
| new_conditional_age_check | 2 | 1.00 |
| new_greeting_no_action | 1 | 1.00 |
| new_infer_from_context | 1 | 1.00 |
| new_read_then_search_correct_value | 3 | 0.33 |
| new_search_then_save | 3 | 0.67 |
| new_stat_to_distinguish_type | 2 | 1.00 |
| new_two_requests_one_msg | 3 | 0.67 |
| new_unsupported_operation | 1 | 1.00 |
| new_user_changes_mind | 2 | 0.50 |
| new_write_then_search | 3 | 0.67 |

Failures (first 12):

- `test_hand8-001` f1_drill_to_nested_config: fails args  | "somewhere inside platform/ there's a redis.conf, find it and show me what's inside" -> '{"name": "fs_list", "arguments": {"path": "platform/"}}'
- `test_hand8-004` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'To proceed, I need to know the path where the logging policy file is located or its name. Could you provide me with the path or the name of '
- `test_hand8-005` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'Our logging policy is documented in the file `ops/logging-policy.md`. According to the document, all services must log to stdout in JSON for'
- `test_hand8-006` f1_search_read_follow_ref: fails json no call | 'look up our logging policy and follow any file it references' -> 'Here is the logging policy:\n\n# Logging Policy\n\nAll services log to stdout in JSON.\nFields: see ops/log-schema.json.\nRetention: 14 days in Lo'
- `test_hand8-009` f2_file_missing_list_parent: fails json no call | 'read the runbook at ops/incident-runbook.md' -> 'It seems the file `ops/incident-runbook.md` does not exist in the sandboxed file tree. Please double-check the file path or provide the corr'
- `test_hand8-011` f2_search_miss_refine: fails tool  | "what's the WAL mode setting for our database?" -> '{"name": "fs_list", "arguments": {"path": "./db_config"}}'
- `test_hand8-012` f2_search_miss_refine: fails json no call | "what's the WAL mode setting for our database?" -> 'The information provided does not directly state the WAL mode setting for your database. However, it defines WAL (Write-Ahead Logging) as a '
- `test_hand8-013` f2_search_miss_refine: reply lacks the tool's fact | "what's the WAL mode setting for our database?" -> 'The WAL mode setting for your database is set to `WAL` as specified in the `db-init.sql` configuration file with the following PRAGMA statem'
- `test_hand8-014` f3_empty_index_abort: called '{"name": "crag_search", "arguments": {"query": "backup procedures", "k": 5}}' | 'search for backup procedures then'
- `test_hand8-015` f3_file_gone_twice: called '{"name": "fs_read", "arguments": {"path": "inventory/stock.csv"}}' | 'hmm, try reading inventory/stock.csv one more time'
- `test_hand8-017` f4_edit_toml_timeout: fails tool  | 'the connection_timeout in network/client.toml is 10, bump it to 60' -> '{"name": "fs_stat", "arguments": {"path": "network/client.toml"}}'
- `test_hand8-020` f4_add_yaml_entry: fails args  | 'add "numpy" to the dependencies list in env/requirements.yaml' -> '{"name": "fs_read", "arguments": {"path": "env/requirements.yaml", "offset": 1, "limit": 1000}}'
