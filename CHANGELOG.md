# Changelog

All notable changes to toolcall-ft. Dates are ISO 8601.

## Unreleased

- v4: 140 ambiguous training cases answered with a clarifying question,
  three seeds, compared with v3 seed by seed. Abstention on test_ood
  0.94 ± 0.04 → 0.99 ± 0.01 (19 fixed, 2 broken); on the independent
  `test_hand5` 0.80 → 0.89 (5 fixed, 0 broken). Right call on test_ood
  0.96 → 0.95 (6 fixed, 13 broken, no seed significant). On askdocs, wrong
  refusals return to the base's level (v3 0.05, v4 0.23, one seed).
- `data/test_hand4.jsonl`: 40 hand-written cases, committed before v4 was
  trained, written together with the v4 data.
- `data/test_hand5.txt`: 39 cases written from a brief by someone who had
  not seen the generator, the training data or the other sets; committed
  before evaluation. `toolcall.handset` converts it to JSONL, and a test
  keeps the two identical.
- askdocs forgetting check rerun for the base, v3 and v4.
- v3: 140 training cases for bare-folder `fs_list` and for a search
  constraint after a closed sentence, three seeds, compared with v2 seed by
  seed. Right call on test_ood 0.92 ± 0.05 → 0.96 ± 0.01; on the blind
  `test_hand3` 0.89 → 0.97 (8 fixed, 0 broken). Abstention on test_ood
  0.97 → 0.94: v3 calls on some ambiguous requests v2 refused.
- `data/test_hand3.jsonl`: 48 hand-written cases, committed before v3 was
  trained.
- Analysis: why the fine-tuned model loses calls under the lazy grammar
  (0.91 → 0.87). All 7 broken cases drop `limit` on a line range, because
  the training calls write `offset` before `limit` (147 of 147) and the
  grammar llama.cpp derives from the schema orders them the other way.
  See `KNOWN_LIMITATIONS.md`.
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
