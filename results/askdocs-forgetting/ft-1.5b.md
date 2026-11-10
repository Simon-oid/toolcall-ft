# askdocs eval report

askdocs `1c934fc`; corpus: cMCP cdb8852, cRAG a3d4815, embedder mxbai-embed-large; answer model: `local` at http://localhost:8081/v1; judge: `qwen2.5-7b-instruct-q4_k_m`; top_k 5; run 2026-11-10 20:48.

Means with bootstrap 95% intervals (10,000 resamples of the cases, seed 20261109).

| Metric | Mean [95% CI] | n |
|---|---|---|
| Retrieval recall@1 (answerable) | 0.61 [0.46, 0.76] | 35 |
| Retrieval recall@3 (answerable) | 0.94 [0.87, 1.00] | 35 |
| Retrieval recall@5 (answerable) | 0.99 [0.96, 1.00] | 35 |
| Retrieval recall@10 (answerable) | 0.99 [0.96, 1.00] | 35 |
| Context recall: right file among the passages the model got | 0.94 [0.87, 1.00] | 35 |
| Key-fact recall (answerable; refusal = 0) | 0.76 [0.63, 0.89] | 35 |
| Wrong refusal (answerable) | 0.14 [0.03, 0.26] | 35 |
| Correct refusal (unanswerable + off-topic) | 1.00 [1.00, 1.00] | 10 |
| Faithfulness: judged sentences supported (per answer) | 0.07 [0.00, 0.15] | 30 |
| Answers with an out-of-range citation | 0.00 [0.00, 0.00] | 45 |
| Key-fact recall, factual only | 0.80 [0.67, 0.93] | 30 |
| Key-fact recall, multi only | 0.50 [0.20, 0.80] | 5 |

## Latency (informational: one client, sequential)

Nearest-rank percentiles. ttft and generation exist only for answers that
called the model (not for refusals with no passages).

| Stage | P50 ms | P95 ms | n |
|---|---|---|---|
| retrieval_ms | 16 | 17 | 45 |
| ttft_ms | 226 | 289 | 43 |
| generation_ms | 430 | 961 | 43 |
| total_ms | 422 | 978 | 45 |

## Tokens and cost per answer

| Per answer | P50 | P95 | n |
|---|---|---|---|
| prompt_tokens | 2016 | 2520 | 43 |
| completion_tokens | 36 | 117 | 43 |

No token prices set (ASKDOCS_LLM_PRICE_*_PER_MTOK): a local model's cost per answer is GPU time, the generation_ms above.

## Cases that missed something

- `f01` (factual): faithfulness 0.00
- `f02` (factual): refused
- `f03` (factual): faithfulness 0.00
- `f04` (factual): faithfulness 0.00
- `f06` (factual): refused
- `f07` (factual): faithfulness 0.50
- `f08` (factual): faithfulness 0.00
- `f09` (factual): key facts 0.50; faithfulness 0.00
- `f10` (factual): faithfulness 0.00
- `f11` (factual): faithfulness 0.00
- `f12` (factual): faithfulness 0.00
- `f13` (factual): faithfulness 0.00
- `f14` (factual): faithfulness 0.00
- `f15` (factual): faithfulness 0.00
- `f16` (factual): faithfulness 0.00
- `f17` (factual): faithfulness 0.00
- `f18` (factual): key facts 0.00; faithfulness 0.00
- `f19` (factual): faithfulness 0.00
- `f20` (factual): key facts 0.50; faithfulness 0.00
- `f21` (factual): refused
- `f22` (factual): refused
- `f23` (factual): faithfulness 0.00
- `f24` (factual): faithfulness 0.00
- `f25` (factual): faithfulness 0.00
- `f26` (factual): faithfulness 0.00
- `f27` (factual): faithfulness 0.50
- `f28` (factual): faithfulness 0.00
- `f29` (factual): faithfulness 0.00
- `f30` (factual): faithfulness 0.00
- `m01` (multi): key facts 0.50; faithfulness 0.00
- `m02` (multi): faithfulness 0.00
- `m03` (multi): refused
- `m04` (multi): key facts 0.50; faithfulness 0.00
- `m05` (multi): key facts 0.50; faithfulness 0.00; recall@5 0.50
