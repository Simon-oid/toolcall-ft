# askdocs eval report

askdocs `v0.1.0-21-g2966bb9`; corpus: cMCP cdb8852, cRAG a3d4815, embedder mxbai-embed-large; answer model: `local` at http://localhost:8081/v1; judge: `qwen2.5-7b-instruct-q4_k_m`; top_k 5; run 2026-11-25 05:11.

Means with bootstrap 95% intervals (10,000 resamples of the cases, seed 20261109).

| Metric | Mean [95% CI] | n |
|---|---|---|
| Retrieval recall@1 (answerable) | 0.57 [0.43, 0.70] | 43 |
| Retrieval recall@3 (answerable) | 0.85 [0.76, 0.93] | 43 |
| Retrieval recall@5 (answerable) | 0.92 [0.85, 0.98] | 43 |
| Retrieval recall@10 (answerable) | 0.94 [0.90, 0.99] | 43 |
| Context recall: right file among the passages the model got | 0.85 [0.76, 0.93] | 43 |
| Key-fact recall (answerable; refusal = 0) | 0.70 [0.57, 0.81] | 43 |
| Key facts present in the passages given (answerable) | 0.92 [0.86, 0.97] | 43 |
| Wrong refusal (answerable) | 0.05 [0.00, 0.12] | 43 |
| Correct refusal (unanswerable + off-topic) | 0.90 [0.70, 1.00] | 10 |
| Faithfulness: judged sentences supported (per answer) | 0.81 [0.70, 0.90] | 41 |
| Answers with an out-of-range citation | 0.00 [0.00, 0.00] | 53 |
| Answers citing nothing (answered, not refused) | 0.00 [0.00, 0.00] | 41 |
| Key-fact recall, factual only | 0.83 [0.70, 0.97] | 30 |
| Key-fact recall, multi only | 0.38 [0.19, 0.58] | 13 |

## Latency (informational: one client, sequential)

Nearest-rank percentiles. ttft and generation exist only for answers that
called the model (not for refusals with no passages).

| Stage | P50 ms | P95 ms | n |
|---|---|---|---|
| retrieval_ms | 14 | 16 | 53 |
| ttft_ms | 215 | 268 | 51 |
| generation_ms | 494 | 1475 | 51 |
| total_ms | 505 | 1490 | 53 |

## Tokens and cost per answer

| Per answer | P50 | P95 | n |
|---|---|---|---|
| prompt_tokens | 2014 | 2506 | 51 |
| completion_tokens | 43 | 202 | 51 |

No token prices set (ASKDOCS_LLM_PRICE_*_PER_MTOK): a local model's cost per answer is GPU time, the generation_ms above.

## Cases that missed something

- `f01` (factual): faithfulness 0.50
- `f05` (factual): faithfulness 0.50
- `f08` (factual): faithfulness 0.50
- `f09` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f13` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f15` (factual): key facts 0.00 (all in the passages: the model missed them); faithfulness 0.71
- `f16` (factual): faithfulness 0.00
- `f17` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f18` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f25` (factual): faithfulness 0.00
- `m01` (multi): faithfulness 0.67
- `m02` (multi): faithfulness 0.00
- `m03` (multi): key facts 0.00 (all in the passages: the model missed them); faithfulness 0.80
- `m04` (multi): key facts 0.00 (passages held 0.50); faithfulness 0.50
- `m05` (multi): key facts 0.50 (all in the passages: the model missed them); recall@5 0.50
- `m06` (multi): key facts 0.50 (all in the passages: the model missed them)
- `m07` (multi): refused; recall@5 0.50
- `m08` (multi): key facts 0.50 (passages held 0.50); faithfulness 0.50
- `m09` (multi): key facts 0.00 (passages held 0.50); faithfulness 0.40; recall@5 0.50
- `m10` (multi): refused; recall@5 0.50
- `m11` (multi): key facts 0.50 (passages held 0.50)
- `m12` (multi): key facts 0.50 (passages held 0.50); recall@5 0.50
- `m13` (multi): key facts 0.50 (passages held 0.50); faithfulness 0.00; recall@5 0.00
- `o04` (offtopic): answered an unanswerable question
