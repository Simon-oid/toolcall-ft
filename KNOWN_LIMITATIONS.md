# Known limitations

Where toolcall-ft's results stop, each with the measurement behind it when
there is one. Models ran as GGUF on llama.cpp on one machine (RX 7800 XT).

## How far the result reaches

- **One training run per version, one seed.** "The 1.5B matches the 7B" rests
  on a single v1 run and a single v2 run. The evaluation itself is
  deterministic, but how much the result moves with the training seed has not
  been measured.
- **Six tools, two servers, fixed.** The model was trained on these schemas
  and tested on these schemas. Nothing shows it calls *other* tools better
  than the base model does.
- **One call per request.** No multi-step tasks, no call that depends on a
  previous tool result, no conversation history.
- **English only**, apart from two greetings in the hand-written sets.
- **The 7B baseline is Q4_K_M, the 1.5B models are Q8_0.** Each model runs at
  the quantization it would be served at on this GPU. The 7B at higher
  precision might do better.
- **No comparison with a large hosted model.** The plan was a free-tier API,
  and it has not been run.

## The test sets

- **Most test cases come from the generator that made the training data.**
  `test_ood` has unseen phrasings and unseen values, but the generator's
  style. The two hand-written sets exist for that reason.
- **The hand-written sets are small:** 54 and 48 cases. Their intervals are
  wide (0.91 [0.81, 1.00]), and on `test_hand2` the base model is already at
  0.84 on calls, so the gain there is not significant.
- **`test_hand` is no longer blind for v2.** Its failures were read to decide
  what v2 should fix. `test_hand2` was committed before v2 was trained.
- **The hand-written cases were written by the same author as the
  generator.** They differ in style, not in who imagined the requests.
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

## Side effects of the training

- **Answering from documents was checked, and held:** on askdocs' 45
  questions, neither version regresses against the base 1.5B (v2:
  faithfulness −0.02 [−0.16, +0.11], key facts +0.06).
- **It is a weak answering model, like its base:** faithfulness 0.12 against
  0.60 for the 3B that askdocs uses.
- **Nothing else about general ability was measured.**

## Constrained decoding

- **The findings are for one llama.cpp build** (`a4d4f2f`). The fixed key
  order that made the grammar drop `limit` is how that build derives a
  grammar from a schema; another build or another runtime may differ.
- **The fine-tuned model is best served free.** Under the lazy grammar its
  right-call rate falls (0.91 → 0.87 for v1 on `test_ood`). The cause was
  not analysed for the fine-tuned model.

## Operations

- **The trained model is not published.** `models/` is not in the
  repository; the GGUF has to be rebuilt with `train.py` and `export.py`
  (about 27 minutes on this GPU).
- **The judge needs a cMCP checkout** built next to the repository, pinned by
  commit in CI.
