# Known limitations

Where toolcall-ft's results stop, each with the measurement behind it when
there is one. Models ran as GGUF on llama.cpp on one machine (RX 7800 XT).
The default model is v6; what earlier versions got wrong, and which version
fixed it, is in [`docs/results.md`](docs/results.md).

## How far the result reaches

- **Three training seeds, from v2 on; one for v1.** v6's right call on
  test_ood is 0.94 ± 0.03 over the seeds, against the 7B's 0.90. The seed
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
  `filesystem-mcp` on 60 episodes; `crag_search` results are not checked
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
  about twice (v6: 0.86 generated, 0.44 by hand).
- **The hand-written sets are small:** 54, 48, 48, 40 and 39 single requests,
  32 and 30 episodes. Their intervals are wide, and on `test_hand7` the 27
  final turns with a value to report are too few for any one seed's change to
  be significant; the seeds are summed instead.
- **Which sets are still blind.**
  - `test_hand` was read to decide what v2 should fix; `test_hand2` was
    committed before v2 was trained, `test_hand3` before v3, `test_hand4`
    before v4, `test_hand5` before any model saw it, `test_hand6` before any
    v5 result was opened, `test_hand7` before any v6 or DPO result was.
  - `test_hand6` was then read to design v6's fix, so it is no longer blind
    for v6 or DPO.
  - `test_hand7` was written knowing the defect it measures, though not the
    generator.
- **Who wrote them.** `test_hand` to `test_hand4` were written by the author
  of the generator; they differ in style, not in who imagined the requests,
  and `test_hand4` was written together with the v4 training data. On it,
  v4's gain in abstention is two to three times what it is on `test_hand5`.
  `test_hand5` to `test_hand7` were written from a brief by someone who had
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

## What v6, the default, still gets wrong

- **The reply fix is small on hand-written episodes.** On `test_hand7` the
  value reaches the final reply in 0.68 ± 0.11 of the turns, against 1.00 on
  the generated episodes and the 7B's 0.70.
- **Whole hand-written episodes do not improve.** 0.44 ± 0.04 on
  `test_hand7`, against v5's 0.47 and the 7B's 0.47: v6 breaks about as many
  call turns as it fixes replies.
- **It answers right after a stat.** Told that `archive` is a directory, it
  can say "archive exists and is empty." instead of listing it (four of the
  six v6 and DPO-1 runs), an effect of the grounded check-then-read replies.
- **It calls after a result that already answers.** An index with 0 chunks,
  then "search it for deployment": it searches, in every seed, as v5 and the
  7B do. A file already reported missing, asked about again: it calls
  `fs_stat` on it, in every seed.

## Preference tuning did not help

Three DPO rounds from v5 were measured against v6
([README](README.md#preference-tuning-three-dpo-rounds)). None is kept:

- **The pairs only constrain the turns they are on.** Final-reply pairs made
  the model reply instead of calling earlier in the same episodes; call
  pairs made it call on requests that need no tool (test_ood abstention
  0.06 and 0.02 on two seeds); abstain pairs on top made it stop calling
  (calls inside generated episodes 0.59, 0.68 and 0.02 by seed).
- **The ratio of pair kinds sets the call rate,** and no mix tried kept v5's
  calls. Tuning the ratio against the test sets would fit it to them, so it
  was not done. Other preference methods (a supervised term on the chosen
  side, GRPO with the judge as reward) were not tried.

## Side effects of the training

- **Answering from documents was checked, and held.** On askdocs' 45
  questions no version regresses against the base 1.5B by askdocs' gate. On
  the latest askdocs, v6 recalls more key facts than the base (0.66 against
  0.49) and refuses 1 answerable question in 43 (base: 9). One seed per
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
  (v6: about 63 minutes of training on this GPU, plus a few minutes of
  export).
- **The judge needs a cMCP checkout** built next to the repository, pinned by
  commit in CI.
- **llama.cpp on ROCm occasionally returns garbage** (a reply of one
  repeated character). Every committed run was scanned for it, and the two
  affected runs were evaluated again.
