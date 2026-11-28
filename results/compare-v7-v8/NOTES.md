# v8: v7's data plus retrying after a miss (`--retry`)

- v8 = v7's recipe (`--multistep --grounded --rare`) plus `retry.py`'s nine episode kinds
  (`--retry`: `mt8_train`, `mt8_val`): five that retry after a miss (list the folder after a
  missing file, list the one subfolder, reword an empty search with a name from the
  conversation, follow an off-topic result's pointer, search instead of guessing a file name)
  and four stop twins in which the history already answers. Three seeds (20261110, 1, 2),
  2 epochs, final eval loss 0.035 / 0.035 / 0.035. 6668 training examples (v7 5132), longest
  1498 tokens.
- `test_hand9` (48 episodes, 125 scored steps) was written from a brief and committed
  (c9101bc, 40d4a27) before the generator (e8e577d). A blind checker printed only counts,
  errors and overlap (0 shared contexts, 0 shared 6-grams with any training split); the set's
  text and every result on it stayed unopened until the three v8 seeds had been evaluated.
- `pooled.md`: `scripts/pooled.py ft-1.5b-v7 ft-1.5b-v8` (three seeds summed, exact McNemar
  per seed). `means.md`: `scripts/means.py`, mean ± sample sd over the seeds, per-seed rates in
  brackets. `../askdocs-forgetting-v8/`: askdocs for seed 0, the gate against the base and
  against v7.
- No reply in any v8, `mt8-*` or `hand9-*` run starts with a character repeated 16 times.

## Result: retrying is partly learned; stopping is not; abstention pays

Episodes right (every step of the episode right), mean over seeds; base and 7B one run:

| set | base 1.5B | 7B | v7 | v8 | v7 → v8 fixed / broken (pooled) |
|---|---|---|---|---|---|
| `test_hand9` (blind) | 0.21 | 0.29 | 0.56 ± 0.03 | **0.61 ± 0.07** | 16 / 8 |
| `test_hand8` | 0.30 | 0.42 | 0.62 ± 0.01 | 0.65 ± 0.00 | 18 / 14 |
| `test_hand7` | | | 0.56 ± 0.02 | 0.52 ± 0.02 | 3 / 6 |
| `test_hand6` | | | 0.59 ± 0.05 | 0.58 ± 0.02 | 6 / 7 |
| `mt8_test_ood` (generated, held-out phrasings) | 0.07 | 0.16 | 0.14 ± 0.03 | 0.92 ± 0.03 | 423 / 1 |
| `mt7_test_ood` | 0.13 | 0.30 | 0.84 ± 0.03 | 0.84 ± 0.03 | 36 / 38 |
| `mt_test_ood` | | | 0.84 ± 0.06 | 0.84 ± 0.00 | 29 / 30 |

On `test_hand9` no seed is significant on its own (3/2, 7/1, 6/5). Calls right
0.80 → 0.87 (22 fixed / 6 broken), but abstains when it should 0.83 → 0.78 (2 / 9). The
`mt8` jump measures the generator's own distribution and says only that the kinds were
learned as written.

### By part on `test_hand9` (episodes right, pooled over seeds; indications only)

| prefix | what it asks | n | base 1.5B | 7B | v7 | v8 |
|---|---|---|---|---|---|---|
| `r1_` | missing file → list the folder | 6 | 0.00 | 0.17 | 0.28 | **0.61** |
| `r2_` | empty search → a new word from the conversation | 4 | 0.50 | 0.50 | 0.67 | 0.83 |
| `r3_` | off-topic results → the term they point to | 3 | 0.33 | 0.33 | 0.33 | 0.67 |
| `r4_` | search instead of guessing a file name | 5 | 0.00 | 0.20 | 0.73 | 0.67 |
| `r5_` | listing without the file → its subfolder | 5 | 0.00 | 0.20 | 0.53 | 0.67 |
| `stop_` | twins of the above: the history already answers | 8 | 0.25 | 0.13 | 0.50 | 0.50 |
| `new_` | shapes in no family | 8 | 0.38 | 0.38 | 0.25 | 0.13 |
| `base_` | routine episodes | 9 | 0.22 | 0.44 | 1.00 | 0.96 |

Retry episodes (`r1_`–`r5_`, 23) go 35/69 → 47/69 over the three seeds. Pairs where both the
retry episode and its stop twin are right: v7 2, 2, 2 of 8; v8 2, 4, 2.

What v8 still gets wrong, in every seed:

- **A re-check the user asks for after the history settled it.** In three `stop_` episodes
  the file is already shown missing, or both searches came back empty, and the user says
  "double-check inside the billing folder" or "check the docs again"; every v7 and v8 seed
  lists the folder again in the two file cases, and four of six search again in the third. The set's rule is to answer from the history. A user
  asking outright for the re-check makes this the most debatable label in the set; it is
  kept as written.
- **An empty index is not a miss.** When `crag_search` reports an empty index and the user
  said "if that finds nothing, try lease", every seed searches for "lease" instead of saying
  the index is empty.
- **Impossible requests.** Asked to hit an HTTP endpoint or run a command, no v7 or v8 seed
  says it cannot: they call tools that do not exist (`http_get`, `bash`, `shell_run`), search
  the docs, or write the command into a file.
- **Off by one.** Told by a file to read from line 45, all three v8 seeds pass `offset` 46;
  v7 got the line once, and twice read the wrong file.

## What it costs

- **Abstention, on every hand-written episode set.** Abstains when it should, fixed / broken
  v7 → v8: `test_hand6` 0 / 5, `test_hand7` 1 / 3, `test_hand8` 7 / 10, `test_hand9` 2 / 9.
  The losses are where the history already holds the answer: `error_already_seen` (3 of
  `test_hand6`'s 5), `new_index_vs_dir`, `new_infer_from_context`. v8 calls once more where it
  should have replied, the cost the stop twins were meant to prevent.
- **Shorter searches on single requests.** "find stuff on the token bucket at the HTTP
  acceptor, top 3" becomes `crag_search "the token bucket"`, without `k` or the second part,
  in all three seeds; "retry logic and exponential backoff" loses the backoff. `retry.py`'s
  first searches are the bare topic, and v8 copies that. Calls right on `test_hand`
  0.98 → 0.94 and on `test_hand5` 0.86 → 0.81.
- `test_id`, `test_ood`, `mt_test_ood`, `mt7_test_ood`: within one standard deviation.
- askdocs (seed 0, 53 questions, judge Qwen2.5-7B):

  | | base 1.5B | v7 | v8 |
  |---|---|---|---|
  | key facts | 0.49 | 0.62 | 0.53 |
  | wrong refusal | 0.21 | 0.07 | 0.02 |
  | correct refusal | 1.00 | 0.90 | 1.00 |
  | faithfulness | 0.79 | 0.75 | 0.73 |

  The gate against the base and against v7 passes on every metric; the key-fact drop from v7
  (-0.085, interval -0.205 to +0.031) is inside the one-seed noise.

## Decision

v7 stays the default. v8 is the first version that learns part of the retry
after a miss, but the gain is on one set and significant in no seed alone,
and it gives back abstention on every hand-written episode set, the cost
the stop twins were there to prevent. A next attempt would vary
`retry.py`'s first queries (with `k` and two-part topics), add twins where
the user asks outright for a second look or where the error is two turns
back, and needs a new blind set: `test_hand9` has now been read.
