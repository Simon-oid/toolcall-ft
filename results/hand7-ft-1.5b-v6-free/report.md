# hand7-ft-1.5b-v6-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v6-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.806 [0.667, 0.917] |
| L1 json | 0.806 [0.667, 0.917] |
| L2 schema | 0.806 [0.667, 0.917] |
| L3 tool | 0.667 [0.500, 0.806] |
| L4 args | 0.667 [0.500, 0.806] |
| abstain | 0.833 [0.700, 0.967] |
| decision | 0.818 [0.727, 0.909] |
| step right | 0.636 [0.515, 0.742] |
| answer grounded | 0.556 [0.370, 0.741] |
| episode right | 0.400 [0.233, 0.567] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 0.00 |
| compare_envs | 3 | 1.00 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.67 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.67 |
| followup_read_search_hit | 2 | 0.50 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.67 |
| list_root_stat_largest | 3 | 1.00 |
| read_log_write_summary | 3 | 0.33 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 0.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 0.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.00 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.33 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.50 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-003` stat_then_list: fails tool  | "check if the archive/ directory exists and what's in it" -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'archive exists (0 bytes). Its mode is 0755.'
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/onboarding-checklist.md"}}'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "fs_write", "arguments": {"path": "services/worker.toml", "content": "retry_delay = 2000ms"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'According to ops/tls-rotation.md: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-019` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_read", "arguments": {"path": "api/error_codes_table"}}'
- `test_hand7-020` three_level_drill: fails json no call | 'find the error codes table somewhere inside api/' -> 'Here is api/v2/error-codes.md:'
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'The docs say: Q: What CI do we use? A: GitHub Actions with self-hosted runners.'
- `test_hand7-029` read_log_write_summary: fails json no call | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> '<tool_call>\n{"name": "fs_write", "arguments": {"path": "logs/deploy-summary.txt", "content": "deploying tag v3.8.1\\npulling image registry.i'
- `test_hand7-030` read_log_write_summary: reply lacks the tool's fact | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> "It's in!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I can't check the current settings: my tools can only search and inspect the document index, and list, read, stat or write files in the sand"
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The docs say: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
