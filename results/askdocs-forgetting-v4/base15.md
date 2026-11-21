# askdocs eval report

askdocs `v0.1.0-20-g2151741`; corpus: cMCP cdb8852, cRAG a3d4815, embedder mxbai-embed-large; answer model: `local` at http://localhost:8081/v1; judge: `qwen2.5-7b-instruct-q4_k_m`; top_k 5; run 2026-11-21 16:38.

Means with bootstrap 95% intervals (10,000 resamples of the cases, seed 20261109).

| Metric | Mean [95% CI] | n |
|---|---|---|
| Retrieval recall@1 (answerable) | 0.57 [0.43, 0.70] | 43 |
| Retrieval recall@3 (answerable) | 0.85 [0.76, 0.93] | 43 |
| Retrieval recall@5 (answerable) | 0.92 [0.85, 0.98] | 43 |
| Retrieval recall@10 (answerable) | 0.94 [0.90, 0.99] | 43 |
| Context recall: right file among the passages the model got | 0.85 [0.76, 0.93] | 43 |
| Key-fact recall (answerable; refusal = 0) | 0.49 [0.36, 0.62] | 43 |
| Key facts present in the passages given (answerable) | 0.92 [0.86, 0.97] | 43 |
| Wrong refusal (answerable) | 0.21 [0.09, 0.33] | 43 |
| Correct refusal (unanswerable + off-topic) | 1.00 [1.00, 1.00] | 10 |
| Faithfulness: judged sentences supported (per answer) | 0.79 [0.66, 0.90] | 34 |
| Answers with an out-of-range citation | 0.00 [0.00, 0.00] | 53 |
| Answers citing nothing (answered, not refused) | 0.00 [0.00, 0.00] | 34 |
| Key-fact recall, factual only | 0.57 [0.40, 0.73] | 30 |
| Key-fact recall, multi only | 0.31 [0.15, 0.50] | 13 |

## Latency (informational: one client, sequential)

Nearest-rank percentiles. ttft and generation exist only for answers that
called the model (not for refusals with no passages).

| Stage | P50 ms | P95 ms | n |
|---|---|---|---|
| retrieval_ms | 15 | 17 | 53 |
| ttft_ms | 220 | 509 | 51 |
| generation_ms | 385 | 1601 | 51 |
| total_ms | 398 | 1616 | 53 |

## Tokens and cost per answer

| Per answer | P50 | P95 | n |
|---|---|---|---|
| prompt_tokens | 2018 | 2491 | 51 |
| completion_tokens | 26 | 90 | 51 |

No token prices set (ASKDOCS_LLM_PRICE_*_PER_MTOK): a local model's cost per answer is GPU time, the generation_ms above.

## Cases that missed something

- `f01` (factual): refused
- `f05` (factual): faithfulness 0.00
- `f06` (factual): refused
- `f09` (factual): key facts 0.50 (all in the passages: the model missed them); faithfulness 0.00
- `f11` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f12` (factual): key facts 0.50 (all in the passages: the model missed them)
- `f13` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f14` (factual): faithfulness 0.00
- `f15` (factual): refused
- `f16` (factual): refused
- `f17` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f18` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f19` (factual): faithfulness 0.38
- `f20` (factual): key facts 0.50 (all in the passages: the model missed them)
- `f21` (factual): refused
- `f26` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f27` (factual): faithfulness 0.50
- `f28` (factual): key facts 0.00 (all in the passages: the model missed them)
- `f29` (factual): key facts 0.50 (all in the passages: the model missed them)
- `m01` (multi): key facts 0.50 (all in the passages: the model missed them)
- `m02` (multi): faithfulness 0.50
- `m03` (multi): refused
- `m04` (multi): key facts 0.00 (passages held 0.50); faithfulness 0.00
- `m05` (multi): refused; recall@5 0.50
- `m06` (multi): key facts 0.50 (all in the passages: the model missed them)
- `m07` (multi): key facts 0.00 (all in the passages: the model missed them); faithfulness 0.00; recall@5 0.50
- `m08` (multi): key facts 0.50 (passages held 0.50); faithfulness 0.67
- `m09` (multi): refused; recall@5 0.50
- `m10` (multi): refused; recall@5 0.50
- `m11` (multi): key facts 0.50 (passages held 0.50); faithfulness 0.67
- `m12` (multi): key facts 0.50 (passages held 0.50); recall@5 0.50
- `m13` (multi): key facts 0.50 (passages held 0.50); recall@5 0.00
