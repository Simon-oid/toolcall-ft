# Architecture

How toolcall-ft is put together, and why. The numbers are in the README;
this is the design.

## The pipeline

```
 cMCP servers ──snapshot_tools.sh──► data/tools.json (6 tools, their inputSchemas)
                                           │
 data.py (seeded generator) ──► train / val / test_id / test_ood     test_hand, test_hand2
        │                                  │                          (written by hand)
        │ distill.py: base model           │
        │ answers the chit-chat            ▼
        ▼                          prompt.py: the model's own chat template + tools
 train.py: LoRA, loss on the               │
 completion only                           ▼
        │                          llama.cpp server (GGUF), one request at a time
        ▼                                  │ raw text
 export.py: merge ► GGUF Q8_0 ─────────────┤
                                           ▼
                          score.py ◄── judge/judge.c (cMCP's parser + schema validator)
                                           │
                          evaluate.py ► results/<run>/results.jsonl, report.md
                          scripts/compare.py (paired), scripts/summarize.py
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
| `test_hand`, `test_hand2`: written by hand | did it learn the generator's style and not the task? |

- **Hygiene, enforced by tests:**
  - no test request or test value appears in training;
  - evaluation splits never repeat a request, since repeats would narrow the
    intervals falsely;
  - CI regenerates the data and requires it to match the committed files.
- **A test read for error analysis stops being a test.** `test_hand` was
  used to decide what v2 should fix. So `test_hand2` was written and
  committed before v2 was trained: the commit order is the evidence that it
  is blind.

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
