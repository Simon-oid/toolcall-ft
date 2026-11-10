# toolcall-ft

**Can a small open model call MCP tools as reliably as a large one?**
This repository fine-tunes a 1–3B model to call the tools of two real MCP
servers, and judges every call with the same code those servers run.

- **The tools** are those of [cMCP](https://github.com/Simon-oid/cMCP)'s reference servers: `crag-mcp`
  (`crag_search`, `crag_stats`, retrieval over a [cRAG](https://github.com/Simon-oid/cRAG)
  index) and `filesystem-mcp` (`fs_list`, `fs_read`, `fs_stat`, `fs_write`, inside a
  sandbox).
- **The judge** is cMCP's own JSON parser and JSON Schema validator, linked from C
  ([`judge/judge.c`](judge/judge.c)). A call that passes it is a call the server would
  accept. A call that fails it fails for the reason the server would give, such as
  `/limit: minimum` or `/top: additionalProperties`.

Status: the judge, the scoring, the dataset and the baselines are done.
Fine-tuning and serving come next. Every number here comes from a script,
with its hardware and date.

## How a call is scored

Each level counts only if the ones before it passed:

| Level | Passes when | Decided by |
|---|---|---|
| 1 json | the call parses to `{"name": string, "arguments": object}` | cMCP's parser (C) |
| 2 schema | the tool exists and its arguments pass the tool's `inputSchema` | cMCP's validator (C) |
| 3 tool | it is the tool the request needs | the expected call |
| 4 args | every argument matches, and none is added | the expected call |

Level 4 is "the call is right".

**How arguments are matched.** Each case says how:
- `exact` by default, where `1`, `1.0` and `true` are all different, since the
  schema says integer;
- `any_of` for equivalent forms (`notes`, `notes/`, `./notes`; the server takes
  all three);
- `contains_all` for free text. A search query has no single right spelling,
  but it must carry the words the user asked about.

**Optional arguments.** An argument the request leaves to the server's default
(`k` for search, `offset` for "the first 20 lines") may be omitted, but not
given a wrong value.

**Requests that need no call** are scored on whether the model abstains:
- a general question (`no_tool`);
- an operation no tool does, like delete or email (`unsupported`);
- a request missing what the tool needs, like "Read the file." (`ambiguous`),
  where the right move is to ask.

## The dataset

Generated from intents × phrasing families × slot values, with a fixed seed
([`src/toolcall/data.py`](src/toolcall/data.py)):

| Split | Cases | Phrasing | Slot values (files, folders, topics, contents) |
|---|---|---|---|
| train | 1499 | families 0–5 | train pools |
| val | 181 | families 0–5 | train pools |
| test_id | 180 | families 0–5 | test pools, never seen in training |
| test_ood | 315 | families 6–7, held out | test pools |

`test_id` asks whether the model learned the task or memorised the names.
`test_ood` asks whether it learned the task or memorised the phrasings.

There are 9 intents (6 tools and 3 kinds of no-call), all present in every
split. The expected call is built from the slots, so it is right by
construction. The tests check it anyway:
- every training call passes cMCP's validator and scores 4/4 against its own
  case;
- no test request or test value appears in training;
- a sample of the `fs_*` calls runs on the real `filesystem-mcp` over a
  fixture tree without a tool error.

Training targets for calls use Qwen 2.5's `<tool_call>` markup. For no-call
cases they are:
- **`unsupported`:** a fixed sentence saying which operation no tool does;
- **`ambiguous`:** a fixed clarifying question;
- **`no_tool`:** the base model's own answer, generated before training, so
  training teaches *when* to call without rewriting how the model talks.

## Baselines

All models run through a llama.cpp server on the same machine (RX 7800 XT,
llama.cpp `a4d4f2f`, 2026-11-10). The prompt is rendered by the model's own
chat template with the six tools, and decoding is greedy. Each server has one
slot and gets one request at a time: two identical runs over the 474 test
cases gave **0** different replies, so a difference between rows is the
model, not noise. Full table with intervals:
[`results/summary.md`](results/summary.md).

The three decodings:
- **free:** the raw reply, judged as written;
- **eager:** the whole reply constrained to "a valid call or `{"name": "none"}`";
- **lazy:** llama.cpp's own tool path, a grammar built from the tools' schemas
  and applied only once the model starts a call.

| test_ood (189 need a call, 105 need none) | right call (L4) [95% CI] | abstains when it should | call/no-call decision |
|---|---|---|---|
| Qwen2.5-1.5B Q8_0, free | 0.70 [0.63, 0.76] | 0.55 | 0.84 |
| Qwen2.5-1.5B, eager | 0.69 | **0.00** | 0.64 |
| Qwen2.5-1.5B, lazy | 0.68 | 0.55 | 0.83 |
| Qwen2.5-3B Q4_K_M, free | 0.70 [0.64, 0.77] | 0.60 | 0.81 |
| Qwen2.5-7B Q4_K_M, free | **0.90** [0.86, 0.94] | 0.60 | 0.83 |
| Qwen2.5-7B, lazy | 0.84 [0.78, 0.89] | 0.61 | 0.83 |

What the baselines show:

- **The gap to close.** On held-out phrasings, the 7B gets 90% of calls
  right and the 1.5B 70%, with the intervals well apart. The 3B is no better
  than the 1.5B.
- **Constraining all output removes the choice not to call.** With the
  whole reply forced into JSON, the model never chose `none`: abstention
  went from 0.55 to 0.00. Once a JSON object has started, it always goes on
  with a tool name.
- **A grammar can drop arguments silently.**
  - The grammar llama.cpp derives from a schema fixes the key order:
    required first, then optional in schema order (`limit` before
    `offset`).
  - The 7B writes `offset` and then `limit`. After `offset` the grammar no
    longer allows `limit`, and the object closes.
  - On the 24 requests for a line range, the 7B got **22** right free and
    **4** right lazy, with `limit` dropped in 20.
  - Every one of those calls is valid (level 2) and wrong (level 4): it reads
    to the end of the file instead of the lines asked for.
  - Constraining guarantees the form, and can cost the content.
- **Constrained decoding does not choose the tool or the values.** At
  levels 3–4 the lazy grammar is within the noise of free decoding at best.
  The fine-tuning has to win there.
- **Abstention is weak for every model, and differs by kind.** The 1.5B
  makes a call on 60% of plain chit-chat (`no_tool`). The 7B makes a call on
  55% of requests for an operation no tool does (`unsupported`).

**Not done: a large model through an API.** The plan is a free-tier
provider. It needs an API key, and the backend for an OpenAI-compatible
endpoint is the next step.

## Training on an AMD GPU

[`scripts/rocm_smoke.py`](scripts/rocm_smoke.py) runs a few LoRA steps to
check that the machine can train before any plan relies on it. Measured on
2026-11-10 (RX 7800 XT 16 GB, ROCm 7.2, PyTorch 2.14.1+rocm7.2):

| | |
|---|---|
| Qwen2.5-1.5B-Instruct, LoRA r=16 on all linear layers, bf16 | loss 0.454 → 0.000 in 40 steps |
| throughput, batch 2 × 512, gradient checkpointing | 2415 tokens/s |
| peak memory | 9.8 GiB |
| same at batch 4 without checkpointing | out of memory |

The out-of-memory case is the logits: a 152k-token vocabulary makes the fp32
logits of 4 × 512 tokens 1.2 GB before their gradient.

## Run it

```sh
make -C ../cMCP && make -C judge          # cMCP (sibling checkout) and the judge
python -m venv .venv && .venv/bin/pip install -e '.[dev]'
scripts/snapshot_tools.sh                 # data/tools.json from the live servers
.venv/bin/python -m toolcall.data         # data/*.jsonl
.venv/bin/pytest -q
```

For training, install the PyTorch build for your GPU, then `pip install -e '.[train]'`.

## License

MIT
