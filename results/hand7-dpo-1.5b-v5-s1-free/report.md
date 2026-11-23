# hand7-dpo-1.5b-v5-s1-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo-1.5b-v5-s1-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-24-g2a0ff32 · date: 2026-11-23 · cases: 66

## test_hand7 (36 need a call, 30 need none, 30 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.778 [0.639, 0.917] |
| L1 json | 0.750 [0.611, 0.889] |
| L2 schema | 0.750 [0.611, 0.889] |
| L3 tool | 0.694 [0.528, 0.833] |
| L4 args | 0.694 [0.528, 0.833] |
| abstain | 0.967 [0.900, 1.000] |
| decision | 0.864 [0.773, 0.939] |
| step right | 0.742 [0.636, 0.848] |
| answer grounded | 0.778 [0.630, 0.926] |
| episode right | 0.567 [0.400, 0.733] |

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
| list_root_stat_largest | 3 | 1.00 |
| read_log_write_summary | 3 | 1.00 |
| read_patch_write | 3 | 0.67 |
| read_then_write_sibling | 3 | 0.67 |
| recall_value_from_read | 1 | 1.00 |
| resolve_ordinal_first | 2 | 1.00 |
| resolve_pronoun_it | 1 | 1.00 |
| same_dir_write | 2 | 1.00 |
| search_dead_end | 3 | 0.33 |
| search_related_topic | 2 | 1.00 |
| search_then_deep_read | 3 | 0.33 |
| search_then_read_full | 3 | 1.00 |
| size_after_write | 2 | 1.00 |
| stat_then_list | 3 | 0.67 |
| stats_then_search | 3 | 0.67 |
| thanks_done | 1 | 1.00 |
| three_level_drill | 4 | 0.50 |
| user_corrects_model | 1 | 1.00 |
| write_and_readback | 3 | 1.00 |

Failures (first 12):

- `test_hand7-004` stat_then_list: fails json no call | "check if the archive/ directory exists and what's in it" -> 'archive is empty.'
- `test_hand7-007` list_miss_then_search: fails tool  | 'I need the onboarding checklist, it should be in hr/' -> '{"name": "fs_read", "arguments": {"path": "hr/leave-policy.md"}}'
- `test_hand7-009` read_patch_write: fails json no call | 'the retry delay in services/worker.toml is 500ms, change it to 2000ms' -> 'I can do that once I know more. Which file should I edit?'
- `test_hand7-014` stats_then_search: reply lacks the tool's fact | 'how big is the knowledge base? then look up anything about TLS certificates' -> "Here's what I found in ops/tls-rotation.md: Certificates are rotated every 90 days using cert-manager. Wildcard certs cover *.app.internal."
- `test_hand7-019` three_level_drill: fails tool  | 'find the error codes table somewhere inside api/' -> '{"name": "fs_read", "arguments": {"path": "api/v1/error_codes.txt"}}'
- `test_hand7-020` three_level_drill: fails json no call | 'find the error codes table somewhere inside api/' -> "The docs are in api/v2 now. I'll look at error-codes.md:"
- `test_hand7-023` double_search_refine: fails json no call | 'find the CI pipeline timeout setting' -> 'docs/faq.md says: Q: What CI do we use? A: GitHub Actions with self-hosted runners.'
- `test_hand7-031` search_then_deep_read: fails json no call | "what's our data retention policy?" -> "I can't check the document index to see what it contains: there is no tool for that. I can list and inspect files in the sandbox, though. Wh"
- `test_hand7-032` search_then_deep_read: fails json no call | "what's our data retention policy?" -> 'The docs say: User data is retained for 2 years after account closure. Anonymised analytics are kept indefinitely.'
- `test_hand7-037` fix_dockerfile_base: fails json no call | 'the Dockerfile uses python:3.9-slim as the base, update it to python:3.12-slim' -> 'I can do that once I know more. Which file should I edit?'
- `test_hand7-039` fix_dockerfile_base: reply lacks the tool's fact | 'the Dockerfile uses python:3.9-slim as the base, update it to python:3.12-slim' -> "The file has been updated to use python:3.12-slim as the base image. It's now:\n\nFROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nR"
- `test_hand7-041` search_dead_end: fails json no call | 'find information about GPU sharding strategy in the docs' -> 'From the index (misc/glossary.md): GPU: Graphics Processing Unit, used for parallel computation.'
