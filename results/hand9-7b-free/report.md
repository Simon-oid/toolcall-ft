# hand9-7b-free

model: Qwen/Qwen2.5-7B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 125

## test_hand9 (77 need a call, 48 need none, 48 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.883 [0.805, 0.948] |
| L1 json | 0.883 [0.805, 0.948] |
| L2 schema | 0.883 [0.805, 0.948] |
| L3 tool | 0.779 [0.688, 0.870] |
| L4 args | 0.532 [0.416, 0.636] |
| abstain | 0.729 [0.604, 0.854] |
| decision | 0.824 [0.752, 0.888] |
| step right | 0.608 [0.520, 0.696] |
| answer grounded | 0.825 [0.700, 0.925] |
| episode right | 0.292 [0.167, 0.417] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_clarify_path | 1 | 0.00 |
| base_clarify_save | 1 | 0.00 |
| base_coref_it | 2 | 1.00 |
| base_coref_second | 2 | 0.50 |
| base_impossible_delete | 1 | 0.00 |
| base_list_then_read | 3 | 1.00 |
| base_read_edit_write | 3 | 1.00 |
| base_search_then_save | 3 | 0.67 |
| base_thanks_after_stat | 2 | 1.00 |
| new_ambiguous_folder | 2 | 0.50 |
| new_compare_configs | 3 | 0.67 |
| new_dynamic_offset | 3 | 1.00 |
| new_impossible_exec | 2 | 0.00 |
| new_impossible_http | 2 | 0.00 |
| new_index_vs_dir | 3 | 1.00 |
| new_stat_branch_limit | 3 | 1.00 |
| new_verify_against_docs | 3 | 0.33 |
| r1_bm25_weights | 3 | 1.00 |
| r1_deploy_env | 4 | 0.50 |
| r1_ferry_sched | 6 | 0.17 |
| r1_greenhouse_cal | 4 | 0.50 |
| r1_lathe_chart | 5 | 0.80 |
| r1_march_water | 3 | 0.67 |
| r2_grace_window | 4 | 0.75 |
| r2_lease_ttl | 3 | 0.67 |
| r2_vacuum_cron | 2 | 1.00 |
| r2_warm_pool | 2 | 1.00 |
| r3_chunk_overlap | 2 | 1.00 |
| r3_rate_quota | 3 | 0.33 |
| r3_socket_keepalive | 5 | 0.60 |
| r4_backpressure | 2 | 0.50 |
| r4_prompt_cache | 2 | 0.50 |
| r4_retry_backoff | 2 | 1.00 |
| r4_schema_strict | 3 | 0.67 |
| r4_token_budget | 4 | 0.50 |
| r5_auth_timeout | 2 | 0.50 |
| r5_clinic_hours | 5 | 0.40 |
| r5_embed_params | 3 | 0.67 |
| r5_invoice_archive | 4 | 0.75 |
| r5_runbook_dir | 3 | 1.00 |
| stop_bm25_weights | 1 | 0.00 |
| stop_deploy_env | 1 | 0.00 |
| stop_greenhouse_cal | 1 | 0.00 |
| stop_lease_ttl | 2 | 0.00 |
| stop_march_water | 1 | 0.00 |
| stop_runbook_dir | 1 | 1.00 |
| stop_schema_strict | 2 | 0.50 |
| stop_vacuum_cron | 1 | 0.00 |

Failures (first 12):

- `test_hand9-001` r1_greenhouse_cal: fails json no call | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> 'It seems the file `greenhouse/sensor_cal.csv` does not exist. Could you please verify the file path or provide the correct path if `sensor_c'
- `test_hand9-002` r1_greenhouse_cal: fails json no call | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> 'It seems there is no `sensor_cal.csv` file in the `greenhouse` directory. The available files are `calibration_v2.csv` and `irrigation.txt`.'
- `test_hand9-005` r1_deploy_env: fails json no call | 'When was ops/cmcp.env last modified?' -> 'It seems that the file `ops/cmcp.env` does not exist in the sandboxed file tree. Please double-check the filename and the path, or provide m'
- `test_hand9-006` r1_deploy_env: fails json no call | 'When was ops/cmcp.env last modified?' -> 'It seems there is no file named `cmcp.env` in the `ops` directory. The available files are `cmcp_prod.env` and `systemd.service`. Could you '
- `test_hand9-009` r1_march_water: fails json no call | "Can you double-check inside the billing folder to see if it's really missing?" -> 'The folder `billing` contains `march_electric.txt` and `water_03.txt`, but not `march_water.txt`. Could you please specify another file or p'
- `test_hand9-014` r1_ferry_sched: fails tool  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_stat", "arguments": {"path": "trips/island.txt"}}'
- `test_hand9-015` r1_ferry_sched: fails args  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_read", "arguments": {"path": "trips/ferry_times.txt", "offset": 1}}'
- `test_hand9-016` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'It seems there was an issue locating the timetable file `trips/ferry_times.txt`. Could you please verify if the file path is correct or prov'
- `test_hand9-017` r1_ferry_sched: fails tool  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_read", "arguments": {"path": "trips/island.txt"}}'
- `test_hand9-018` r1_ferry_sched: fails args  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_read", "arguments": {"path": "trips/summer/ferry_times.txt", "offset": 1, "limit": 1}}'
- `test_hand9-021` r1_lathe_chart: fails tool  | 'Read workshop/lathe_speeds.csv and write the recommended RPM for brass into workshop/brass_rpm.txt.' -> '{"name": "fs_stat", "arguments": {"path": "workshop/lathe_speeds.csv"}}'
- `test_hand9-027` r2_lease_ttl: fails args  | 'Look up the worker lock duration in the docs; if "lock duration" finds nothing, try searching for lease.' -> '{"name": "crag_search", "arguments": {"query": "lock duration", "k": 5}}'
