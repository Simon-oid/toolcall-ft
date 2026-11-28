# hand9-ft-1.5b-v7-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 125

## test_hand9 (77 need a call, 48 need none, 48 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.935 [0.870, 0.987] |
| L1 json | 0.935 [0.870, 0.987] |
| L2 schema | 0.935 [0.870, 0.987] |
| L3 tool | 0.857 [0.779, 0.935] |
| L4 args | 0.831 [0.740, 0.909] |
| abstain | 0.812 [0.688, 0.917] |
| decision | 0.888 [0.832, 0.936] |
| step right | 0.808 [0.736, 0.872] |
| answer grounded | 0.800 [0.675, 0.925] |
| episode right | 0.583 [0.438, 0.708] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| base_clarify_path | 1 | 1.00 |
| base_clarify_save | 1 | 1.00 |
| base_coref_it | 2 | 1.00 |
| base_coref_second | 2 | 1.00 |
| base_impossible_delete | 1 | 1.00 |
| base_list_then_read | 3 | 1.00 |
| base_read_edit_write | 3 | 1.00 |
| base_search_then_save | 3 | 1.00 |
| base_thanks_after_stat | 2 | 1.00 |
| new_ambiguous_folder | 2 | 0.50 |
| new_compare_configs | 3 | 1.00 |
| new_dynamic_offset | 3 | 0.67 |
| new_impossible_exec | 2 | 0.50 |
| new_impossible_http | 2 | 0.50 |
| new_index_vs_dir | 3 | 0.33 |
| new_stat_branch_limit | 3 | 1.00 |
| new_verify_against_docs | 3 | 0.67 |
| r1_bm25_weights | 3 | 1.00 |
| r1_deploy_env | 4 | 0.75 |
| r1_ferry_sched | 6 | 0.50 |
| r1_greenhouse_cal | 4 | 0.75 |
| r1_lathe_chart | 5 | 0.80 |
| r1_march_water | 3 | 1.00 |
| r2_grace_window | 4 | 0.75 |
| r2_lease_ttl | 3 | 1.00 |
| r2_vacuum_cron | 2 | 1.00 |
| r2_warm_pool | 2 | 1.00 |
| r3_chunk_overlap | 2 | 1.00 |
| r3_rate_quota | 3 | 0.67 |
| r3_socket_keepalive | 5 | 0.80 |
| r4_backpressure | 2 | 0.50 |
| r4_prompt_cache | 2 | 1.00 |
| r4_retry_backoff | 2 | 1.00 |
| r4_schema_strict | 3 | 1.00 |
| r4_token_budget | 4 | 1.00 |
| r5_auth_timeout | 2 | 1.00 |
| r5_clinic_hours | 5 | 0.60 |
| r5_embed_params | 3 | 0.67 |
| r5_invoice_archive | 4 | 1.00 |
| r5_runbook_dir | 3 | 1.00 |
| stop_bm25_weights | 1 | 0.00 |
| stop_deploy_env | 1 | 1.00 |
| stop_greenhouse_cal | 1 | 1.00 |
| stop_lease_ttl | 2 | 0.50 |
| stop_march_water | 1 | 0.00 |
| stop_runbook_dir | 1 | 1.00 |
| stop_schema_strict | 2 | 1.00 |
| stop_vacuum_cron | 1 | 0.00 |

Failures (first 12):

- `test_hand9-001` r1_greenhouse_cal: fails json no call | 'Check the frost warning threshold in greenhouse/sensor_cal.csv.' -> 'There is no file at greenhouse/sensor_cal.csv: it does not exist.'
- `test_hand9-005` r1_deploy_env: fails json no call | 'When was ops/cmcp.env last modified?' -> "ops/cmcp.env doesn't exist."
- `test_hand9-016` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'trips/island.txt points to a non-existent file, trips/ferry_times.txt.'
- `test_hand9-017` r1_ferry_sched: fails tool  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_read", "arguments": {"path": "trips/island.txt"}}'
- `test_hand9-019` r1_ferry_sched: reply lacks the tool's fact | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> 'The ferry departs at 10:15.'
- `test_hand9-021` r1_lathe_chart: fails json no call | 'Read workshop/lathe_speeds.csv and write the recommended RPM for brass into workshop/brass_rpm.txt.' -> 'There is no file at workshop/lathe_speeds.csv: it does not exist.'
- `test_hand9-031` r2_grace_window: fails tool  | 'Read app/alerts.conf to see which alert rule is configured, then check the docs for its cooldown (if cooldown finds nothing, try searching for debounce).' -> '{"name": "fs_read", "arguments": {"path": "docs/rules/disk_high.yaml"}}'
- `test_hand9-037` r3_rate_quota: fails json no call | 'Look up the per-client rate limit in the documentation.' -> 'From the index (docs/changelog.md, cos 0.520): v2.4 says: Per-client rate limits moved out of the HTTP section; search for "pacer" to find t'
- `test_hand9-043` r3_socket_keepalive: fails tool  | 'Read net/client.ini to find the transport protocol, then look up its probe interval in the docs and save the interval to net/probe.txt.' -> '{"name": "fs_write", "arguments": {"path": "net/probe.txt", "content": "10"}}'
- `test_hand9-050` r4_backpressure: called '{"name": "crag_search", "arguments": {"query": "backpressure queue cap"}}' | 'Check the documentation for the default backpressure queue cap when ingestion falls behind.'
- `test_hand9-063` r5_embed_params: fails tool  | "Check config/ for the embedding batch size setting; if there's no embedding config in that folder, look it up in the docs." -> '{"name": "fs_read", "arguments": {"path": "config/ports.yaml"}}'
- `test_hand9-070` r5_clinic_hours: fails tool  | 'Read clinic/notice.txt to see where the holiday hours are stored, then check what time the lab opens on Dec 26.' -> '{"name": "fs_read", "arguments": {"path": "clinic/schedules/holiday-schedules.txt"}}'
