# Known limitations

Where toolcall-ft's results stop, each with the measurement behind it when
there is one. Models ran as GGUF on llama.cpp on one machine (RX 7800 XT).

## How far the result reaches

- **Three seeds for v2, one for v1.** Over three v2 training seeds, the right
  call on test_ood is 0.92 ± 0.05 (0.88 to 0.97) and abstention 0.97 ± 0.04.
  The seed moves the right-call rate about as much as the gap to the 7B, so
  "matches the 7B" is the honest claim, not "beats". v1 was trained once.
- **Six tools, two servers, fixed.** The model was trained on these schemas
  and tested on these schemas. Nothing shows it calls *other* tools better
  than the base model does.
- **Multi-step only since v5, and only teacher-forced.** v1–v4 make one call
  per request. v5's episodes are scored one turn at a time with the right
  history before each turn. A model that goes wrong and then recovers is
  never tested, and neither is a model whose error compounds. Results come
  from a simulated file tree and corpus in the servers' formats, checked
  byte for byte against `filesystem-mcp` on 60 episodes; `crag_search`
  results are not checked against the real server.
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
  `test_ood` has unseen phrasings and unseen values, but the generator's
  style. The two hand-written sets exist for that reason.
- **The hand-written sets are small:** 54, 48, 48, 40 and 39 cases. Their intervals are
  wide (0.91 [0.81, 1.00]), and on `test_hand2` the base model is already at
  0.84 on calls, so the gain there is not significant.
- **`test_hand` is no longer blind for v2.** Its failures were read to decide
  what v2 should fix. `test_hand2` was committed before v2 was trained,
  `test_hand3` before v3, `test_hand4` before v4 and `test_hand5` before any
  model saw it.
- **`test_hand` to `test_hand4` were written by the same author as the
  generator.** They differ in style, not in who imagined the requests, and
  `test_hand4` was written together with the v4 training data. On it, v4's
  gain in abstention is two to three times what it is on `test_hand5`, the
  only set written from a brief by someone who had not seen the generator,
  the training data or the other sets. Quote `test_hand5`. It is also the
  only one, and it is small.
- **One `test_hand5` label was set during review.** "Find the part about
  deployment in the docs, the one with the diagram" was moved from
  ambiguous to a call (`crag_search`, query containing "deployment"), and
  every v4 seed fails it by adding `k: 1` for "the one". Whether that is
  wrong is arguable; the set is frozen, so the label stays.
- **Level 4 is strict by rule.** An argument the request did not ask for
  counts as wrong even when harmless (`offset 1, limit 1000` for "dump the
  file"), and a correct synonym in a search query counts as wrong.

## What the fine-tuned model still gets wrong (v2)

It fails 16 of 294 `test_ood` cases.

- **Folders named without the word "folder".** "What does research contain?"
  accounts for 9 of the 16: the model reads a file, searches the docs, or
  asks.
- **A learned sentence opener leaks.** v1's fixed refusal appeared on valid
  requests. v2 varies the wording, and now the opener of a clarifying
  question appears there instead ("I can do that once I know more…").
- **A trailing instruction taken as the query.** "Run a retrieval on X. Just
  the single best hit." is searched as `"the single best hit"`.

## What v3 still gets wrong

It fails 9 to 16 of 294 `test_ood` cases, depending on the seed.

- **It calls on ambiguous requests v2 refused.** "Find the part about that
  in the docs" is searched as `"that"`, and "fill drafts/outline.py in"
  is answered by writing invented content: 10 cases broken and 2 fixed
  over three seeds (abstention 0.97 → 0.94). The 140 new cases all need a
  call; no ambiguous counterpart was added.
- **A trailing instruction still replaces the query** in 2 of 3 runs
  ("the single best hit", "the best hit"), against 4 for v2.

## What v4 still gets wrong

- **It calls on ambiguous requests that contain a concrete noun.** "The
  config file — not the main one, the other one" and "the output directory
  — you know which one" are answered with `fs_list` on `config` and
  `output`, in all three seeds (`test_hand5`).
- **It drops details on clear requests.** On `test_hand`, seeds 1 and 2
  break 5 calls v3 made, by leaving out `limit`, getting a line count wrong
  or using `fs_list` where `fs_stat` was asked for. On `test_ood` it breaks
  13 calls and fixes 6 over three seeds, each seed's interval including zero.
- **It refuses more answerable askdocs questions than v3:** wrong refusals
  0.23 against v3's 0.05 and the base's 0.21, on one seed.

## What v5 still gets wrong

- **Its final answers drop the value.** On `test_hand6` the final reply
  carries the fact the user asked for in 0.52 ± 0.08 of the turns, against
  v4's 0.57 and 1.00 on the generated episodes. After a write it says
  "It's in notes/overlap.txt now." and leaves out the number it saved; after
  a read it pastes the file instead of answering. The generator's final
  replies only name the file, and the model copied that.
- **It calls after a result that already answers.** An index with 0 chunks,
  then "search it": it searches. A file already reported missing: it calls
  `fs_stat` on it. The 7B does both as well; only the untrained 1.5B
  skips the second call.
- **The episode answer check is a substring match.** A reply that gives the
  right number in other words ("five" for "5", "48 kB" for "48000") fails,
  and two `test_hand6` episodes (021, 064) need arithmetic on the tool
  result, which a 1.5B is not expected to do reliably. Episode 024 needs
  four numbers from two earlier results, and 042 six facts from a paginated
  read: no model passes either.
- **Strict about the route, not only the result.** A model that guesses the
  right file name without listing the folder first fails the step, even when
  the guess would have worked.

## What v6 and DPO still get wrong

- **The reply fix is small on hand-written episodes.** On `test_hand7` the
  value reaches the final reply in 0.68 ± 0.11 (v6) and 0.73 ± 0.04 (DPO)
  of the turns, against 1.00 and 0.85 on the generated ones. No single
  seed's gain over v5 is significant on 27 turns.
- **Whole episodes do not improve.** 0.44 ± 0.04 (v6), 0.50 ± 0.07 (DPO),
  v5 0.47: each breaks about as many call turns as it fixes replies.
- **DPO replies where it should call.** Trained on final turns only, it
  answers instead of calling early in the same kinds of episode
  ("I can do that once I know more…"): 49 of its 58 broken calls on the
  generated episodes. On single requests it calls when it should in 0.93,
  against v5's 0.98.
- **Pairs on the call turns overshoot.** DPO round 2 added them (the right
  call over a sampled mistake) and its calls came back to v5's level, but it
  now calls where no tool is needed: it abstains on 0.06 and 0.02 of
  test_ood's no-tool requests on the two seeds with ~185 call pairs, 0.82 on
  the seed with 24. No pair in the set preferred a reply to a call.
- **Adding abstain pairs overshoots back.** DPO round 3 added pairs that
  prefer the reply to an unneeded call; abstention returned (test_ood 0.94
  to 1.00) and calls inside generated episodes fell to 0.59 / 0.68 / 0.02,
  tracking the ratio of abstain to call pairs. With DPO the mix of pair
  kinds sets the call rate, and no mix tried kept v5's calls.
- **Both answer right after a stat.** Told that `archive` is a directory,
  four of six runs say "archive exists and is empty." instead of listing
  it, an effect of the grounded check-then-read replies.

## Side effects of the training

- **Answering from documents was checked, and held:** on askdocs' 45
  questions, no version regresses against the base 1.5B by askdocs' gate
  (v2: faithfulness −0.02 [−0.16, +0.11], key facts +0.06; v3 and v4
  rerun on 2026-11-21, one seed each). v4 loses v3's drop in wrong refusals,
  as above. v5 (2026-11-22, one seed): key facts 0.55, wrong refusals 0.16,
  faithfulness 0.89, against the base's 0.49, 0.21 and 0.79. v6
  (2026-11-23, one seed): 0.66, 0.02, 0.85; DPO from v5: 0.56, 0.19, 0.72; DPO round 2:
  0.53, 0.16, 0.88; DPO round 3: 0.70, 0.05, 0.81.
- **It is a weak answering model, like its base:** faithfulness 0.12 against
  0.60 for the 3B that askdocs uses.
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
  remove the drop; it is not done (v3 changes one thing at a time).

## Operations

- **The trained model is not published.** `models/` is not in the
  repository; the GGUF has to be rebuilt with `train.py` and `export.py`
  (about 27 minutes on this GPU).
- **The judge needs a cMCP checkout** built next to the repository, pinned by
  commit in CI.
