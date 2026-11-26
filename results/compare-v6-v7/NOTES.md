# v7: v6's data plus the rare episode shapes (`--rare`)

- v7 = v6's recipe (`--multistep --grounded`) plus `rare.py`'s twelve episode kinds
  (`--rare`: `mt7_train`, `mt7_val`), three seeds (20261110, 1, 2), 2 epochs, final eval loss
  0.037 / 0.040 / 0.036. 5132 training examples (v6 3376), longest 1498 tokens.
- `test_hand8` (43 episodes, 90 scored steps) was written from a brief and committed (dc5aaa2)
  before the generator (44a2dba); its text and every result on it stayed unopened until the
  three v7 seeds had been evaluated. One generator phrasing that matched it was reworded before
  training (see CHANGELOG).
- `pooled.md`: `scripts/pooled.py ft-1.5b-v6 ft-1.5b-v7` (three seeds summed, exact McNemar per
  seed). `means.md`: `scripts/means.py`, mean ± sample sd over the seeds, per-seed rates in
  brackets. `../askdocs-forgetting-v7/`: askdocs for seed 0 and the gate against the base.
- No reply in any v7, `mt7-*` or `hand8-*` run starts with a character repeated 16 times.

## Result: episodes right on every hand-written set, a small cost elsewhere

Episodes right (every step of the episode right), mean over seeds; base and 7B one run:

| set | base 1.5B | 7B | v6 | v7 | v6 → v7 fixed / broken (pooled) |
|---|---|---|---|---|---|
| `test_hand8` (blind) | 0.30 | 0.42 | 0.48 ± 0.07 | **0.62 ± 0.01** | 25 / 7 |
| `test_hand7` | | | 0.44 ± 0.04 | 0.56 ± 0.02 | 14 / 4 |
| `test_hand6` | | | 0.45 ± 0.08 | 0.59 ± 0.05 | 20 / 6 |
| `mt7_test_ood` (generated, held-out phrasings) | 0.13 | 0.30 | 0.20 ± 0.03 | 0.84 ± 0.03 | 463 / 4 |
| `mt_test_ood` (v5's generated episodes) | | | 0.86 ± 0.02 | 0.84 ± 0.06 | 36 / 45 |

On `test_hand8` every seed moves the same way (12/2, 8/3, 5/2), but only seed 0 is significant
on its own (p 0.013). Calls right 0.72 → 0.81, abstains when it should 0.78 → 0.86, final reply
carries the value 0.66 → 0.72. The gain carries to the two earlier hand-written episode sets,
which v7's data was not written against (but which were read to choose its kinds).

### By family on `test_hand8` (episodes right; 2–3 episodes per family, so indications only)

| prefix | family | n | base 1.5B | 7B | v6 | v7 |
|---|---|---|---|---|---|---|
| `f1_` | long chains (3+ calls) | 2 | 0.00 | 0.00 | 0.00 | 0.17 |
| `f2_` | retry after a miss | 2 | 0.00 | 0.00 | 0.00 | 0.00 |
| `f3_` | stop when the history already answers | 3 | 0.33 | 0.33 | 0.00 | 0.67 |
| `f4_` | read, edit, write | 2 | 0.00 | 0.00 | 0.00 | 1.00 |
| `f5_` | listing, then metadata | 2 | 0.00 | 1.00 | 0.83 | 0.67 |
| `f6_` | long files in pages | 2 | 0.00 | 0.50 | 0.33 | 0.17 |
| `f7_` | the user corrects | 2 | 0.50 | 0.50 | 0.50 | 0.50 |
| `f8_` | write, then check | 2 | 0.50 | 0.50 | 0.83 | 1.00 |
| `new_` | shapes in no family | 13 | 0.46 | 0.46 | 0.49 | 0.56 |
| `base_` | routine episodes | 13 | 0.31 | 0.46 | 0.72 | 0.79 |

(Labels from the `E |` lines of `data/test_hand8.txt`, in episode order.)

What v7 still gets wrong, the same way in all three seeds:

- **Retry after a miss (`f2_`).** After `fs_read` reports a missing file, v7 says the file
  does not exist instead of listing the folder; then, asked again, it guesses another file name.
  Asked to search the docs for a setting, it guesses a file name (`wal_mode.txt`) instead of
  `crag_search`, and after an off-topic search result it reads a file rather than searching
  with other words. `rare.py` has a read-miss-then-list kind, but also a kind that teaches
  stopping after a miss when the user repeats the request (`f3_`): the two cues are close, and
  the reply wins.
- **Following a reference (`f1_`).** After reading a file that says "see ops/log-schema.json",
  v7 repeats the file instead of reading the one it cites. The generator's long chains descend
  folders; none follows a reference inside a file's text.
- **Pages (`f6_`).** After a range read, where the answer is already in the result, two seeds
  read the file again instead of answering, and the third writes a Python expression as
  `fs_write` content.
- **Corrections (`f7_`).** The corrected call guesses the staging file name
  (`config/database_staging.yaml`), which the episode never shows.

`new_` moves 0.49 → 0.56: most of the gain is on the families the data was built for and on
routine episodes, not on shapes nobody wrote training data for.

## What it costs

- A new habit from the read-edit-write episodes: "replace the contents of keys.txt with:
  rotated" (`test_hand2`) becomes `fs_read keys.txt` in all three seeds, where v6 wrote it,
  and "is exports a file or a folder?" gets `fs_list` instead of `fs_stat` in some seeds. They
  are 4 of `test_hand2`'s 6 broken calls (0.99 → 0.93, 0 fixed). v6's "archive exists and is
  empty." after a stat appears in no v7 run.

- `mt_test_ood` (v5/v6's generated episodes): episodes right 0.86 → 0.84, 36 fixed / 45 broken;
  seed 0 alone loses calls (15 fixed / 29 broken, p 0.049), seeds 1 and 2 do not.
- Single requests: calls right on `test_ood` 0.94 → 0.96 (16 / 6), abstains when it should
  0.98 → 0.96 (1 / 6). `test_id` unchanged.
- askdocs (seed 0, 53 questions, judge Qwen2.5-7B):

  | | base 1.5B | v6 | v7 |
  |---|---|---|---|
  | key facts | 0.49 | 0.66 | 0.62 |
  | wrong refusal | 0.21 | 0.02 | 0.07 |
  | correct refusal | 1.00 | 1.00 | 0.90 |
  | faithfulness | 0.79 | 0.85 | 0.75 |

  The gate against the base passes on every metric. Against v6 every metric moves slightly the
  wrong way, each within the one-seed intervals; the correct-refusal drop is one question
  (`u03`, answered).

## Decision

v7 becomes the default: it raises episodes right on all three hand-written episode sets by
0.12–0.14, more than any change since v5 (v6 and DPO moved them by at most 0.06), and is above
the 7B on the blind one, at the price of a small,
mostly non-significant loss on v5's generated episodes, abstention and askdocs. Retrying after
a miss is not learned by any model measured, and goes in the known limitations.
