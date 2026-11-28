# hand9-1.5b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-1.5b-instruct-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 125

## test_hand9 (77 need a call, 48 need none, 48 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.649 [0.545, 0.753] |
| L1 json | 0.649 [0.545, 0.753] |
| L2 schema | 0.610 [0.506, 0.714] |
| L3 tool | 0.545 [0.442, 0.649] |
| L4 args | 0.377 [0.273, 0.494] |
| abstain | 0.812 [0.708, 0.917] |
| decision | 0.712 [0.632, 0.792] |
| step right | 0.520 [0.432, 0.608] |
| answer grounded | 0.775 [0.650, 0.900] |
| episode right | 0.208 [0.104, 0.333] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_clarify_path | 1 | 0.00 |
| base_clarify_save | 1 | 0.00 |
| base_coref_it | 2 | 1.00 |
| base_coref_second | 2 | 0.50 |
| base_impossible_delete | 1 | 0.00 |
| base_list_then_read | 3 | 0.67 |
| base_read_edit_write | 3 | 0.33 |
| base_search_then_save | 3 | 0.33 |
| base_thanks_after_stat | 2 | 1.00 |
| new_ambiguous_folder | 2 | 0.50 |
| new_compare_configs | 3 | 0.67 |
| new_dynamic_offset | 3 | 0.33 |
| new_impossible_exec | 2 | 1.00 |
| new_impossible_http | 2 | 1.00 |
| new_index_vs_dir | 3 | 0.33 |
| new_stat_branch_limit | 3 | 1.00 |
| new_verify_against_docs | 3 | 0.00 |
| r1_bm25_weights | 3 | 0.33 |
| r1_deploy_env | 4 | 0.50 |
| r1_ferry_sched | 6 | 0.33 |
| r1_greenhouse_cal | 4 | 0.25 |
| r1_lathe_chart | 5 | 0.80 |
| r1_march_water | 3 | 0.67 |
| r2_grace_window | 4 | 0.50 |
| r2_lease_ttl | 3 | 0.67 |
| r2_vacuum_cron | 2 | 1.00 |
| r2_warm_pool | 2 | 1.00 |
| r3_chunk_overlap | 2 | 1.00 |
| r3_rate_quota | 3 | 0.33 |
| r3_socket_keepalive | 5 | 0.40 |
| r4_backpressure | 2 | 0.50 |
| r4_prompt_cache | 2 | 0.50 |
| r4_retry_backoff | 2 | 0.50 |
| r4_schema_strict | 3 | 0.67 |
| r4_token_budget | 4 | 0.50 |
| r5_auth_timeout | 2 | 0.50 |
| r5_clinic_hours | 5 | 0.60 |
| r5_embed_params | 3 | 0.67 |
| r5_invoice_archive | 4 | 0.25 |
| r5_runbook_dir | 3 | 0.67 |
| stop_bm25_weights | 1 | 0.00 |
| stop_deploy_env | 1 | 0.00 |
| stop_greenhouse_cal | 1 | 0.00 |
| stop_lease_ttl | 2 | 0.00 |
| stop_march_water | 1 | 0.00 |
| stop_runbook_dir | 1 | 1.00 |
| stop_schema_strict | 2 | 1.00 |
| stop_vacuum_cron | 1 | 0.00 |

Failures (first 12):

- `test_hand9-000` r1_greenhouse_cal: fails args  | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> '{"name": "fs_read", "arguments": {"path": "greenhouse/sensor_cal.csv", "offset": 1, "limit": 1}}'
- `test_hand9-001` r1_greenhouse_cal: fails json no call | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> 'The file `greenhouse/sensor_cal.csv` does not exist in the specified directory. Please check the file path and try again.'
- `test_hand9-002` r1_greenhouse_cal: fails json no call | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> "I found two files in the 'greenhouse' directory: 'calibration_v2.csv' and 'irrigation.txt'. Could you please specify which one you're referr"
- `test_hand9-005` r1_deploy_env: fails json no call | 'When was ops/cmcp.env last modified?' -> "The file 'ops/cmcp.env' does not exist in the current directory. Could you please provide the correct path to the file?"
- `test_hand9-006` r1_deploy_env: fails json no call | 'When was ops/cmcp.env last modified?' -> "I'm sorry, but the file `ops/cmcp.env` does not exist in the directory `ops`. Could you please provide the correct path to the file?"
- `test_hand9-009` r1_march_water: fails json no call | "Can you double-check inside the billing folder to see if it's really missing?" -> "I found two files in the billing folder: march_electric.txt and water_03.txt. Let's check if water_03.txt contains the account number."
- `test_hand9-011` r1_bm25_weights: fails tool  | 'Double-check crag/ in case the filename changed slightly.' -> '{"name": "fs_read", "arguments": {"path": "crag/"}}'
- `test_hand9-012` r1_bm25_weights: fails json no call | 'Double-check crag/ in case the filename changed slightly.' -> "The file you're looking for is named `pipeline.cfg`. Let's check the `bm25_params.json` file to see which weights file it uses."
- `test_hand9-015` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'The ferry uses Pier 4. The first morning departure from the timetable file it names is at 06:00.'
- `test_hand9-016` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'The ferry timetable file "trips/ferry_times.txt" does not exist. Please check the spelling and try again.'
- `test_hand9-017` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'The ferry uses Pier 4. The first morning departure from the timetable file it names is in the file `trips/island.txt`.'
- `test_hand9-018` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'The ferry uses Pier 4. The first morning departure from the timetable file it names is in ferry_times.txt.'
