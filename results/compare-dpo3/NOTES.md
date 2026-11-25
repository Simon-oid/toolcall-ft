# DPO round 3: final-reply + call + abstain pairs (point 26c)

- `pooled.md`: `scripts/pooled.py` for v5, v6, round 1 and round 2, each against
  `dpo3-1.5b-v5` (three seeds summed, exact McNemar per seed).
- `means.md`: `scripts/means.py` over the five families, mean ± sample sd over the seeds,
  per-seed rates in brackets.
- `../sampled-abstain-dpo2-1.5b-v5{,-s1,-s2}`: round-2 DPO sampled on the 615 training turns
  that need no call (single requests, and episode turns where the user spoke last;
  `toolcall.sample --abstain`, n=4, T=1); the first sample that calls is kept.
- `../../data/prefs_v5ca{,-s1,-s2}.jsonl`: 231 final-reply pairs + round 2's call pairs +
  abstain pairs (chosen = the training reply, rejected = the sampled call):

  | seed | call pairs | abstain pairs | abstain / call |
  |---|---|---|---|
  | 0 | 181 | 505 | 2.8 |
  | 1 | 189 | 565 | 3.0 |
  | 2 | 24 | 99 | 4.1 |

- DPO from each seed's v5, as before; train loss 0.12, 0.12, 0.24.

## Result: abstention comes back, calls go

| | v5 | DPO r2 | DPO r3 (seeds 0 / 1 / 2) |
|---|---|---|---|
| abstains when it should, test_ood | 1.00 | 0.06 / 0.02 / 0.82 | 0.94 / 1.00 / 1.00 |
| calls right, test_ood | 0.94 | 0.89 (mean) | 0.59 / 0.74 / 0.30 |
| right call inside an episode, generated held-out | 0.91 | 0.90 (mean) | 0.59 / 0.68 / 0.02 |
| right call inside an episode, test_hand7 | 0.69 | 0.68 (mean) | 0.33 / 0.53 / 0.03 |
| final reply carries the value, test_hand7 | 0.59 | 0.52 (mean) | 0.63 / 0.70 / 0.78 |
| episodes right, test_hand7 | 0.47 | 0.30 (mean) | 0.33 / 0.47 / 0.20 |

v5 -> r3 pooled: 228 calls broken, 1 fixed on test_ood; 371 broken, 5 fixed on the generated
episodes. The damage follows the ratio of abstain pairs to call pairs: seed 2 (4.1 to 1) almost
never calls ("Run a retrieval on the soak test, please." -> "Happy to help. What should I look
up?"). Seeds 0 and 1 still call, but often the wrong tool: on test_ood seed 0 answers 20 of the
35 `crag_search` turns with `crag_stats`. The rejected side of the abstain pairs is made of
real calls (seed 0: `fs_write` 197, `crag_search` 156, `fs_list` 48), so DPO pushed those calls
down in general, not only on requests that need no tool.

askdocs (seed 0, `../askdocs-forgetting-v6/dpo3.md`): key facts 0.70, wrong refusals 0.05,
faithfulness 0.81, against the base's 0.49, 0.21 and 0.79; key facts +0.21 [+0.09, +0.34].
A model that calls less answers documents better; it is not a better tool caller.

Three rounds, one lesson: with DPO here the mix of pair kinds sets the call rate. Final-reply
pairs alone made it reply instead of calling, call pairs made it call everywhere, abstain pairs
on top made it stop calling. v6 (SFT on whole episodes) stays the default.

Every new run was scanned for replies that start with 16 repeated characters: none.
