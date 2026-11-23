# hand7-ft-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.861 [0.750, 0.972] |
| L1 json | 0.833 [0.694, 0.944] |
| L2 schema | 0.833 [0.694, 0.944] |
| L3 tool | 0.722 [0.583, 0.861] |
| L4 args | 0.694 [0.528, 0.833] |
| abstain | 0.933 [0.833, 1.000] |
| decision | 0.894 [0.818, 0.955] |
| step right | 0.667 [0.545, 0.773] |
| answer grounded | 0.593 [0.407, 0.778] |
| episode right | 0.500 [0.333, 0.667] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 1.00 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.67 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.33 |
| followup_read_search_hit | 2 | 1.00 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.67 |
| list_root_stat_largest | 3 | 0.67 |
| read_log_write_summary | 3 | 0.67 |
| read_patch_write | 3 | 0.33 |
| read_then_write_sibling | 3 | 0.33 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.00 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 1.00 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.50 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/leave-policy.md"}}'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "fs_write", "arguments": {"path": "services/worker.toml", "content": "retry_delay = 2000ms"}}'
- `test_hand7-011` read_patch_write: reply lacks the tool's fact | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> 'Done: I saved it to services/worker.toml.'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> "Here's what I found in ops/tls-rotation.md: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal."
- `test_hand7-019` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_read", "arguments": {"path": "api/error_codes"}}'
- `test_hand7-020` three_level_drill: fails json no call | 'find the error codes table somewhere inside api/' -> 'The docs are in api/v2: I found error-codes.md.'
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'The docs say: Q: What CI do we use? A: GitHub Actions with self-hosted runners.'
- `test_hand7-030` read_log_write_summary: reply lacks the tool's fact | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> 'Saved to logs/deploy-summary.txt.'
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I can't check the document index: it doesn't have a tool to do that. I can list, read, stat or write files in the sandbox, though."
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The docs say: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
- `test_hand7-033` search_then_deep_read: reply lacks the tool's fact | "what's our data retention policy?" -> 'The policy is in compliance/data-lifecycle.md.'
- `test_hand7-035` list_root_stat_largest: fails args  | 'show me the top-level directory, then get the size of the biggest file' -> '{"name": "fs_stat", "arguments": {"path": "data"}}'
