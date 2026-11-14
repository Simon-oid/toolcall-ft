# Changelog

All notable changes to toolcall-ft. Dates are ISO 8601.

## Unreleased

- Hosted-model baseline: `evaluate --api-model` (OpenAI-compatible API,
  native tools, token-per-minute throttling, 429 retry, provider-rejected
  calls scored from the raw generation). gpt-oss-120b at reasoning low:
  right call 0.89 on test_ood (0.94 counting the `k: 10` convention misses),
  abstention 0.79.
- v2 retrained with seeds 1 and 2: right call on test_ood 0.92 ± 0.05,
  abstention 0.97 ± 0.04 over three seeds.

## 0.1.0 — 2026-11-11

First release: the question, the measurement, and a fine-tuned model that
answers it.

### Measurement
- `judge/judge.c`: levels 1–2 of a tool call decided by cMCP's own JSON
  parser and JSON Schema validator.
- `score.py`: levels 3–4 against the expected call (`exact`, `any_of`,
  `contains_all`, optional arguments), and abstention for requests that need
  no call.
- `evaluate.py`: free, eager-constrained and lazy-grammar decoding through
  llama.cpp, one request at a time (exactly reproducible), with bootstrap
  intervals; `scripts/compare.py` for paired comparisons with McNemar's test.

### Data
- A seeded generator: 9 intents over six tools and three kinds of no-call,
  with `test_id` (unseen values) and `test_ood` (held-out phrasings).
- Two hand-written test sets; the second committed before the model it
  judges was trained.
- v2 training data: varied refusals and clarifying questions, 160 extra
  line-range reads, test cases byte-identical to v1's.

### Model
- LoRA fine-tuning of Qwen2.5-1.5B-Instruct with the loss on the completion
  only, export to Q8_0 GGUF.
- v2 on held-out phrasings: right call 0.92 (base 0.70, 7B 0.90), abstains
  when it should 0.99 (base 0.55, 7B 0.60).

### Findings
- Constraining the whole reply to JSON removes the choice not to call.
- llama.cpp's tool grammar fixes the key order and silently dropped an
  argument in 20 of 24 line-range calls from the 7B.
