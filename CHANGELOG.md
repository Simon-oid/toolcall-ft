# Changelog

All notable changes to toolcall-ft. Dates are ISO 8601.

## Unreleased

- DPO round 3 (point 26c): round 2's pairs plus abstain pairs on the 615
  training turns that need no call, an unneeded call sampled from round 2
  rejected and the training reply chosen (`toolcall.sample --abstain`,
  `toolcall.prefs --abstain-from`): 505, 565 and 99 by seed, from v5.
  Abstention on test_ood returns to 0.94 / 1.00 / 1.00, but calls inside
  generated episodes fall to 0.59 / 0.68 / 0.02 (v5 0.91), following the
  ratio of abstain to call pairs; seed 0 swaps `crag_search` for
  `crag_stats`. askdocs key facts 0.70, wrong refusals 0.05 (one seed).
  v6 stays the default. `scripts/means.py`: per-family rates over seeds.
- DPO round 2 (point 26b): round 1's 231 final-reply pairs plus pairs on the
  call turns of train and mt_train, the right call chosen and a mistake of
  round-1 DPO rejected (`toolcall.sample`: 4 samples at T=1, since greedy it
  is wrong on only 24 of 2254; `toolcall.prefs --calls-from`): 181, 189 and
  24 call pairs by seed, trained from v5. Calls inside generated episodes
  return to v5's level (0.84 → 0.90, v5 0.91), but it learns to call where
  no tool is needed: abstention on test_ood 1.00 → 0.06 / 0.02 / 0.82 by
  seed (0 fixed, 220 broken pooled), episodes right on test_hand7 0.47 →
  0.30. The set had no pairs preferring a reply to a call. v6 stays the
  default. `LlamaCpp` gains `temperature` and `seed`.
- v6 and DPO (point 26): grounded final replies (`toolcall.grounded`: after
  a save the reply quotes what was written, after a check-then-read it gives
  the size and the contents; 231 training episodes change), learned two
  ways, three seeds each. v6 retrains v5's recipe on them; DPO trains a LoRA
  on v5 with 231 on-policy pairs per seed (`toolcall.prefs`,
  `toolcall.dpo`, beta 0.1, reference v5). On the blind `test_hand7` the
  value reaches the final reply in 0.59 (v5) → 0.68 (v6) and 0.73 (DPO),
  the 7B 0.70; episodes right stay at 0.44–0.50. DPO breaks calls: on
  generated episodes 58 broken, 4 fixed, mostly replying instead of calling;
  single-turn calls when it should 0.98 → 0.93. v6 keeps single-turn as v5,
  and on askdocs wrong refusals drop to 0.02 (one seed).
- `data/test_hand7.txt`: 30 hand-written episodes (66 scored turns), written
  from a new brief knowing v5's defect, committed before any v6 or DPO
  result was opened.
- `scripts/pooled.py`: paired comparison of two model families with the
  seeds' fixed and broken counts summed and McNemar per seed.

- v5: multi-step and multi-turn episodes (`toolcall.episodes`, ten kinds,
  results rendered in the servers' formats by `toolcall.corpus`), scored
  turn by turn with the right history; an episode is right when every turn
  is. Trained on v4's data plus 1,409 episode turns, three seeds. Episodes
  right on the generated held-out split 0.35 ± 0.03 → 0.90 ± 0.03; on the
  hand-written `test_hand6` 0.25 ± 0.03 → 0.40 ± 0.07 (7B 0.44). Right call
  inside an episode 0.36 → 0.68 (47 fixed, 6 broken); final replies carrying
  the tool's fact 0.57 → 0.52 (12 fixed, 16 broken): v5 copies the
  generator's terse replies. Single-turn sets and askdocs unchanged within
  noise.
- `data/test_hand6.txt`: 32 hand-written episodes (74 scored turns), written
  from a brief without seeing the generator, committed before any v5 result
  was opened. `toolcall.handset_mt` converts the text format.
- `evaluate`: step and episode rates for episode splits; `compare.py`: a
  paired `step` metric for them.

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
