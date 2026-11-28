# hand7-ft-1.5b-v8-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: ft-1.5b-v8-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-46-ge8e577d · date: 2026-11-28 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.944 [0.861, 1.000] |
| L1 json | 0.944 [0.861, 1.000] |
| L2 schema | 0.944 [0.861, 1.000] |
| L3 tool | 0.861 [0.750, 0.972] |
| L4 args | 0.750 [0.611, 0.889] |
| abstain | 0.933 [0.833, 1.000] |
| decision | 0.939 [0.879, 0.985] |
| step right | 0.758 [0.652, 0.864] |
| answer grounded | 0.778 [0.630, 0.926] |
| episode right | 0.533 [0.367, 0.700] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 0.00 |
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
| read_log_write_summary | 3 | 1.00 |
| read_patch_write | 3 | 1.00 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 0.50 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.67 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 0.50 |
| stat_then_list | 3 | 0.33 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.75 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-003` stat_then_list: fails tool  | "check if the archive/ directory exists and what's in it" -> '{"name": "fs_list", "arguments": {"path": "archive"}}'
- `test_hand7-005` stat_then_list: reply lacks the tool's fact | "check if the archive/ directory exists and what's in it" -> 'archive is a directory. Here it is: logs.'
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_list", "arguments": {"path": "hr/templates"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'According to ops/tls-rotation.md: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-019` three_level_drill: fails args  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_list", "arguments": {"path": "api/v1"}}'
- `test_hand7-023` double_search_refine: fails args  | 'find the CI pipeline timeout setting' -> '{"name": "crag_search", "arguments": {"query": "GitHub Actions"}}'
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The docs say: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
- `test_hand7-035` list_root_stat_largest: fails tool  | 'show me the top-level directory, then get the size of the biggest file' -> '{"name": "fs_list", "arguments": {"path": "src"}}'
- `test_hand7-041` search_dead_end: fails args  | 'find information about GPU sharding strategy in the docs' -> '{"name": "crag_search", "arguments": {"query": "parallel computation"}}'
- `test_hand7-042` search_dead_end: reply lacks the tool's fact | 'find information about GPU sharding strategy in the docs' -> 'According to misc/glossary.md: GPU is the Graphics Processing Unit, used for parallel computation.'
- `test_hand7-052` size_after_write: fails json no call | 'how big is it?' -> 'notes/standup.md: 56 bytes.'
- `test_hand7-056` error_in_history: reply lacks the tool's fact | 'can you try a different query maybe?' -> "I can't rebuild the index: it's still in use by the search tool."
