# Known limitations

Where toolcall-ft's results stop, each with the measurement behind it when
there is one. Models ran as GGUF on llama.cpp on one machine (RX 7800 XT).
The default model is v7; what earlier versions got wrong, and which version
fixed it, is in [`docs/results.md`](docs/results.md).

## How far the result reaches

- **Three training seeds, from v2 on; one for v1.** v7's right call on
  test_ood is 0.96 ± 0.02 over the seeds, against the 7B's 0.90. The seed
  moves the rate about as much as the gap to the 7B, so "matches the 7B" is
  the honest claim, not "beats".
- **Six tools, two servers, fixed.** The model was trained on these schemas
  and tested on these schemas. Nothing shows it calls *other* tools better
  than the base model does.
- **Multi-step is teacher-forced.** Episodes are scored one turn at a time,
  with the right history before each turn. A model that goes wrong and then
  recovers is never tested, and neither is a model whose error compounds.
- **Tool results are simulated.** They come from an in-memory file tree and
  corpus in the servers' formats, checked byte for byte against
  `filesystem-mcp` on 60 episodes of `episodes.py` and 80 of `rare.py`
  (directory sizes normalised); `crag_search` results are not checked
  against the real server.
- **English only**, apart from two greetings in the hand-written sets.
- **The 7B baseline is Q4_K_M, the 1.5B models are Q8_0.** Each model runs at
  the quantization it would be served at on this GPU. The 7B at higher
  precision might do better.
- **One hosted model, one setting.** gpt-oss-120b on Groq's free tier, at
  `reasoning_effort: low`. A higher effort, or another large model, may do
  better, especially on abstention. Its runtime differs from llama.cpp, and
  part of its right-call gap is the dataset's `k` default, which it never saw.

## The test sets

- **Most test cases come from the generator that made the training data.**
  `test_ood` and `mt_test_ood` have unseen phrasings and unseen values, but
  the generator's style. On episodes the generated test overstates the gain
  (v6: 0.86 generated, 0.44 by hand; v7: 0.84 and 0.62 on the blind set).
  `rare.py`'s own test, `mt7_test_ood`, overstates it most: v7 0.84 against
  v6's 0.20, where `test_hand8` moves 0.48 → 0.62.
- **The hand-written sets are small:** 54, 48, 48, 40 and 39 single requests,
  32, 30 and 43 episodes. Their intervals are wide, and on `test_hand7` the 27
  final turns with a value to report are too few for any one seed's change to
  be significant; the seeds are summed instead. On `test_hand8` only seed 0's
  gain is significant on its own (p 0.013), and its eight families have 2–3
  episodes each: a rate per family is an indication, not a measurement.
- **Which sets are still blind.**
  - `test_hand` was read to decide what v2 should fix; `test_hand2` was
    committed before v2 was trained, `test_hand3` before v3, `test_hand4`
    before v4, `test_hand5` before any model saw it, `test_hand6` before any
    v5 result was opened, `test_hand7` before any v6 or DPO result was.
  - `test_hand6` was then read to design v6's fix, so it is no longer blind
    for v6 or DPO.
  - `test_hand7` was written knowing the defect it measures, though not the
    generator.
  - `test_hand6` and `test_hand7` were both read to choose v7's new episode
    kinds, so neither is blind for v7. `test_hand8` was written from a brief
    and committed before `rare.py`, and stayed unread until v7's three seeds
    were evaluated; one generator phrasing that matched it word for word was
    reworded before training. It has now been read for v7's error analysis,
    so a v8 needs a new set.
- **Who wrote them.** `test_hand` to `test_hand4` were written by the author
  of the generator; they differ in style, not in who imagined the requests,
  and `test_hand4` was written together with the v4 training data. On it,
  v4's gain in abstention is two to three times what it is on `test_hand5`.
  `test_hand5` to `test_hand8` were written from a brief by someone who had
  not seen the generator: quote those.
- **One `test_hand5` label was set during review.** "Find the part about
  deployment in the docs, the one with the diagram" was moved from
  ambiguous to a call (`crag_search`, query containing "deployment"), and
  every v4 seed fails it by adding `k: 1` for "the one". Whether that is
  wrong is arguable; the set is frozen, so the label stays.
- **Level 4 is strict by rule.** An argument the request did not ask for
  counts as wrong even when harmless (`offset 1, limit 1000` for "dump the
  file"), and a correct synonym in a search query counts as wrong.
- **The episode answer check is a substring match.** A reply that gives the
  right number in other words ("five" for "5", "48 kB" for "48000") fails.
  Two `test_hand6` episodes (021, 064) need arithmetic on the tool result;
  024 needs four numbers from two earlier results, and 042 six facts from a
  paginated read: no model passes those two.
- **Strict about the route, not only the result.** A model that guesses the
  right file name without listing the folder first fails the step, even when
  the guess would have worked.

## What v7, the default, still gets wrong

- **Four hand-written episodes in ten.** 0.62 ± 0.01 on the blind
  `test_hand8`, 0.56 and 0.59 on `test_hand7` and `test_hand6`.
- **It does not retry after a miss.** After a read reports a missing file it
  says the file does not exist instead of listing the folder; asked to search
  the docs, it guesses a file name. It gets neither of `test_hand8`'s two
  such episodes right in any seed, and neither do the base and the 7B. `rare.py` teaches both the retry and, when the user
  repeats a request after a miss, stopping: the cues are close.
- **It does not follow a reference.** After reading a file that says "see
  ops/log-schema.json", it repeats the file instead of reading the one cited.
  No generated episode follows a reference inside a file's text.
- **Shapes nobody wrote data for barely move:** 0.49 → 0.56 on `test_hand8`'s
  `new_` episodes, against 0.00 → 1.00 on read-edit-write.
- **It reads before a write that needs no read.** "replace the contents of
  keys.txt with: rotated" becomes `fs_read`, in all three seeds, an effect of
  the read-edit-write episodes. "Is exports a file or a folder?" gets
  `fs_list` instead of `fs_stat` in some seeds.
- **Small losses against v6:** v5's generated episodes 0.86 → 0.84 (36 fixed,
  45 broken; one seed significant), abstention on test_ood 0.98 → 0.96,
  test_hand2 right calls 0.99 → 0.93 (0 fixed, 6 broken), and on askdocs
  wrong refusals 0.02 → 0.07 (one seed).
- v6's "archive exists and is empty." after a stat no longer appears, and
  stopping when the history already answers (an index with 0 chunks, a file
  already missing) rises from 0.00 to 0.67 of `test_hand8`'s three episodes.

## Preference tuning did not help

Three DPO rounds from v5 were measured against v6
([README](README.md#preference-tuning-three-dpo-rounds)). None was kept:

- **The pairs only constrain the turns they are on.** Final-reply pairs made
  the model reply instead of calling earlier in the same episodes; call
  pairs made it call on requests that need no tool (test_ood abstention
  0.06 and 0.02 on two seeds); abstain pairs on top made it stop calling
  (calls inside generated episodes 0.59, 0.68 and 0.02 by seed).
- **The ratio of pair kinds sets the call rate,** and no mix tried kept v5's
  calls. Tuning the ratio against the test sets would fit it to them, so it
  was not done. A supervised term on the chosen side was not tried.
- **GRPO from v7 changed little** ([notes](results/compare-v7-grpo/NOTES.md)).
  With the evaluation's metric as reward it broke nothing, but no change
  was significant (`test_hand8` episodes 0.62 → 0.65). v7 is right on
  98.5% of its own training turns even when sampled, so only 60–78 turns
  per seed give a learning signal. The failure GRPO was meant for, retrying
  after a miss, is not among them. Training on it needs new prompts where
  v7 fails, and a new blind set to judge them.

## Side effects of the training

- **Answering from documents was checked, and held.** On askdocs' evaluation
  questions (45 for v1–v2, 53 from v3 on) no version regresses against the
  base 1.5B by askdocs' gate. On the latest askdocs, v7 recalls more key
  facts than the base (0.62 against 0.49) and refuses 3 answerable questions
  in 43 (base: 9, v6: 1). One seed per
  version; v4 refused more than v3 (0.23 against 0.05), so caution learned
  for tool calls can carry over to answering.
- **It is a weak answering model, like its base:** faithfulness 0.12 against
  0.60 for the 3B that askdocs uses (v2, measured with the older askdocs).
- **Nothing else about general ability was measured.**

## Constrained decoding

- **The findings are for one llama.cpp build** (`a4d4f2f`). The fixed key
  order that made the grammar drop `limit` is how that build derives a
  grammar from a schema; another build or another runtime may differ.
- **The fine-tuned model is best served free, and the reason is in the
  training data.** Under the lazy grammar its right-call rate falls
  (0.91 → 0.87 for v1 on `test_ood`). All 7 cases the grammar breaks (and
  none it fixes) are line-range reads that lose `limit`: the same mechanism
  as the 7B's. The grammar orders keys required first, then optional in
  schema order (`path`, `limit`, `offset`); every training call with both
  writes `path`, `offset`, `limit` (147 of 147), so the model learned the
  order the grammar forbids. Training with the grammar's key order should
  remove the drop; it was not done, to change one thing at a time.

## Operations

- **The trained model is not published.** `models/` is not in the
  repository; the GGUF has to be rebuilt with `train.py` and `export.py`
  (v7: about 98 minutes of training on this GPU, plus a few minutes of
  export).
- **The judge needs a cMCP checkout** built next to the repository, pinned by
  commit in CI.
- **llama.cpp on ROCm occasionally returns garbage** (a reply of one
  repeated character). Every committed run was scanned for it, and the two
  affected runs were evaluated again.
