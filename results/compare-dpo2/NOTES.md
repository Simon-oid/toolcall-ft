# DPO round 2: final-reply pairs + call pairs

- `pooled.md`: `scripts/pooled.py` for v5, v6 and round-1 DPO, each against `dpo2-1.5b-v5`
  (three seeds summed, exact McNemar per seed).
- `means.txt`: per-family rate on every set, mean ± population sd over the three seeds,
  then the per-seed values in brackets (same units as `pooled.py`).
- `../sampled-dpo-v5{,-s1,-s2}`: round-1 DPO sampled on every call turn of train and
  mt_train (`toolcall.sample`, n=4, T=1, top_k 40); the first wrong sample per turn.
  `../onpolicy-dpo-v5` is the greedy pass tried first: 24 wrong of 2254, too few pairs.
- `../../data/prefs_v5c{,-s1,-s2}.jsonl`: v5's 231 final-reply pairs plus the call pairs
  built from those samples: 181, 189 and 24 call pairs. Seed 2's round-1 model was wrong on
  only 24 of 2254 call turns even when sampled, so that seed got a much weaker treatment.
- DPO started from each seed's v5, as round 1 did; train loss 0.20, 0.20, 0.27.

## Result: it calls when it should not

Round 2 brought the calls back to v5's level on generated episodes (0.90 vs v5 0.91 and
round-1 0.84) but broke abstention everywhere, in proportion to the number of call pairs:

| abstain | v5 | v6 | DPO r1 | DPO r2 (seeds 0 / 1 / 2) |
|---|---|---|---|---|
| test_ood | 1.00 | 0.98 | 1.00 | 0.06 / 0.02 / 0.82 |
| mt_test_ood_g | 1.00 | 1.00 | 1.00 | 0.76 / 0.81 / 0.94 |
| test_hand7 | 0.93 | 0.90 | 0.94 | 0.53 / 0.63 / 0.83 |

v5 -> DPO r2 pooled: 220 abstentions broken, 0 fixed on test_ood; 97 broken, 0 fixed on
mt_test_ood_g; 24 broken, 0 fixed on test_hand7. Episodes on test_hand7 fall from 0.47 (v5)
and 0.50 (r1) to 0.30. Seed 0 on test_ood calls `crag_search` on 99 of 105 chit-chat or
general-knowledge requests ("What does CPU stand for?").

Cause: every call pair says "a call beats what you said" and nothing in the set says "a
reply beats a call". The final-reply pairs are on the turn after a tool result, not on
requests that need no tool, so DPO learned a push toward calling with no counterweight.
A fix would need abstain pairs too (chosen = the plain reply, rejected = an unneeded call
sampled from this model). v6 stays the default.

askdocs (seed 0, `../askdocs-forgetting-v6/dpo2.md`): key facts 0.53, wrong refusals 0.16,
faithfulness 0.88; no metric differs from the base model beyond noise.

Every new run was scanned for replies that start with 16 repeated characters: none.
