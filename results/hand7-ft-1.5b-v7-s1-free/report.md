# hand7-ft-1.5b-v7-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v7-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-37-g44a2dba · date: 2026-11-26 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.917 [0.806, 1.000] |
| L1 json | 0.917 [0.806, 1.000] |
| L2 schema | 0.917 [0.806, 1.000] |
| L3 tool | 0.806 [0.667, 0.917] |
| L4 args | 0.694 [0.528, 0.833] |
| abstain | 0.933 [0.833, 1.000] |
| decision | 0.924 [0.848, 0.985] |
| step right | 0.758 [0.652, 0.864] |
| answer grounded | 0.815 [0.667, 0.963] |
| episode right | 0.533 [0.367, 0.700] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 1.00 |
| answer_in_history | 1 | 1.00 |
| compare_envs | 3 | 1.00 |
| count_from_listing | 1 | 0.00 |
| double_search_refine | 3 | 0.67 |
| empty_index_no_search | 1 | 1.00 |
| error_in_history | 1 | 0.00 |
| fix_dockerfile_base | 3 | 1.00 |
| followup_read_search_hit | 2 | 1.00 |
| general_knowledge | 1 | 1.00 |
| list_miss_then_search | 3 | 0.67 |
| list_root_stat_largest | 3 | 0.67 |
| read_log_write_summary | 3 | 0.67 |
| read_patch_write | 3 | 1.00 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 0.50 |
| stat_then_list | 3 | 0.67 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.75 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-003` stat_then_list: fails tool  | "check if the archive/ directory exists and what's in it" -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_list", "arguments": {"path": "hr/templates"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The docs say: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-019` three_level_drill: fails args  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_list", "arguments": {"path": "api/v1"}}'
- `test_hand7-023` double_search_refine: fails tool  | 'find the CI pipeline timeout setting' -> '{"name": "fs_read", "arguments": {"path": "docs/faq.md"}}'
- `test_hand7-029` read_log_write_summary: fails args  | 'read lines 1 to 10 of logs/deploy.log and save a one-line summary to logs/deploy-summary.txt' -> '{"name": "fs_write", "arguments": {"path": "logs/deploy-summary.txt", "content": "deploy complete, total time: 41s\\nnotifying #releases chan'
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I can't find the documentation: our search engine is down."
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The docs say: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
- `test_hand7-035` list_root_stat_largest: fails args  | 'show me the top-level directory, then get the size of the biggest file' -> '{"name": "fs_stat", "arguments": {"path": "data"}}'
- `test_hand7-041` search_dead_end: fails tool  | 'find information about GPU sharding strategy in the docs' -> '{"name": "fs_read", "arguments": {"path": "misc/glossary.md"}}'
- `test_hand7-042` search_dead_end: called '{"name": "crag_search", "arguments": {"query": "model parallel shard device"}}' | 'find information about GPU sharding strategy in the docs'
- `test_hand7-052` size_after_write: fails json no call | 'how big is it?' -> 'notes/standup.md: 56 bytes.'
