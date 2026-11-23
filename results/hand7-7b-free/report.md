# hand7-7b-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-22 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.806 [0.667, 0.917] |
| L1 json | 0.806 [0.667, 0.917] |
| L2 schema | 0.806 [0.667, 0.917] |
| L3 tool | 0.778 [0.639, 0.889] |
| L4 args | 0.556 [0.389, 0.722] |
| abstain | 0.900 [0.800, 1.000] |
| decision | 0.848 [0.758, 0.924] |
| step right | 0.636 [0.515, 0.742] |
| answer grounded | 0.704 [0.519, 0.852] |
| episode right | 0.467 [0.300, 0.633] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 1.00 |
| count_from_listing | 1 | 1.00 |
| double_search_refine | 3 | 0.33 |
| empty_index_no_search | 1 | 0.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 0.67 |
| followup_read_search_hit | 2 | 1.00 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.33 |
| list_root_stat_largest | 3 | 0.67 |
| read_log_write_summary | 3 | 1.00 |
| read_patch_write | 3 | 1.00 |
| read_then_write_sibling | 3 | 0.67 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.00 |
| search_related_topic | 2 | 0.50 |
| search_then_deep_read | 3 | 0.00 |
| search_then_read_full | 3 | 0.33 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.67 |
| stats_then_search | 3 | 0.33 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.75 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-000` search_then_read_full: fails args  | 'find documentation about connection pooling and show me the source file' -> '{"name": "crag_search", "arguments": {"k": 5, "query": "connection pooling"}}'
- `test_hand7-001` search_then_read_full: fails json no call | 'find documentation about connection pooling and show me the source file' -> 'The connection pool is described in the file `infra/db-pool.md`. According to the document, the connection pool is capped at 20 connections '
- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'The `archive/` directory exists but it is currently empty. Would you like to list the contents of a different directory or perform another a'
- `test_hand7-006` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/onboarding-checklist", "offset": 1, "limit": 1000}}'
- `test_hand7-007` list_miss_then_search: fails json no call | 'I need the onboarding checklist, it should be in hr/' -> 'The directory `hr` contains `leave-policy.md` and `expense-form.md`, but no onboarding checklist was found. Would you like to create a new f'
- `test_hand7-013` stats_then_search: fails args  | 'how big is the knowledge base? then look up anything about TLS certificates' -> '{"name": "crag_search", "arguments": {"query": "TLS certificates", "k": 5}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The knowledge base contains 2,860 chunks and 74 files, with each chunk having a dimension of 768.\n\nFrom the search results, it appears that '
- `test_hand7-019` three_level_drill: fails args  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_list", "arguments": {"path": "api/v1"}}'
- `test_hand7-022` double_search_refine: fails args  | 'find the CI pipeline timeout setting' -> '{"name": "crag_search", "arguments": {"query": "CI pipeline timeout setting", "k": 5}}'
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'The search results did not directly mention the CI pipeline timeout setting. The document "faq.md" discussed using GitHub Actions but did no'
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I don't have information about your specific data retention policy. This would typically be defined by the policies or guidelines of your or"
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'Our data retention policy states that user data is retained for 2 years after account closure. Anonymized analytics are kept indefinitely.'
