# hand9-ft-1.5b-v8-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 125

## test_hand9 (77 need a call, 48 need none, 48 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.987 [0.961, 1.000] |
| L1 json | 0.987 [0.961, 1.000] |
| L2 schema | 0.987 [0.961, 1.000] |
| L3 tool | 0.961 [0.909, 1.000] |
| L4 args | 0.909 [0.844, 0.961] |
| abstain | 0.792 [0.667, 0.896] |
| decision | 0.912 [0.856, 0.960] |
| step right | 0.864 [0.800, 0.920] |
| answer grounded | 0.850 [0.725, 0.950] |
| episode right | 0.688 [0.562, 0.812] |

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
| r1_deploy_env | 4 | 1.00 |
| r1_ferry_sched | 6 | 0.67 |
| r1_greenhouse_cal | 4 | 1.00 |
| r1_lathe_chart | 5 | 1.00 |
| r1_march_water | 3 | 1.00 |
| r2_grace_window | 4 | 1.00 |
| r2_lease_ttl | 3 | 1.00 |
| r2_vacuum_cron | 2 | 1.00 |
| r2_warm_pool | 2 | 1.00 |
| r3_chunk_overlap | 2 | 1.00 |
| r3_rate_quota | 3 | 1.00 |
| r3_socket_keepalive | 5 | 0.80 |
| r4_backpressure | 2 | 0.50 |
| r4_prompt_cache | 2 | 1.00 |
| r4_retry_backoff | 2 | 1.00 |
| r4_schema_strict | 3 | 1.00 |
| r4_token_budget | 4 | 1.00 |
| r5_auth_timeout | 2 | 1.00 |
| r5_clinic_hours | 5 | 0.80 |
| r5_embed_params | 3 | 0.67 |
| r5_invoice_archive | 4 | 1.00 |
| r5_runbook_dir | 3 | 1.00 |
| stop_bm25_weights | 1 | 0.00 |
| stop_deploy_env | 1 | 1.00 |
| stop_greenhouse_cal | 1 | 1.00 |
| stop_lease_ttl | 2 | 0.50 |
| stop_march_water | 1 | 0.00 |
| stop_runbook_dir | 1 | 0.00 |
| stop_schema_strict | 2 | 1.00 |
| stop_vacuum_cron | 1 | 1.00 |

Failures (first 12):

- `test_hand9-016` r1_ferry_sched: fails json no call | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> "trips/island.txt doesn't have it: trips/ferry_times.txt isn't there."
- `test_hand9-017` r1_ferry_sched: fails args  | 'Check trips/island.txt for which pier the ferry uses, and get the first morning departure from the timetable file it names.' -> '{"name": "fs_list", "arguments": {"path": "trips/island.txt"}}'
- `test_hand9-042` r3_socket_keepalive: fails args  | 'Read net/client.ini to find the transport protocol, then look up its probe interval in the docs and save the interval to net/probe.txt.' -> '{"name": "crag_search", "arguments": {"query": "the probe interval"}}'
- `test_hand9-050` r4_backpressure: called '{"name": "crag_search", "arguments": {"query": "backpressure queue cap"}}' | 'Check the documentation for the default backpressure queue cap when ingestion falls behind.'
- `test_hand9-063` r5_embed_params: fails tool  | "Check config/ for the embedding batch size setting; if there's no embedding config in that folder, look it up in the docs." -> '{"name": "fs_stat", "arguments": {"path": "config/embedding"}}'
- `test_hand9-070` r5_clinic_hours: fails tool  | 'Read clinic/notice.txt to see where the holiday hours are stored, then check what time the lab opens on Dec 26.' -> '{"name": "crag_search", "arguments": {"query": "the lab opens on Dec 26"}}'
- `test_hand9-078` stop_march_water: called '{"name": "fs_list", "arguments": {"path": "billing"}}' | "Can you double-check inside the billing folder to see if it's really missing?"
- `test_hand9-079` stop_bm25_weights: called '{"name": "fs_list", "arguments": {"path": "crag"}}' | 'Double-check crag/ in case the filename changed slightly.'
- `test_hand9-082` stop_lease_ttl: called '{"name": "crag_search", "arguments": {"query": "lease"}}' | 'Look up the worker lock duration in the docs; if "lock duration" finds nothing, try searching for lease.'
- `test_hand9-085` stop_runbook_dir: called '{"name": "fs_list", "arguments": {"path": "runbooks/legacy"}}' | "Never mind, skip it — we're rewriting the runbook anyway."
- `test_hand9-093` new_index_vs_dir: fails args  | "First run crag_stats to get the indexed chunk count, then list the root workspace folder so we can see what's there." -> '{"name": "fs_list", "arguments": {"path": "workspace"}}'
- `test_hand9-094` new_index_vs_dir: called '{"name": "fs_list", "arguments": {"path": "docs"}}' | "First run crag_stats to get the indexed chunk count, then list the root workspace folder so we can see what's there."
