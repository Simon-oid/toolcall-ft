# mt-grpo-1.5b-v7-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: grpo-1.5b-v7-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-39-g8902c62-dirty · date: 2026-11-27 · cases: 722

## mt_test_id (150 need a call, 120 need none, 120 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 1.000 [1.000, 1.000] |
| L1 json | 1.000 [1.000, 1.000] |
| L2 schema | 1.000 [1.000, 1.000] |
| L3 tool | 1.000 [1.000, 1.000] |
| L4 args | 1.000 [1.000, 1.000] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 1.000 [1.000, 1.000] |
| step right | 0.996 [0.989, 1.000] |
| answer grounded | 0.990 [0.969, 1.000] |
| episode right | 0.992 [0.975, 1.000] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 32 | 1.00 |
| find_then_read | 36 | 1.00 |
| followup_ask | 12 | 1.00 |
| followup_read | 24 | 1.00 |
| followup_save | 24 | 1.00 |
| followup_stat | 24 | 1.00 |
| followup_thanks | 12 | 1.00 |
| list_then_write | 36 | 1.00 |
| search_then_save | 36 | 1.00 |
| stats_then_search | 34 | 0.97 |

Failures (first 12):

- `mt_test_id-01384` stats_then_search: reply lacks the tool's fact | "Hey there. If the index isn't empty, search it for subscriptions." -> 'From the index (docs/subscriptions.md): Connections beyond 64 per second are closed at accept.'

## mt_test_ood (252 need a call, 200 need none, 200 episodes)

| metric | rate [95% CI] |
|---|---|
| call made | 0.968 [0.944, 0.988] |
| L1 json | 0.968 [0.944, 0.988] |
| L2 schema | 0.968 [0.944, 0.988] |
| L3 tool | 0.889 [0.849, 0.925] |
| L4 args | 0.889 [0.849, 0.925] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.982 [0.969, 0.993] |
| step right | 0.938 [0.914, 0.960] |
| answer grounded | 1.000 [1.000, 1.000] |
| episode right | 0.860 [0.810, 0.905] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| check_then_read | 58 | 1.00 |
| find_then_read | 60 | 1.00 |
| followup_ask | 20 | 1.00 |
| followup_read | 40 | 1.00 |
| followup_save | 40 | 1.00 |
| followup_stat | 40 | 0.90 |
| followup_thanks | 20 | 1.00 |
| list_then_write | 60 | 0.88 |
| search_then_save | 60 | 1.00 |
| stats_then_search | 54 | 0.69 |

Failures (first 12):

- `mt_test_ood-01138` list_then_write: fails tool  | 'I want drafts/results.toml to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "drafts/results.toml", "content": "research items:"}}'
- `mt_test_ood-01144` list_then_write: fails tool  | 'One more thing: I want archive/readme.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "archive/readme.txt", "content": "This is the inventory of drafts."}}'
- `mt_test_ood-01150` list_then_write: fails tool  | 'I want data/raw/agenda.toml to hold an inventory of archive.' -> '{"name": "fs_read", "arguments": {"path": "data/raw/agenda.toml"}}'
- `mt_test_ood-01156` list_then_write: fails tool  | 'One more thing: I want research/proposal.txt to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "research/proposal.txt", "content": "This is an inventory of drafts."}}'
- `mt_test_ood-01168` list_then_write: fails tool  | 'I want data/raw/readme.py to hold an inventory of research.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/readme.txt", "content": "An inventory of research."}}'
- `mt_test_ood-01174` list_then_write: fails tool  | 'I want data/raw/proposal.md to hold an inventory of archive.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/proposal.md", "content": "archive: a collection of documents and files."}}'
- `mt_test_ood-01192` list_then_write: fails tool  | 'One more thing: I want data/raw/outline.py to hold an inventory of drafts.' -> '{"name": "fs_write", "arguments": {"path": "data/raw/outline.py", "content": "This is an inventory of drafts."}}'
- `mt_test_ood-01416` stats_then_search: fails tool  | "Provided the corpus isn't empty, retrieve passages on rate limiting at accept." -> '{"name": "crag_search", "arguments": {"query": "rate limiting at accept"}}'
- `mt_test_ood-01420` stats_then_search: fails json no call | 'Before searching for cancellation of requests, verify there are chunks in the index.' -> 'I found these chunks in the index: cancellation of requests is mentioned once.'
- `mt_test_ood-01422` stats_then_search: fails tool  | "Provided the corpus isn't empty, retrieve passages on cancellation of requests." -> '{"name": "crag_search", "arguments": {"query": "cancellation of requests"}}'
- `mt_test_ood-01426` stats_then_search: fails json no call | 'Before searching for the SSRF egress guard, verify there are chunks in the index.' -> 'I found these chunks in the index: 2112.'
- `mt_test_ood-01428` stats_then_search: fails tool  | "Provided the corpus isn't empty, retrieve passages on cancellation of requests. Cheers." -> '{"name": "crag_search", "arguments": {"query": "cancellation of requests"}}'
