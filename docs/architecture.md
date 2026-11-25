# Architecture

How toolcall-ft is put together, and why. The numbers are in the
[README](../README.md) and, version by version, in [`results.md`](results.md);
this is the design.

## The pipeline

```
 cMCP servers ──snapshot_tools.sh──► data/tools.json (6 tools, their inputSchemas)
                                           │
 data.py (seeded generator) ──► train / val / test_id / test_ood     test_hand … test_hand8
 episodes.py ──► mt_* (episodes, results     │                       (written by hand;
   in the servers' formats, corpus.py)      │                        handset.py, handset_mt.py)
 grounded.py ──► mt_*_g (final replies       │
   that carry the value, v6)                 │
 rare.py ──► mt7_* (the episode shapes       │
   episodes.py never makes, v7)              ▼
        │                          prompt.py: the model's own chat template + tools
        │ distill.py: base model           │
        │ answers the chit-chat            ▼
        ▼                          llama.cpp server (GGUF), one request at a time
 train.py: LoRA, loss on the               │ raw text
 completion only                           ▼
        │                          score.py ◄── judge/judge.c (cMCP's parser + schema validator)
        ▼                                  │
 export.py: merge ► GGUF Q8_0 ──► served   ▼
        │                          evaluate.py ► results/<run>/results.jsonl, report.md
        ▼                          scripts/compare.py (one seed), pooled.py and means.py (three)
 prefs.py + sample.py: on-policy
 pairs ► dpo.py: DPO LoRA on the
 merged SFT model ► export.py
```

## Decisions

Each one with what it buys and what it costs.

### 1. The judge is the server's own code

Levels 1 and 2 (valid JSON, valid against the tool's schema) are decided by
`judge/judge.c`, which links cMCP's core library and calls the parser and
validator the servers run on `tools/call`.

- **Buys:** a call that passes is a call the server accepts, for the same
  reasons. Two validators can disagree on edge cases (integer against float,
  `additionalProperties`, string length in code points), and only one of them
  is the system the model will talk to.
- **Costs:** a C build step and a dependency on a cMCP checkout, pinned by
  commit in CI.
- **Checked:** a call with no `arguments` is rejected by the judge, and by
  the real `crag-mcp` too.

### 2. Four levels, each conditional on the one before

json → schema → right tool → right arguments.

- **Buys:** it separates what constrained decoding can guarantee (levels 1–2)
  from what only the model can get right (3–4). Without that split, the
  grammar that silently dropped `limit` would have looked like an
  improvement: every call it produced was valid.
- **Costs:** level 4 needs a per-argument matching rule (`exact`, `any_of`,
  `contains_all`), and the rules encode judgement. A correct synonym in a
  search query counts as wrong.

### 3. Not calling is scored separately, in three kinds

`no_tool`, `unsupported`, `ambiguous`.

- **Buys:** a model that always calls a tool scores well on levels 1–4 and is
  unusable. The three kinds fail differently: the base 1.5B calls on
  chit-chat, and the 7B calls on operations no tool does.
- **Costs:** "should it ask or guess?" is a judgement call for some requests.

### 4. One runtime, one request at a time

Every model runs as GGUF on a llama.cpp server with a single slot, and the
raw reply is judged.

- **Buys:**
  - A difference between two rows is the model or the constraint, never the
    software.
  - The evaluation is exactly reproducible: two identical runs gave 0
    different replies in 474.
  - The fine-tuned model is evaluated in the form it is served in.
- **Costs:** the evaluation is slower than a batched one, a few minutes for
  474 cases.

### 5. Three kinds of test, for three different doubts

| Test | Doubt it answers |
|---|---|
| `test_id`: seen phrasings, unseen values | did it memorise the file names and topics? |
| `test_ood`: held-out phrasing families, unseen values | did it memorise the phrasings? |
| `test_hand` to `test_hand5`: written by hand | did it learn the generator's style and not the task? |
| `mt_test_id`, `mt_test_ood`, `mt7_test_id`, `mt7_test_ood`, `test_hand6` to `test_hand8`: episodes | can it chain calls and follow a conversation? |

- **Hygiene, enforced by tests:**
  - no test request or test value appears in training;
  - evaluation splits never repeat a request, since repeats would narrow the
    intervals falsely;
  - CI regenerates the data and requires it to match the committed files.
- **A test read for error analysis stops being a test.** `test_hand` was
  used to decide what v2 should fix. So `test_hand2` was written and
  committed before v2 was trained: the commit order is the evidence that it
  is blind. `test_hand6` was read to design v6's fix, so `test_hand7` was
  written and committed before any v6 or DPO result was opened. Both were
  then read to choose v7's new episode kinds, so `test_hand8` was written
  from a brief and committed before the generator that makes them
  (`rare.py`); the check that its requests are not in training reports
  counts only, so it stays unread.

### 6. Training sees exactly what evaluation sees

`train.py` renders prompts with the same function as `evaluate.py`, and the
loss is on the completion only.

- **Buys:** no train/serve skew, and no capacity spent learning to reproduce
  1,000 tokens of tool schemas.
- **Guards, because both failures are silent:**
  - the script refuses to start if any example is longer than `--max-length`:
    a truncated example loses the very tokens the loss is on;
  - it decodes the tokens the loss falls on and requires them to end with
    exactly one end-of-turn token.

### 7. The no-call targets do not teach a new voice

- **`no_tool` replies** are the base model's own answers, generated with no
  tools in the prompt. Replies cut by the token limit are dropped.
- **Refusals and clarifying questions** come in several wordings, chosen by
  a hash of the request. One fixed sentence (v1) leaked onto valid requests.
  Several wordings reduced the leak but did not end it.

### 8. The served artifact is compared like with like

The adapter is merged and converted to Q8_0, the quantization of the base
model it is compared with.

- **Buys:** the measured gain is the training, not a quantization difference.
- **Costs:** the merged model is a full copy of the weights (1.6 GB), where
  the adapter alone is a small fraction of that. But llama.cpp would load an
  adapter at runtime, and the two models would no longer run the same way.

### 9. Episodes are scored turn by turn, with the right history

A multi-step or multi-turn episode becomes one case per model turn
(`episodes.py`, `handset_mt.py`). Each case holds the conversation so far,
with the correct earlier calls and the tool results in the servers' own
formats, and the turn the model must produce: a call, judged on the four
levels, or a reply with no call that must contain the fact the tool
returned. An episode is right when all its turns are.

- **Buys:** each turn is measured on its own, so a failure is located (the
  listing, the read, the final answer), and the scorer and judge are the
  single-turn ones. No live server is needed at evaluation.
- **Costs:** teacher forcing never shows the model its own mistakes, so
  recovery and compounding errors go unmeasured. The results are simulated:
  a test checks `filesystem-mcp`'s byte for byte on 60 episodes, but not
  `crag_search`'s.
- **The training targets are the same turns.** The history renders exactly
  as the training completion does (`<tool_call>…</tool_call>` in the chat
  template), so what the model wrote in one turn is what it reads in the
  next.

### 10. SFT and DPO get the same new targets, and are compared on a blind set

v6's grounded replies (`grounded.py`) are both its SFT targets and DPO's
"chosen" side; DPO's "rejected" side is what v5 itself replied on the same
training episodes (`prefs.py`). So the two methods differ only in how they
use the targets, not in what the targets say.

- **Buys:** a clean answer to "do preferences fix this better than
  retraining?", and the grounded answer rules score both the same way.
- **Costs:** the pairs only constrain the turns they are on. Round 1's
  pairs were final turns, and it replied instead of calling on the call
  turns before them. Round 2 added call pairs (the right call over a sampled
  mistake) and called on requests that need no tool; round 3 added abstain
  pairs (the training reply over an unneeded call) and stopped calling, in
  proportion to the ratio of abstain to call pairs. The mix of pair kinds
  becomes a knob that sets the call rate. SFT on whole episodes (v6) has no
  such knob, which is why it is the default.
- **Rejected sides are sampled when greedy is too right.** On its own
  training data a model is almost never wrong greedy (round-1 DPO: 24 of
  2254 call turns), so `sample.py` draws 4 samples at temperature 1 and
  keeps the first mistake. The rejected side stays what the model would
  actually say.
- **The reference is v5 itself.** The DPO LoRA is trained on the merged v5
  and the reference is the same weights with the adapter off, so the KL term
  keeps DPO near v5, not near the base model.

## Reproducing

```sh
make -C ../cMCP && make -C judge
pip install -e '.[train,dev]'                 # after the PyTorch build for your GPU
scripts/snapshot_tools.sh && python -m toolcall.data
llama-server -hf Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q8_0 --port 8083 -ngl 99 -c 8192 -np 1 &
python -m toolcall.evaluate --name 1.5b-free --model Qwen/Qwen2.5-1.5B-Instruct
python -m toolcall.distill  --model Qwen/Qwen2.5-1.5B-Instruct
# stop the server: training needs the GPU memory
python -m toolcall.train    --model Qwen/Qwen2.5-1.5B-Instruct --out models/ft
python -m toolcall.export   --model Qwen/Qwen2.5-1.5B-Instruct --adapter models/ft
llama-server -m models/ft-q8_0.gguf --port 8083 -ngl 99 -c 8192 -np 1 &
python -m toolcall.evaluate --name ft-free --model Qwen/Qwen2.5-1.5B-Instruct
python scripts/compare.py 1.5b-free ft-free
```

v6, with the episodes and the grounded final replies, and its episode sets:

```sh
python -m toolcall.train    --model Qwen/Qwen2.5-1.5B-Instruct --out models/ft-v6 --multistep --grounded
python -m toolcall.export   --model Qwen/Qwen2.5-1.5B-Instruct --adapter models/ft-v6
llama-server -m models/ft-v6-q8_0.gguf --port 8083 -ngl 99 -c 8192 -np 1 &
python -m toolcall.evaluate --name mtg-ft-v6-free  --model Qwen/Qwen2.5-1.5B-Instruct --splits mt_test_id_g,mt_test_ood_g
python -m toolcall.evaluate --name hand7-ft-v6-free --model Qwen/Qwen2.5-1.5B-Instruct --splits test_hand7
```

DPO from v5 (`models/ft-v5`, trained with `--multistep`), round 1; rounds 2
and 3 add `--calls-from` and `--abstain-from` runs made by `toolcall.sample`:

```sh
python -m toolcall.export   --model Qwen/Qwen2.5-1.5B-Instruct --adapter models/ft-v5   # -> models/ft-v5-merged
llama-server -m models/ft-v5-q8_0.gguf --port 8083 -ngl 99 -c 8192 -np 1 &
python -m toolcall.evaluate --name onpolicy-v5 --model Qwen/Qwen2.5-1.5B-Instruct --splits train,mt_train
python -m toolcall.prefs    --run onpolicy-v5 --out data/prefs_v5.jsonl
# stop the server
python -m toolcall.dpo      --start models/ft-v5-merged --out models/dpo --prefs data/prefs_v5.jsonl
python -m toolcall.export   --model models/ft-v5-merged --adapter models/dpo
```
