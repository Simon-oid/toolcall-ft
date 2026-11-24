# toolcall-ft

[![CI](https://github.com/Simon-oid/toolcall-ft/actions/workflows/ci.yml/badge.svg)](https://github.com/Simon-oid/toolcall-ft/actions/workflows/ci.yml)
[![Coverage ≥80%, gated in CI](https://img.shields.io/badge/coverage-%E2%89%A580%25%20gated-brightgreen)](https://github.com/Simon-oid/toolcall-ft/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Simon-oid/toolcall-ft)](https://github.com/Simon-oid/toolcall-ft/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](pyproject.toml)

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

![toolcall-ft demo: five requests sent to the base model and to the fine-tuned one, each call judged by cMCP's validator](docs/demo.gif)

**Result: after LoRA fine-tuning, the 1.5B model makes the right call as often
as the 7B, and as a hosted 120B, and knows much better when not to call.**

| | right call, held-out phrasings | right call, hand-written (2 sets) | abstains when it should, held-out |
|---|---|---|---|
| Qwen2.5-1.5B base | 0.70 [0.63, 0.76] | 0.69 · 0.84 | 0.55 |
| Qwen2.5-7B base | 0.90 [0.86, 0.94] | 0.87 · 0.91 | 0.60 |
| gpt-oss-120b, hosted, reasoning low | 0.89 [0.84, 0.93] | 0.95 · 0.88 | 0.79 [0.71, 0.87] |
| **Qwen2.5-1.5B + LoRA (v2)**, seed 0 | **0.92** [0.88, 0.96] | **0.95 · 0.91** | **0.99** |
| same recipe, 3 seeds: mean ± sd | 0.92 ± 0.05 | 0.97 ± 0.01 · 0.91 ± 0.00 | 0.97 ± 0.04 |
| **v3**, 3 seeds: mean ± sd | **0.96 ± 0.01** | 0.95 ± 0.03 · 0.92 ± 0.05 | 0.94 ± 0.04 |
| **v4**, 3 seeds: mean ± sd | 0.95 ± 0.01 | 0.91 ± 0.03 · 0.96 ± 0.02 | **0.99 ± 0.01** |
| **v5** (+ multi-step), 3 seeds | 0.94 ± 0.04 | 0.93 ± 0.04 · 0.96 ± 0.05 | **1.00 ± 0.01** |
| **v6** (+ grounded replies), 3 seeds | 0.94 ± 0.03 | 0.96 ± 0.01 · 0.99 ± 0.02 | 0.98 ± 0.01 |
| DPO from v5, 3 seeds | 0.92 ± 0.05 | 0.85 ± 0.08 · 0.92 ± 0.07 | 1.00 ± 0.01 |
| DPO round 2 (+ call pairs), 3 seeds | 0.89 ± 0.09 | 0.84 ± 0.08 · 0.90 ± 0.13 | 0.30 ± 0.45 |

**Multi-step and multi-turn (v5, v6).** Chaining calls, such as listing a folder
and then reading the right file, or resolving "how big is it?" after a read:

| episodes right, teacher-forced | generated, held-out phrasings | by hand, set 1 (32 episodes) | by hand, set 2 (30, blind) |
|---|---|---|---|
| Qwen2.5-1.5B base | 0.27 | 0.22 | 0.23 |
| Qwen2.5-7B base | 0.66 | 0.44 | 0.47 |
| v4, 3 seeds | 0.35 ± 0.03 | 0.25 ± 0.03 | |
| **v5**, 3 seeds | **0.90 ± 0.03** | 0.40 ± 0.07 | 0.47 ± 0.03 |
| v6, 3 seeds | 0.86 ± 0.02 | 0.45 ± 0.08 | 0.44 ± 0.04 |
| DPO from v5, 3 seeds | 0.81 ± 0.01 | 0.46 ± 0.02 | 0.50 ± 0.07 |
| DPO round 2, 3 seeds | 0.73 ± 0.10 | 0.28 ± 0.12 | 0.30 ± 0.09 |

v5's calls inside an episode are as good as the 7B's. Its final answers are
not: it learned the generator's terse replies and often leaves out the value
the user asked for ([below](#v5-multi-step-and-multi-turn)). v6 and DPO fix
part of that (the value reaches the reply in 0.59 → 0.68 and 0.73 of set 2's
final turns, the 7B 0.70), but whole episodes do not move, and DPO costs
calls ([below](#v6-and-dpo-final-replies-that-report-the-value)). A second
DPO round with pairs on the call turns overshot: it calls on requests that
need no tool.

How these were measured:
- the Qwen models run as GGUF on llama.cpp, free greedy decoding;
- gpt-oss-120b runs on Groq's free tier with native tool calling, temperature
  0, `reasoning_effort: low` (13.7 reasoning tokens per request on average),
  graded by the same scorer and C judge ([below](#a-hosted-120b-baseline));
- the intervals are 95% bootstrap; "± sd" is across three training seeds;
- the hand-written sets have 54 and 48 cases, so their intervals are wide.

Details, paired tests and failures are in [Fine-tuning](#fine-tuning).
Every number here comes from a script, with its hardware and date.

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
| gpt-oss-120b, hosted API, reasoning low | 0.89 [0.84, 0.93] | 0.79 | 0.92 |

### A hosted 120B baseline

`python -m toolcall.evaluate --api-model openai/gpt-oss-120b --reasoning-effort low`
(key in `$TOOLCALL_API_KEY`, never a flag) sends each case to an
OpenAI-compatible API with the six tools as native `tools`
([`src/toolcall/api_backend.py`](src/toolcall/api_backend.py)). It is a
different runtime as well as a different model, so read the gap to the local
rows as both. Its failures on test_ood, by kind:

- **Right call: a tie, and most misses are a convention.** 9 of its 11 wrong
  arguments are `k: 10` on `crag_search` where the request asked for no count
  and the test expects the default 5. Counting those right gives 0.94, level
  with the fine-tuned 1.5B (0.92 ± 0.05 over seeds). The fine-tuned model
  learned the dataset's conventions; the 120B did not see them.
- **Abstention: a real gap.** It calls a tool in 22 of the 105 requests it
  should refuse (fine-tuned: 1 to 9 across seeds). Most are first steps
  toward a task the tools cannot finish ("translate and save" → `fs_read`).
  Four are worse: "erase this file", with no delete tool, becomes `fs_write`
  with empty content, which truncates the file.
- 2 of 474 calls were rejected by the provider as invalid (a tool not in the
  request); they are scored from the raw generation, as wrong calls.

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

## Fine-tuning

**The training.**
- Qwen2.5-1.5B-Instruct, LoRA r=16 (α 32) on all linear layers, bf16.
- 2 epochs over the 1527 training cases, effective batch 16, lr 2e-4 cosine.
- 192 steps in 26 minutes on the RX 7800 XT; validation loss 0.024 → 0.014.
- The prompt is rendered exactly as at evaluation, and the loss is on the
  completion only ([`src/toolcall/train.py`](src/toolcall/train.py)).

**Serving it.** The adapter is merged into the weights and converted with
llama.cpp's own converter to Q8_0, the base model's quantization
([`src/toolcall/export.py`](src/toolcall/export.py)). It is then served and
evaluated exactly like the baselines.

Paired against the base model, on the same cases
([`scripts/compare.py`](scripts/compare.py)):

| test_ood (held-out phrasings) | new − base [95% CI] | fixed | broken | McNemar p |
|---|---|---|---|---|
| right call (189 cases) | +0.21 [+0.15, +0.28] | 43 | 3 | 5e-10 |
| abstains when it should (105) | +0.37 [+0.27, +0.48] | 42 | 3 | 9e-10 |

Against the 7B on test_ood:
- right call: +0.005 [−0.05, +0.06], 15 fixed and 14 broken, a tie;
- abstention: +0.32 [+0.22, +0.43].

**A hand-written test set.** `test_ood` comes from the same generator as the
training data: its phrasings are new, but its style is not. So
[`data/test_hand.jsonl`](data/test_hand.jsonl) holds 54 requests written by
hand, in the way people type:
- chatty, terse, or with a reason attached ("I want to cook tonight");
- `pls`, `u`, `lol`, a greeting in Italian;
- file and folder names the generator never uses.

The labels follow the real server's rules, and a test checks each one with
cMCP's validator.

| test_hand (39 need a call, 15 need none) | right call [95% CI] | abstains when it should |
|---|---|---|
| 1.5B base | 0.69 [0.54, 0.82] | 0.60 |
| 7B base | 0.87 [0.77, 0.97] | 0.87 |
| 1.5B + LoRA | 0.90 [0.79, 0.97] | 0.93 |

- **Against the base 1.5B:** +0.21 on right calls, 9 cases fixed and 1
  broken, p = 0.02. The gain holds outside the generator's style.
- **Against the 7B:** a tie (4 fixed, 3 broken).
- **On abstention:** the 7B abstains much better here than on the
  synthetic set, so the fine-tuned model's lead is smaller. With 15 cases it
  is not significant.

**Where v1 failed** (25 of 294 on test_ood, 5 of 54 by hand), which v2
then addressed:
- **`crag_stats` taken for `fs_stat`.** "Report the size of the document
  index." becomes `fs_stat {"path": "index"}`. The base model makes the same
  mistake.
- **`limit` dropped on unusual phrasings** of "the first N lines" or "line
  8", where only `offset` is set. The dataset needs more of these.
- **The fixed refusal sentence leaks.** "What does research contain?" gets
  "I can't search the web: my tools can only…".
  - The model learned the refusal *template* and applies it where it does
    not belong. It sometimes even garbles it ("inspect and inspect").
  - That is the cost of training refusals on one fixed sentence. Varied
    refusals, like the distilled chit-chat replies, would be the fix.
- **A search query that loses the user's key word** ("supported keywords"
  without "schema").

**v2: fixing the two systematic failures.** The v1 errors pointed to two
gaps in the training data, and v2 fills them:
- refusals and clarifying questions now come in four wordings each;
- 160 extra training reads cover "the first N lines" in new wordings, and a
  single line.

Every test case stays byte-identical: the new cases come from their own
random stream, and the wordings are picked by a hash of the request. A
second hand-written set, `test_hand2` (48 cases), was committed *before*
v2 was trained. `test_hand` had been used to analyse v1's errors, so it is
no longer a clean test for v2.

Paired, v2 against v1:

| | v1 | v2 | fixed / broken |
|---|---|---|---|
| line-range reads right (test_ood) | 20/24, `limit` dropped 4× | 23/24, dropped 0× | |
| abstains when it should (test_ood) | 0.92 | 0.99 | 7 / 0, McNemar p 0.016 |
| `crag_stats` (test_ood) | 8/14 | 14/14 | |
| right call (test_ood) | 0.91 | 0.92 | 12 / 10, a tie |
| test_hand2, right call · abstains | 0.91 · 1.00 | 0.91 · 1.00 | 1 / 1 |

Against the 7B on test_ood, v2 is:
- level on right calls: +0.016 [−0.03, +0.06];
- far ahead on abstention: +0.39 [+0.30, +0.49], 42 cases fixed against 1.

**What v2 still gets wrong.** It fails 16 of 294 test_ood cases.
- **"What does research contain?"** accounts for 9 of them. The request
  never says that `research` is a folder, so the model reads it as a
  file, searches the docs, or asks.
  - The fixed refusal no longer leaks there. The opener of a clarifying
    question does instead: "I can do that once I know more…".
  - The leak moved from one template to another rather than disappearing.
- **"Run a retrieval on X. Just the single best hit."** The model searches
  for `"the single best hit"` and loses the topic.

**v3: folders and trailing instructions.** v3 adds 140 training cases for
the two failures above, and changes nothing else:
- 80 `fs_list` requests that name a bare folder ("what does research
  contain?");
- 60 `crag_search` requests where a constraint follows a closed sentence
  ("… please. Just the single best hit.").

None of their wordings appears in a test set. A third hand-written set,
[`data/test_hand3.jsonl`](data/test_hand3.jsonl) (48 cases), was committed
before v3 was trained. Both versions were trained with the same three seeds
and compared seed by seed:

| | v2, 3 seeds | v3, 3 seeds | fixed / broken, pooled |
|---|---|---|---|
| right call (test_ood) | 0.92 ± 0.05 | **0.96 ± 0.01** | 29 / 6 |
| bare-folder `fs_list` (test_ood, 15 cases) | 6 of 15 on average | 14 of 15 | |
| query replaced by "the single best hit" | 4 in 3 runs | 2 in 3 runs | |
| right call (test_hand3, blind) | 0.89 | **0.97** | 8 / 0 |
| abstains when it should (test_ood) | 0.97 ± 0.04 | 0.94 ± 0.04 | 2 / 10 |
| abstains when it should (test_hand3) | 0.88 | 0.88 | 1 / 1 |

"Pooled" adds the three seeds' paired changes, so a case counts once per
seed; per seed, v3's gain on test_ood right calls is +0.05, +0.07 and
+0.00 (McNemar p 0.01, 0.0005, 1).
- **The folder failure is fixed** in all three seeds, and the right-call
  rate no longer swings with the seed (sd 0.05 → 0.01).
- **It costs some abstention on ambiguous requests.** The 10 broken cases
  are "find the part about that in the docs", searched as `"that"`, and
  "fill drafts/outline.py in", answered with invented content. v3 taught
  the model to call more readily, and no ambiguous counterpart was added
  to balance it. That is the next data change.
- **The trailing-instruction failure is only halved,** and on the older
  hand-written sets the two versions are level within their intervals.

**v4: asking instead of guessing.** v4 adds 140 training cases, all
ambiguous, and changes nothing else: requests shaped like v3's new cases
but with the deciding argument missing (a listing with no folder, a search
with no topic, a write with no file or no content), each answered with a
clarifying question. The evaluation splits are byte-identical, and the
three seeds are the same as v2's and v3's.

Two hand-written sets measure it, and they disagree on how much:
- [`data/test_hand4.jsonl`](data/test_hand4.jsonl) (40 cases, 16 ambiguous)
  was committed before v4 was trained, but written together with the v4
  training data, so it shares their idea of what an ambiguous request is.
- [`data/test_hand5.txt`](data/test_hand5.txt) (39 cases, 14 ambiguous) was
  written from a one-page brief, the tools and the case types only, by
  someone who had not seen `data.py`, the v4 cases or test_hand4. It was
  committed before any model saw it, and
  [`toolcall.handset`](src/toolcall/handset.py) converts it to JSONL.

| | v3, 3 seeds | v4, 3 seeds | fixed / broken, pooled |
|---|---|---|---|
| abstains when it should (test_ood) | 0.94 ± 0.04 | **0.99 ± 0.01** | 19 / 2 |
| abstains when it should (test_hand5, independent) | 0.80 ± 0.06 | **0.89 ± 0.00** | 5 / 0 |
| abstains when it should (test_hand4, written with the data) | 0.67 ± 0.06 | 0.92 ± 0.06 | 15 / 0 |
| right call (test_ood) | 0.96 ± 0.01 | 0.95 ± 0.01 | 6 / 13 |
| right call (test_hand5) | 0.94 ± 0.03 | 0.92 ± 0.03 | 0 / 1 |
| right call (test_hand) | 0.95 ± 0.03 | 0.91 ± 0.03 | 0 / 5 |

Per-seed paired tests are in
[`results/compare-v3-v4/`](results/compare-v3-v4/).
- **It asks more, on every set.** No seed abstains worse than v3 on any
  set, and v4 asks on 12 of test_hand5's 14 ambiguous requests in all
  three seeds, where v3 varied with the seed (9 to 11).
- **How much depends on who wrote the test.** On test_hand5 the gain in
  abstention is +0.06, +0.06 and +0.17 per seed. That is a third to a half of
  test_hand4's +0.15, +0.25 and +0.35. The independent set is the number to
  quote.
- **It costs a little precision on clear requests.** Right calls fall by
  0.01–0.02 on test_ood in every seed, each interval including zero, and on
  test_hand seeds 1 and 2 break 5 calls and fix none. The broken calls lose
  a detail rather than pick the wrong action: no `limit` for "the first 3
  lines", `limit 30` for lines 100 to 120, `fs_list` for "is photos/2026 a
  directory?". v4 learned caution, and some of it spills onto requests that
  were clear.

### v5: multi-step and multi-turn

Up to v4, every case is one request and one call. v5 adds episodes
([`src/toolcall/episodes.py`](src/toolcall/episodes.py)): a conversation in
which the model must make several calls in a row, each depending on the
previous result, or answer a follow-up that refers to an earlier turn.
- **Ten kinds.** Find a file then read it, check it exists then read it,
  search the docs then save the answer, list then write, check the index
  then search; and follow-ups to a read: "read it", "how big is it?",
  "save that", an unresolvable "that one" (to be asked about), and thanks.
- **Results look like the servers'.** Each tool result is rendered in the
  real server's format, from a small in-memory file tree and corpus
  ([`src/toolcall/corpus.py`](src/toolcall/corpus.py)). A test runs 60
  episodes against the real `filesystem-mcp` and requires byte-identical
  output.
- **Scored one turn at a time, with the right history** (teacher forcing).
  A call turn is judged on the four levels. A final turn must make no call,
  and its reply must contain the fact the tool returned (a size, a line,
  the file written). An episode is right only if every turn is.
- **Same hygiene as the single-turn data.** A separate seed and separate
  files, so v1–v4's data stay byte-identical. Held-out phrasing families
  and unseen file names and topics in the test splits.
- **Training.** v4's data plus 1,409 episode turns: 3,376 cases, 2 epochs,
  422 steps in 63 minutes per seed. Same three seeds as v2–v4.

[`data/test_hand6.txt`](data/test_hand6.txt) (32 episodes, 74 scored turns)
was written by hand from a brief by someone who had not seen the generator,
and committed before any v5 result was opened. The text format is converted
by [`toolcall.handset_mt`](src/toolcall/handset_mt.py).

| 3 seeds, mean ± sd | v4 | v5 | fixed / broken, pooled |
|---|---|---|---|
| episodes right, generated held-out | 0.35 ± 0.03 | **0.90 ± 0.03** | |
| episodes right, test_hand6 | 0.25 ± 0.03 | **0.40 ± 0.07** | |
| right call inside an episode, test_hand6 | 0.36 ± 0.05 | **0.68 ± 0.01** | 47 / 6 |
| no call when none is due, test_hand6 | 0.81 ± 0.03 | 0.92 ± 0.04 | 12 / 2 |
| final reply carries the fact, generated held-out | 0.78 ± 0.02 | 1.00 ± 0.00 | 106 / 0 |
| final reply carries the fact, test_hand6 | 0.57 ± 0.03 | 0.52 ± 0.08 | 12 / 16 |

Per-seed paired tests are in
[`results/compare-v4-v5/`](results/compare-v4-v5/).
- **It learned to chain calls.** Inside test_hand6's episodes the right
  call rises from 0.36 to 0.68 in every seed (McNemar p ≤ 0.005 per seed):
  28–29 of 42, against the 7B's 26. It calls `fs_list` before guessing a file name
  and `fs_stat` for "how big is it?".
- **The generated test overstates the gain about twice.** 0.90 of the
  generated episodes are right, 0.40 of the hand-written ones, the same
  pattern test_hand4 and test_hand5 showed for v4.
- **It learned the generator's final replies.** On the hand-written set its
  answers are worse than v4's (16 broken, 12 fixed). After a write it says
  "It's in notes/overlap.txt now." and drops the value it computed or saved
  (64, 763, 6). After a read it pastes the file instead of answering the
  question. The generator's replies only ever name the file, so the model
  never saw a reply that reports the value. The 7B, untrained, gets these
  right.
- **What no model handles.** An index with 0 chunks, then "search it for
  deployment": all eight models search. A file already reported missing,
  asked about again: all but the base 1.5B call `fs_stat`.
- **Single-turn results hold.** On test_ood, right calls 0.95 → 0.94
  (10 fixed, 16 broken, no seed significant; seed 1 loses 7 more than it
  gains: "after line N" read as `offset N`, and "what does research
  contain?" sent to `crag_search`). Abstention 0.99 → 1.00.
  On the hand-written sets 1–5 no seed changes significantly.

### v6 and DPO: final replies that report the value

v5's defect is in its data: the generator's final replies only name the file.
Point 26 fixes the targets and compares two ways of teaching them.
- **Grounded targets** ([`src/toolcall/grounded.py`](src/toolcall/grounded.py)).
  Only the final turn of four episode kinds changes. After a save the reply
  quotes what was written ("Saved to notes/a.md. It says: …"); after a
  check-then-read it gives the size and the contents. Their answer rules now
  ask for those values, and a test checks that every old reply fails them.
  231 of the training episodes change.
- **v6 (SFT).** v5's recipe on the grounded episodes, from the base model,
  same three seeds.
- **DPO from v5** ([`prefs.py`](src/toolcall/prefs.py),
  [`dpo.py`](src/toolcall/dpo.py)). v5 answered every training episode
  (on-policy: right on all 3,376 turns under the old rules). Each final reply
  that fails the grounded rule becomes a pair, the grounded reply chosen and
  v5's own rejected: 231 pairs per seed. TRL's DPOTrainer trains a new LoRA on
  the merged v5 (beta 0.1, 2 epochs, 30 steps, 12 minutes); the reference is
  v5 itself.

test_hand6 stopped being an independent judge when the fix was designed by
reading its failures. So [`data/test_hand7.txt`](data/test_hand7.txt)
(30 episodes, 66 scored turns) was written by hand from a new brief, knowing
the defect but not the generator, and committed before any v6 or DPO result
was opened. It is the number to quote.

| 3 seeds, mean ± sd | 7B | v5 | v6 | DPO | vs v5, fixed / broken pooled: v6 · DPO |
|---|---|---|---|---|---|
| final reply carries the value, test_hand7 | 0.70 | 0.59 ± 0.00 | 0.68 ± 0.11 | **0.73 ± 0.04** | 12 / 5 · 12 / 1 |
| right call inside an episode, test_hand7 | 0.56 | **0.68 ± 0.04** | 0.64 ± 0.03 | 0.64 ± 0.12 | 3 / 8 · 3 / 8 |
| episodes right, test_hand7 | 0.47 | 0.47 ± 0.03 | 0.44 ± 0.04 | **0.50 ± 0.07** | 5 / 7 · 7 / 4 |
| final reply carries the value, test_hand6 | 0.73 | 0.52 ± 0.08 | 0.62 ± 0.11 | 0.71 ± 0.04 | 16 / 7 · 22 / 5 |
| final reply carries the value, generated held-out | 0.74 | 0.51 ± 0.00 | **1.00 ± 0.00** | 0.85 ± 0.06 | 234 / 2 · 168 / 4 |
| right call inside an episode, generated held-out | 0.79 | **0.91 ± 0.02** | 0.88 ± 0.02 | 0.84 ± 0.03 | 18 / 43 · 4 / 58 |
| calls when it should, single-turn test_ood | | **0.98 ± 0.01** | **0.98 ± 0.01** | 0.93 ± 0.04 | |

The generated rows use the grounded answer rules. Per-seed tests are in
[`results/compare-v5-v6-dpo/`](results/compare-v5-v6-dpo/), from
[`scripts/pooled.py`](scripts/pooled.py).
- **Both fix the reply a little on the blind set.** The value reaches the
  final reply in 0.68 (v6) and 0.73 (DPO) of test_hand7's final turns, up
  from 0.59 and level with the 7B. No seed is significant on 27 turns (best
  p = 0.06). Pooled over seeds, DPO fixes 12 and breaks 1.
- **Neither moves whole episodes.** test_hand7's episodes stay at 0.44–0.50,
  where v5 and the 7B are. The calls each breaks cancel the replies it fixes.
- **The generated test overstates the gain again.** On generated held-out
  episodes v6 reports the value in every final reply, DPO in 0.85; on
  test_hand7, 0.68 and 0.73.
- **DPO learned to talk where its pairs were.** Every pair was a final turn,
  and nothing held the call turns before them in place. On generated
  episodes it breaks 58 calls and fixes 4. In 49 of the 58 breaks over the
  three seeds it replies instead of calling, early in the same
  kinds of episode the pairs came from: "I can do that once I know more. What should I
  write in scripts/results.toml?". It also calls less on single requests
  (0.98 → 0.93 on test_ood, right calls on test_hand 0.93 → 0.85). v6,
  trained on whole episodes, breaks fewer calls and keeps single-turn as v5.
- **A new mistake in both.** After `fs_stat` reports a directory, four of
  the six v6 and DPO runs say "archive exists and is empty." instead of
  listing it. The grounded check-then-read replies taught them to answer
  right after a stat.
- **Which to keep.** v6 is the safer default: same single-turn and askdocs
  results as v5 or better (below), and the best generated episodes. DPO
  gives the best replies on the blind set at the cost of calls.

**DPO round 2: pairs on the call turns too.** Round 1's pairs were all final
turns, so round 2 adds pairs on the call turns of the same training data:
the right call chosen, a mistake of round-1 DPO rejected. Greedy, round-1
DPO gets only 24 of the 2254 training call turns wrong, so the mistakes were
sampled ([`sample.py`](src/toolcall/sample.py): 4 samples at T=1, the first
wrong one kept): 181, 189 and 24 call pairs by seed, on top of the 231
final-reply pairs. Seed 2's model was wrong that rarely even when sampled.
Training starts from v5 again, as in round 1.

| 3 seeds, mean ± sd | v5 | DPO r1 | DPO r2 | v5 → r2, fixed / broken pooled |
|---|---|---|---|---|
| right call inside an episode, generated held-out | **0.91 ± 0.02** | 0.84 ± 0.03 | 0.90 ± 0.02 | 22 / 28 |
| abstains when it should, single-turn test_ood | **1.00 ± 0.01** | **1.00 ± 0.01** | 0.30 ± 0.45 | 0 / 220 |
| abstains when it should, test_hand7 | 0.93 ± 0.00 | **0.94 ± 0.04** | 0.67 ± 0.15 | 0 / 24 |
| final reply carries the value, test_hand7 | 0.59 ± 0.00 | **0.73 ± 0.04** | 0.52 ± 0.07 | 9 / 15 |
| episodes right, test_hand7 | 0.47 ± 0.03 | **0.50 ± 0.07** | 0.30 ± 0.09 | 3 / 18 |

The calls came back to v5's level, and the model learned to call
everywhere. On test_ood seed 0 calls `crag_search` on 99 of 105 requests
that need no tool ("What does CPU stand for?"), and on test_hand7 most of
the final turns it gets wrong are another call instead of the reply. The
damage follows the number of call pairs: abstention on test_ood is 0.06,
0.02 and 0.82 for seeds 0, 1 and 2. Every call pair says "a call beats what
you said", and nothing in the set says "a reply beats a call" on a request
that needs no tool. A third round would need those abstain pairs too. On
askdocs (seed 0) it keeps the base's level: key facts 0.53, wrong refusals
0.16, faithfulness 0.88. Per-seed tests are in
[`results/compare-dpo2/`](results/compare-dpo2/). v6 stays the default.

**Does it still answer questions?** Training a model to call tools can cost
it its general ability. So the base and the fine-tuned 1.5B answered
[askdocs](https://github.com/Simon-oid/askdocs)' 45 evaluation questions,
which need grounded, cited answers and no tool calls, with the same
retrieval. A 7B judged faithfulness. Reports are in
[`results/askdocs-forgetting/`](results/askdocs-forgetting/).

| askdocs eval | base 1.5B | fine-tuned v1 | fine-tuned v2 | v2 − base [95% CI] |
|---|---|---|---|---|
| key facts | 0.71 | 0.76 | 0.77 | +0.06 [−0.04, +0.18] |
| wrong refusals | 0.17 | 0.14 | 0.14 | −0.03 |
| correct refusals | 1.00 | 1.00 | 1.00 | 0 |
| faithfulness | 0.17 | 0.07 | 0.12 | −0.02 [−0.16, +0.11] |

askdocs' regression gate flags nothing for either version. The fine-tuning
did not cost the model its ability to answer from documents.

**v3 and v4 on askdocs.** Rerun on 2026-11-21 for the base, v3 and v4
(seed 0 each), same retrieval and judge
([`results/askdocs-forgetting-v4/`](results/askdocs-forgetting-v4/)).
askdocs itself changed since the table above, and the base model's
faithfulness moved from 0.17 to 0.79, so the two tables are not comparable.

| askdocs eval, 2026-11-21 | base 1.5B | v3 | v4 |
|---|---|---|---|
| key-fact recall | 0.49 | 0.60 | 0.50 |
| wrong refusals | 0.21 | 0.05 | 0.23 |
| correct refusals | 1.00 | 1.00 | 1.00 |
| faithfulness | 0.79 | 0.72 | 0.78 |

The gate flags nothing for either. But v3 refused answerable questions a
quarter as often as the base (0.05 against 0.21), and v4 gives that back
(0.23): the caution it learned for tool calls carries over to answering.
One seed per version, so this is a signal, not a measurement.

**v5 on askdocs.** Rerun on 2026-11-22 against the same base run (seed 0,
[`results/askdocs-forgetting-v5/`](results/askdocs-forgetting-v5/)): key-fact
recall 0.55, wrong refusals 0.16, correct refusals 1.00, faithfulness 0.89
(base 0.49, 0.21, 1.00, 0.79). The gate flags nothing. Training on episodes,
whose final replies quote tool results, did not cost the model its answering
from documents.

**v6 and DPO on askdocs.** Same base run, seed 0 each, 2026-11-23
([`results/askdocs-forgetting-v6/`](results/askdocs-forgetting-v6/)):

| askdocs eval | base 1.5B | v5 | v6 | DPO from v5 |
|---|---|---|---|---|
| key-fact recall | 0.49 | 0.55 | **0.66** | 0.56 |
| wrong refusals | 0.21 | 0.16 | **0.02** | 0.19 |
| faithfulness | 0.79 | **0.89** | 0.85 | 0.72 |

The gate flags nothing for either. v6, which learned to put the value it
read into its reply, almost never refuses an answerable question (1 of 43)
and recalls more key facts than the base (+0.17 [+0.05, +0.31]). DPO's
faithfulness is the lowest of the four, within the gate's noise. One seed
each.

**As askdocs' answering model.** The same run compares the fine-tuned model
with the 3B that askdocs uses by default
([`compose.local-model.yaml`](https://github.com/Simon-oid/askdocs/blob/main/compose.local-model.yaml)
serves any local GGUF):

| answering model | key facts | faithfulness | answer P50 |
|---|---|---|---|
| Qwen2.5-3B (askdocs' default) | 0.87 | 0.60 | 686 ms |
| Qwen2.5-1.5B + LoRA v2 | 0.77 | 0.12 | 445 ms |

It is a third faster and much worse at citing, as the base 1.5B is. So it is
not a replacement for the answering model: what the fine-tuning bought is
tool calling.

**How strict level 4 is.** Exact matching counts some harmless calls as
wrong. The 7B answered "dump the file" with `offset 1, limit 1000`, and wrote
`User-agent: *` with a trailing newline. Both are wrong here, by rule: an
argument the request did not ask for, or content that is not what was
dictated.

**Limits.** Three training seeds for v2 to v6 and for DPO, one for v1; askdocs
was checked on one seed of each version. Six fixed tools, English only.
Episodes are scored with the right history before each turn, so a model
that recovers from its own mistake is never tested. test_hand7 has 27
final turns with a value to report, too few for any one seed's change to
be significant. [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md) has the
full list, and [`docs/architecture.md`](docs/architecture.md) the design
decisions behind the measurement.

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

## Demo

[`scripts/demo.py`](scripts/demo.py) sends five hand-written requests to the
base model and to the fine-tuned one, side by side, and prints each call
with the validator's verdict (the recording at the top). In one run the base model miscounted a line
range (`limit 15` for lines 30 to 45), passed an argument `crag_stats` does
not take, and called a tool that does not exist (`fs_delete`). The
fine-tuned model got all five right.

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
