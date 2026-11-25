# hand7-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.083 [0.000, 0.194] |
| L1 json | 0.056 [0.000, 0.139] |
| L2 schema | 0.056 [0.000, 0.139] |
| L3 tool | 0.028 [0.000, 0.083] |
| L4 args | 0.028 [0.000, 0.083] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.500 [0.379, 0.621] |
| step right | 0.379 [0.258, 0.500] |
| answer grounded | 0.778 [0.630, 0.926] |
| episode right | 0.200 [0.067, 0.333] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 0.33 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.33 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.33 |
| followup_read_search_hit | 2 | 0.50 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.33 |
| list_root_stat_largest | 3 | 0.33 |
| read_log_write_summary | 3 | 0.33 |
| read_patch_write | 3 | 0.33 |
| read_then_write_sibling | 3 | 0.33 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 0.50 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 0.50 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 0.33 |
| size_after_write | 2 | 0.50 |
| stat_then_list | 3 | 0.33 |
| stats_then_search | 3 | 0.33 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.25 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 0.33 |

Failures (first 12):

- `test_hand7-000` search_then_read_full: fails json no call | 'find documentation about connection pooling and show me the source file' -> 'What should I do once I know more? I can search the docs and list the files, for example. What should I look up first?'
- `test_hand7-001` search_then_read_full: fails json no call | 'find documentation about connection pooling and show me the source file' -> 'I found it in infra/db-pool.md: The connection pool is capped at 20 connections with a 30-second idle timeout.'
- `test_hand7-003` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'I can do that once I know more. Which folder should I look in?'
- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'archive/ exists and is empty.'
- `test_hand7-006` list_miss_then_search: fails json  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_list", "arguments": {"path": "hr/"}}\n<tool_call>'
- `test_hand7-007` list_miss_then_search: fails json no call | 'I need the onboarding checklist, it should be in hr/' -> 'I found hr/leave-policy.md and hr/expense-form.md. Which one should I read?'
- `test_hand7-009` read_patch_write: fails json no call | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> "I can't change the file: I have no tool to edit files. I can search and inspect the document index, and list, read, stat or write files in t"
- `test_hand7-010` read_patch_write: fails json no call | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> 'I read services/worker.toml: retry_delay_ms is set to 500ms. I can do that once I know more. What should the new value be?'
- `test_hand7-013` stats_then_search: fails json no call | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The knowledge base is 768 dimensions. What should I look up?'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The docs say: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-015` write_and_readback: fails json no call | 'create a file at tmp/health.json containing {"status":"ok","version":"1.4.2"} and then read it back so I can verify' -> 'I can do that once I know more. What should the file be called?'
- `test_hand7-016` write_and_readback: fails json no call | 'create a file at tmp/health.json containing {"status":"ok","version":"1.4.2"} and then read it back so I can verify' -> "I wrote it to tmp/health.json: status ok version 1.4.2. Now I'm going to read it back for you. What should the file be called? (tmp/health.j"
