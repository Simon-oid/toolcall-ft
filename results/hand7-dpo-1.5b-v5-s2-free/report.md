# hand7-dpo-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.889 [0.778, 0.972] |
| L1 json | 0.889 [0.778, 0.972] |
| L2 schema | 0.889 [0.778, 0.972] |
| L3 tool | 0.750 [0.611, 0.889] |
| L4 args | 0.722 [0.583, 0.861] |
| abstain | 0.900 [0.767, 1.000] |
| decision | 0.894 [0.818, 0.970] |
| step right | 0.712 [0.606, 0.818] |
| answer grounded | 0.704 [0.519, 0.852] |
| episode right | 0.500 [0.333, 0.667] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous_delete_which | 1 | 0.00 |
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
| read_log_write_summary | 3 | 1.00 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 1.00 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.00 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.67 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.75 |
| user_corrects_model | 1 | 0.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'archive is empty.'
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/leave-policy.md"}}'
- `test_hand7-009` read_patch_write: fails tool  | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> '{"name": "fs_write", "arguments": {"path": "services/worker.toml", "content": "retry_delay = 2000ms"}}'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> 'The docs say: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal.'
- `test_hand7-019` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_read", "arguments": {"path": "api/v1"}}'
- `test_hand7-023` double_search_refine: fails tool  | 'find the CI pipeline timeout setting' -> '{"name": "fs_read", "arguments": {"path": "docs/faq.md"}}'
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I can't check the documentation: there is no tool to look up the data retention policy. I can list and inspect the files in the sandbox, tho"
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The documentation says: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
- `test_hand7-033` search_then_deep_read: reply lacks the tool's fact | "what's our data retention policy?" -> 'The documentation says:\n\n- Personal data is deleted 2 years after account closure.\n- Anonymised analytics are kept indefinitely.\n- Backups a'
- `test_hand7-035` list_root_stat_largest: fails args  | 'show me the top-level directory, then get the size of the biggest file' -> '{"name": "fs_stat", "arguments": {"path": "data"}}'
- `test_hand7-037` fix_dockerfile_base: fails tool  | 'the Dockerfile uses python:3.9-slim as the base, update it to python:3.12-slim' -> '{"name": "fs_list", "arguments": {"path": "Dockerfiles"}}'
- `test_hand7-039` fix_dockerfile_base: reply lacks the tool's fact | 'the Dockerfile uses python:3.9-slim as the base, update it to python:3.12-slim' -> 'The file has been updated to:\n\nFROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['
