# GRPO from v7, on the turns v7 still gets wrong

- GRPO = TRL's GRPOTrainer from the merged v7 of the same seed (`grpo.py`), a new LoRA
  (r 16), beta 0.04 (KL to v7: the reference is v7 with the adapter off), lr 1e-5, 8 replies
  per prompt at temperature 1, 8 prompts per step, 2 epochs. Three seeds (20261110, 1, 2), each
  starting from v7 of that seed.
- **Reward = the evaluation's metric.** Each reply is scored by `score_cases`, the scorer and C
  judge `evaluate.py` uses: 1 if the step is right (the right call at level 4, or an
  abstention that carries the fact where the turn asks for one), 0.5 for a call that parses and
  passes the tool's schema but is not right, 0 otherwise.

## First: on its own training data, v7 leaves GRPO nothing to learn from

A 6-step smoke on all of v7's training turns (5132: `train`, `mt_train_g`, `mt7_train`) gave a
mean reward of 0.97–1.00, and in 47 of the 48 groups all 8 replies scored the same
(`frac_reward_zero_std`). GRPO's advantage is the reply's reward minus its group's mean, so such
a group gives no gradient. At ~60 s a step, one epoch (642 steps) would be ~11–12 hours of GPU
for about a hundred useful prompts.

So the run trains only on the hard turns. `sample.py --all` samples v7 four times at
temperature 1 on every training turn, and `grpo.py --hard-from` keeps the turns where at least
one sample was wrong (server garbage excluded):

| seed | turns wrong per sample (of 5132) | with a wrong sample | GRPO steps | train time |
|---|---|---|---|---|
| 0 | 33, 42, 13, 33 | 67 (1.3%) | 18 | 19 min |
| 1 | 33, 47, 13, 30 | 78 (1.5%) | 20 | 25 min |
| 2 | 35, 35, 18, 32 | 60 (1.2%) | 16 | 18 min |

37 turns are hard for all three seeds (113 for at least one). They are mostly one kind:
`list_then_stat` (`mt7_train`) is 48, 40 and 52 of them; then `check_then_read` (`mt_train_g`;
25 for seed 1) and a few `read_edit_write`, `drill_down`, `user_corrects`, `read_next_page`.
No retry-after-a-miss turn is hard: v7 gets those right on its training data, and fails them
only on the hand-written set (see `../compare-v6-v7/NOTES.md`).

On the hard turns the groups do disagree: the share of groups with one reward is 0.09–0.43 in
the first quarter of the run, the mean reward rises a little (0.82 → 0.86, 0.86 → 0.88,
0.76 → 0.78 from the first to the last quarter), and the KL to v7 stays below 0.0005.

- `pooled.md`: `scripts/pooled.py ft-1.5b-v7 grpo-1.5b-v7` (three seeds summed, exact McNemar
  per seed). `means.md`: `scripts/means.py`, mean ± sample sd over seeds, per-seed rates in
  brackets. `../askdocs-forgetting-grpo/`: askdocs for seed 0 and the gate against the base.
- `../sampled-all-v7{,-s1,-s2}/`: the samples the hard turns come from (evaluate's row format;
  the kept row is a turn's first wrong sample, or its first sample when none was wrong).
- No reply in any GRPO run or sample starts with a character repeated 16 times.

## Result: nothing breaks, nothing significant is fixed

Mean over seeds:

| set | metric | v7 | GRPO | fixed / broken (pooled) |
|---|---|---|---|---|
| `test_hand8` | episodes right | 0.62 ± 0.01 | 0.65 ± 0.00 | 4 / 0 |
| `test_hand8` | final reply carries the value | 0.72 ± 0.02 | 0.74 ± 0.00 | 3 / 1 |
| `test_hand7` | episodes right | 0.56 ± 0.02 | 0.57 ± 0.03 | 1 / 0 |
| `test_hand7` | right call inside an episode | 0.70 ± 0.02 | 0.72 ± 0.03 | 2 / 0 |
| `test_hand6` | episodes right | 0.59 ± 0.05 | 0.60 ± 0.08 | 2 / 1 |
| `mt7_test_ood` | episodes right | 0.84 ± 0.03 | 0.84 ± 0.02 | 6 / 7 |
| `mt_test_ood` | episodes right | 0.84 ± 0.06 | 0.84 ± 0.05 | 3 / 2 |
| `test_ood` | right call | 0.96 ± 0.02 | 0.96 ± 0.02 | 0 / 0 |
| `test_ood` | abstains when it should | 0.96 ± 0.01 | 0.97 ± 0.01 | 1 / 0 |
| `test_id` | right call · abstains | 1.00 · 0.97 | 1.00 · 0.97 | 0 / 0 |

- **No per-seed change is significant** (smallest McNemar p 0.5). Over the six episode sets,
  pooled over seeds, GRPO fixes 20 episodes and breaks 12 (`mt_test_ood` and its grounded twin
  share their episodes, so the two overlap); most of both are on the generated sets.
- **The hand-written episodes move one way.** On `test_hand8` each seed fixes one or two
  episodes and breaks none: seed 0 `new_two_requests_one_msg`, seed 1 `f6_specific_range`,
  seed 2 `new_read_then_search_correct_value` and `base_search_then_write`. A different episode
  in each seed, so this is not one learned behaviour, and `test_hand8` is no longer blind (it
  was read for the v7 analysis). It is an indication only.
- **Unlike DPO, it breaks nothing.** The three DPO rounds each moved the turns their pairs were
  on and broke the rest (abstention 0.06 on two seeds of round 2; calls 0.02 on one seed of
  round 3). With the metric as reward, the KL to v7 and only 60–78 prompts, GRPO stays within
  noise of v7 on every set.
- **askdocs (seed 0):** key-fact recall 0.62 → 0.61, wrong refusals 0.07 → 0.07, faithfulness
  0.75 → 0.80 (40 answers, intervals overlap); gate against the base 1.5B ok on every metric.
- **The failure it was meant for is not in its data.** Retry after a miss (`f2_`) stays at 0.00
  in every seed: v7 does not fail those turns on its training data, so no group on them ever
  disagrees. Training on that failure needs prompts where v7 fails, written apart from
  `test_hand8` and judged on a new blind set.

v7 stays the default: GRPO's gains are within the seed spread and it adds a training stage.
