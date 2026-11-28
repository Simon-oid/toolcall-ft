# Results, version by version

The detailed record behind the [README](../README.md)'s tables: what each
version changed, what it fixed, what it broke, and the paired tests. Every
number comes from a committed run in [`results/`](../results/); the paired
tests come from [`scripts/compare.py`](../scripts/compare.py) (one seed) and
[`scripts/pooled.py`](../scripts/pooled.py) (three seeds, McNemar per seed).

## v1: the first fine-tune

v1 is the recipe in the README's [Fine-tuning](../README.md#fine-tuning)
section, trained once on the 1527 single-request cases.
Paired against the base model, on the same cases
([`scripts/compare.py`](../scripts/compare.py)):

| test_ood (held-out phrasings) | new − base [95% CI] | fixed | broken | McNemar p |
|---|---|---|---|---|
| right call (189 cases) | +0.21 [+0.15, +0.28] | 43 | 3 | 5e-10 |
| abstains when it should (105) | +0.37 [+0.27, +0.48] | 42 | 3 | 9e-10 |

Against the 7B on test_ood:
- right call: +0.005 [−0.05, +0.06], 15 fixed and 14 broken, a tie;
- abstention: +0.32 [+0.22, +0.43].

**A hand-written test set.** `test_ood` comes from the same generator as the
training data: its phrasings are new, but its style is not. So
[`data/test_hand.jsonl`](../data/test_hand.jsonl) holds 54 requests written by
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

## v2: varied refusals and line ranges

The v1 errors pointed to two
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

## v3: folders and trailing instructions

v3 adds 140 training cases for
the two failures above, and changes nothing else:
- 80 `fs_list` requests that name a bare folder ("what does research
  contain?");
- 60 `crag_search` requests where a constraint follows a closed sentence
  ("… please. Just the single best hit.").

None of their wordings appears in a test set. A third hand-written set,
[`data/test_hand3.jsonl`](../data/test_hand3.jsonl) (48 cases), was committed
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

## v4: asking instead of guessing

v4 adds 140 training cases, all
ambiguous, and changes nothing else: requests shaped like v3's new cases
but with the deciding argument missing (a listing with no folder, a search
with no topic, a write with no file or no content), each answered with a
clarifying question. The evaluation splits are byte-identical, and the
three seeds are the same as v2's and v3's.

Two hand-written sets measure it, and they disagree on how much:
- [`data/test_hand4.jsonl`](../data/test_hand4.jsonl) (40 cases, 16 ambiguous)
  was committed before v4 was trained, but written together with the v4
  training data, so it shares their idea of what an ambiguous request is.
- [`data/test_hand5.txt`](../data/test_hand5.txt) (39 cases, 14 ambiguous) was
  written from a one-page brief, the tools and the case types only, by
  someone who had not seen `data.py`, the v4 cases or test_hand4. It was
  committed before any model saw it, and
  [`toolcall.handset`](../src/toolcall/handset.py) converts it to JSONL.

| | v3, 3 seeds | v4, 3 seeds | fixed / broken, pooled |
|---|---|---|---|
| abstains when it should (test_ood) | 0.94 ± 0.04 | **0.99 ± 0.01** | 19 / 2 |
| abstains when it should (test_hand5, independent) | 0.80 ± 0.06 | **0.89 ± 0.00** | 5 / 0 |
| abstains when it should (test_hand4, written with the data) | 0.67 ± 0.06 | 0.92 ± 0.06 | 15 / 0 |
| right call (test_ood) | 0.96 ± 0.01 | 0.95 ± 0.01 | 6 / 13 |
| right call (test_hand5) | 0.94 ± 0.03 | 0.92 ± 0.03 | 0 / 1 |
| right call (test_hand) | 0.95 ± 0.03 | 0.91 ± 0.03 | 0 / 5 |

Per-seed paired tests are in
[`results/compare-v3-v4/`](../results/compare-v3-v4/).
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

## v5: multi-step and multi-turn

Up to v4, every case is one request and one call. v5 adds episodes
([`src/toolcall/episodes.py`](../src/toolcall/episodes.py)): a conversation in
which the model must make several calls in a row, each depending on the
previous result, or answer a follow-up that refers to an earlier turn.
- **Ten kinds.** Find a file then read it, check it exists then read it,
  search the docs then save the answer, list then write, check the index
  then search; and follow-ups to a read: "read it", "how big is it?",
  "save that", an unresolvable "that one" (to be asked about), and thanks.
- **Results look like the servers'.** Each tool result is rendered in the
  real server's format, from a small in-memory file tree and corpus
  ([`src/toolcall/corpus.py`](../src/toolcall/corpus.py)). A test runs 60
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

[`data/test_hand6.txt`](../data/test_hand6.txt) (32 episodes, 74 scored turns)
was written by hand from a brief by someone who had not seen the generator,
and committed before any v5 result was opened. The text format is converted
by [`toolcall.handset_mt`](../src/toolcall/handset_mt.py).

| 3 seeds, mean ± sd | v4 | v5 | fixed / broken, pooled |
|---|---|---|---|
| episodes right, generated held-out | 0.35 ± 0.03 | **0.90 ± 0.03** | |
| episodes right, test_hand6 | 0.25 ± 0.03 | **0.40 ± 0.07** | |
| right call inside an episode, test_hand6 | 0.36 ± 0.05 | **0.68 ± 0.01** | 47 / 6 |
| no call when none is due, test_hand6 | 0.81 ± 0.03 | 0.92 ± 0.04 | 12 / 2 |
| final reply carries the fact, generated held-out | 0.78 ± 0.02 | 1.00 ± 0.00 | 106 / 0 |
| final reply carries the fact, test_hand6 | 0.57 ± 0.03 | 0.52 ± 0.08 | 12 / 16 |

Per-seed paired tests are in
[`results/compare-v4-v5/`](../results/compare-v4-v5/).
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

## v6 and DPO: final replies that report the value

v5's defect is in its data: the generator's final replies only name the file.
v6 fixes the targets, and the same targets are taught two ways.
- **Grounded targets** ([`src/toolcall/grounded.py`](../src/toolcall/grounded.py)).
  Only the final turn of four episode kinds changes. After a save the reply
  quotes what was written ("Saved to notes/a.md. It says: …"); after a
  check-then-read it gives the size and the contents. Their answer rules now
  ask for those values, and a test checks that every old reply fails them.
  231 of the training episodes change.
- **v6 (SFT).** v5's recipe on the grounded episodes, from the base model,
  same three seeds.
- **DPO from v5** ([`prefs.py`](../src/toolcall/prefs.py),
  [`dpo.py`](../src/toolcall/dpo.py)). v5 answered every training episode
  (on-policy: right on all 3,376 turns under the old rules). Each final reply
  that fails the grounded rule becomes a pair, the grounded reply chosen and
  v5's own rejected: 231 pairs per seed. TRL's DPOTrainer trains a new LoRA on
  the merged v5 (beta 0.1, 2 epochs, 30 steps, 12 minutes); the reference is
  v5 itself.

test_hand6 stopped being an independent judge when the fix was designed by
reading its failures. So [`data/test_hand7.txt`](../data/test_hand7.txt)
(30 episodes, 66 scored turns) was written by hand from a new brief, knowing
the defect but not the generator, and committed before any v6 or DPO result
was opened. It is the number to quote.

| 3 seeds, mean ± sd | 7B | v5 | v6 | DPO | vs v5, fixed / broken pooled: v6 · DPO |
|---|---|---|---|---|---|
| final reply carries the value, test_hand7 | 0.70 | 0.59 ± 0.00 | 0.68 ± 0.11 | **0.73 ± 0.04** | 12 / 5 · 12 / 1 |
| right call inside an episode, test_hand7 | 0.56 | **0.69 ± 0.04** | 0.64 ± 0.03 | 0.64 ± 0.12 | 3 / 8 · 3 / 8 |
| episodes right, test_hand7 | 0.47 | 0.47 ± 0.03 | 0.44 ± 0.04 | **0.50 ± 0.07** | 5 / 7 · 7 / 4 |
| final reply carries the value, test_hand6 | 0.73 | 0.52 ± 0.08 | 0.62 ± 0.11 | 0.71 ± 0.04 | 16 / 7 · 22 / 5 |
| final reply carries the value, generated held-out | 0.74 | 0.51 ± 0.00 | **1.00 ± 0.00** | 0.85 ± 0.06 | 234 / 2 · 168 / 4 |
| right call inside an episode, generated held-out | 0.79 | **0.91 ± 0.02** | 0.87 ± 0.02 | 0.84 ± 0.03 | 18 / 43 · 4 / 58 |
| calls when it should, single-turn test_ood | | **0.98 ± 0.01** | **0.98 ± 0.01** | 0.93 ± 0.04 | |

The generated rows use the grounded answer rules. Per-seed tests are in
[`results/compare-v5-v6-dpo/`](../results/compare-v5-v6-dpo/), from
[`scripts/pooled.py`](../scripts/pooled.py).
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
  results as v5 or better ([askdocs](#answering-documents-askdocs)), and the best
  generated episodes. DPO
  gives the best replies on the blind set at the cost of calls.

## DPO rounds 2 and 3: pairs on the other turns

Round 1's pairs were all final turns, and it broke the call turns before
them. Two more rounds added pairs on the other turns, each from v5 with the
same recipe:

- **Round 2: call pairs.** On the call turns of the training data, the right
  call chosen and a mistake of round-1 DPO rejected. Greedy, round-1 DPO gets
  only 24 of the 2254 training call turns wrong, so the mistakes were sampled
  ([`sample.py`](../src/toolcall/sample.py): 4 samples at T=1, the first wrong
  one kept): 181, 189 and 24 call pairs by seed, with the 231 final-reply pairs.
- **Round 3: abstain pairs too.** Round 2's model was sampled on the 615
  training turns that need no call (`sample.py --abstain`), and each call it
  made there became a pair, the training reply chosen: 505, 565 and 99 abstain
  pairs by seed, with round 2's pairs.

| 3 seeds | v5 | DPO r1 | DPO r2 (seeds 0 / 1 / 2) | DPO r3 (seeds 0 / 1 / 2) |
|---|---|---|---|---|
| abstains when it should, single-turn test_ood | 1.00 | 1.00 | 0.06 / 0.02 / 0.82 | 0.94 / 1.00 / 1.00 |
| right call inside an episode, generated held-out | 0.91 | 0.84 | 0.90 / 0.89 / 0.92 | 0.59 / 0.68 / 0.02 |
| right call inside an episode, test_hand7 | 0.69 | 0.64 | 0.67 / 0.64 / 0.72 | 0.33 / 0.53 / 0.03 |
| final reply carries the value, test_hand7 | 0.59 | 0.73 | 0.44 / 0.52 / 0.59 | 0.63 / 0.70 / 0.78 |
| episodes right, test_hand7 | 0.47 | 0.50 | 0.23 / 0.27 / 0.40 | 0.33 / 0.47 / 0.20 |

v5 and round 1 are means over the seeds; per-seed values and the paired tests
are in [`results/compare-dpo2/`](../results/compare-dpo2/) and
[`results/compare-dpo3/`](../results/compare-dpo3/).

- **Round 2 calls everywhere.** The calls came back to v5's level, and
  abstention collapsed: against v5, 220 abstentions broken and none fixed on
  test_ood. Seed 0 calls `crag_search` on 99 of the 105 requests that need no
  tool ("What does CPU stand for?"), and on test_hand7 most of the final turns
  it gets wrong are another call instead of the reply. Every call pair says "a
  call beats what you said", and nothing in the set says "a reply beats a
  call". The damage follows the number of call pairs: seed 2, with 24, loses
  least.
- **Round 3 hardly calls.** Abstention came back and the calls went: against
  v5, 371 calls broken and 5 fixed on the generated episodes. The damage
  follows the ratio of abstain pairs to call pairs (2.8, 3.0 and 4.1 to 1).
  Seed 2 answers "Run a retrieval on the soak test, please." with "Happy to
  help. What should I look up?". The rejected calls were real tool calls
  (`fs_write`, `crag_search`, `fs_list`), so DPO pushed those calls down
  everywhere: seed 0 answers 20 of test_ood's 35 `crag_search` turns with
  `crag_stats`.
- **What the three rounds show.** With DPO here, the mix of pair kinds sets
  how often the model calls. Final-reply pairs alone made it reply instead of
  calling, call pairs made it call everywhere, abstain pairs on top made it
  stop calling. Tuning the ratio until the test sets look right would be
  fitting it to them. v6, trained on whole episodes, has no such knob and
  stays the default.

## v7: the episode shapes the generator never made

v6's whole hand-written episodes stayed where v5's were (0.44–0.47 on
test_hand7). Reading test_hand6's and test_hand7's failures gave eight
families of episode the generator never produced, and v7 adds data for them.
- **A brief first, then a blind set.** [`data/test_hand8.txt`](../data/test_hand8.txt)
  (43 episodes, 90 scored steps) was written by hand from a brief naming the
  eight families and the right move in each, and committed before the
  generator. Its labels split it into the families (`f1_`–`f8_`, 2–3
  episodes each), shapes in none of them (`new_`, 13) and routine episodes
  (`base_`, 13). The check that no hand-written request is in the new
  training data reports counts only, so the set stayed unread until v7's
  three seeds were evaluated.
- **A second generator** ([`src/toolcall/rare.py`](../src/toolcall/rare.py)):
  twelve kinds (folders inside folders, search then read the source, a read
  that misses then a listing, a dead-end search, stopping when the history
  already answers, a size from a listing, read-edit-write, listing then stat,
  the next page of a log, a user who corrects the last call, checking a
  write), with grounded final replies, its own seed, pools disjoint between
  train and test, and subfolders in listings. 80 of its episodes run on the
  real `filesystem-mcp` byte for byte (directory sizes normalised).
- **Training.** v6's data plus 1756 `mt7_train` turns: 5132 examples, 2
  epochs, 642 steps in 98 minutes per seed, same three seeds.

| 3 seeds, mean ± sd | base 1.5B | 7B | v6 | v7 | fixed / broken, pooled |
|---|---|---|---|---|---|
| episodes right, test_hand8 (blind) | 0.30 | 0.42 | 0.48 ± 0.07 | **0.62 ± 0.01** | 25 / 7 |
| right call inside an episode, test_hand8 | | | 0.72 ± 0.04 | 0.81 ± 0.02 | 16 / 4 |
| no call when none is due, test_hand8 | | | 0.78 ± 0.05 | 0.86 ± 0.02 | 16 / 5 |
| final reply carries the value, test_hand8 | | | 0.66 ± 0.08 | 0.72 ± 0.02 | 16 / 9 |
| episodes right, test_hand7 | 0.23 | 0.47 | 0.44 ± 0.04 | 0.56 ± 0.02 | 14 / 4 |
| episodes right, test_hand6 | 0.22 | 0.44 | 0.45 ± 0.08 | 0.59 ± 0.05 | 20 / 6 |
| episodes right, `mt7_test_ood` (generated) | 0.13 | 0.30 | 0.20 ± 0.03 | 0.84 ± 0.03 | 463 / 4 |
| episodes right, `mt_test_ood` (v5's generated) | 0.27 | 0.66 | 0.86 ± 0.02 | 0.84 ± 0.06 | 36 / 45 |
| right call, single-turn test_ood | 0.70 | 0.90 | 0.94 ± 0.03 | 0.96 ± 0.02 | 16 / 6 |
| abstains when it should, test_ood | 0.55 | 0.60 | 0.98 ± 0.01 | 0.96 ± 0.01 | 1 / 6 |
| right call, test_hand2 | | | 0.99 ± 0.02 | 0.93 ± 0.02 | 0 / 6 |

By family on test_hand8 (episodes right, v6 → v7, three seeds pooled):

| read-edit-write | stop when the history answers | write then check | long chains | retry after a miss | pages | listing then stat | corrections | `new_` | `base_` |
|---|---|---|---|---|---|---|---|---|---|
| 0.00 → 1.00 | 0.00 → 0.67 | 0.83 → 1.00 | 0.00 → 0.17 | 0.00 → 0.00 | 0.33 → 0.17 | 0.83 → 0.67 | 0.50 → 0.50 | 0.49 → 0.56 | 0.72 → 0.79 |

Per-seed tests and the failures are in
[`results/compare-v6-v7/`](../results/compare-v6-v7/).
- **Whole episodes move on every hand-written set.** +0.14 on the blind
  test_hand8, +0.12 on test_hand7, +0.14 on test_hand6, in every seed, and
  above the 7B on all three. Only seed 0 is significant alone on test_hand8
  (p 0.013); the other two point the same way (8 / 3, 5 / 2).
- **The gain is where the data was.** Read-edit-write and stopping when the
  history already answers go from never to mostly right. Shapes nobody wrote
  data for move 0.49 → 0.56.
- **Retry after a miss is not learned** by any model measured. After a read
  reports a missing file, v7 says it does not exist instead of listing the
  folder; asked to search the docs for a setting, it guesses a file name
  (`wal_mode.txt`). The generator teaches both the retry and, when the user
  repeats a request after a miss, stopping, and the cues are close.
- **A new habit, from read-edit-write.** "replace the contents of keys.txt
  with: rotated" becomes `fs_read keys.txt` in all three seeds, where v6
  wrote it; "is exports a file or a folder?" gets `fs_list` in some seeds.
  These are most of test_hand2's 6 broken calls. v6's "archive exists and is
  empty." after a stat no longer appears.
- **The generated test overstates the gain most.** On `rare.py`'s own
  held-out phrasings episodes right go 0.20 → 0.84; on the blind hand-written
  set 0.48 → 0.62.

## v8: retrying after a miss, and its stop twins

On test_hand8, v7 never retried after a miss, and neither did the base, the 7B or GRPO.
v8 adds data for the retry and, beside each kind, a twin where the history
already answers, so that the model learns when not to retry.
- **A brief first, then a blind set.** [`data/test_hand9.txt`](../data/test_hand9.txt)
  (48 episodes, 125 scored steps) was written from a brief and committed
  (c9101bc, 40d4a27) before the generator (e8e577d): five retry parts
  (`r1_` missing file → list the folder, `r2_` empty search → a word from the
  conversation, `r3_` off-topic results → the term they point to, `r4_`
  search instead of guessing a file name, `r5_` listing without the file →
  its subfolder), eight `stop_` twins, eight `new_` and nine `base_`
  episodes. A blind checker printed only counts, errors and overlap with the
  training data (none, verbatim or by 6-gram).
- **A third generator** ([`src/toolcall/retry.py`](../src/toolcall/retry.py)):
  nine kinds, five retries and four stop twins, built from `rare.py`'s
  helpers, with aliases (another name for each topic, said earlier in the
  conversation) disjoint between train and test.
- **Training.** v7's data plus 1536 `mt8_train` turns: 6668 examples, 2
  epochs, 834 steps in 129 minutes per seed, same three seeds.

| 3 seeds, mean ± sd | base 1.5B | 7B | v7 | v8 | fixed / broken, pooled |
|---|---|---|---|---|---|
| episodes right, test_hand9 (blind) | 0.21 | 0.29 | 0.56 ± 0.03 | **0.61 ± 0.07** | 16 / 8 |
| right call inside an episode, test_hand9 | | | 0.80 ± 0.04 | 0.87 ± 0.03 | 22 / 6 |
| no call when none is due, test_hand9 | | | 0.83 ± 0.02 | 0.78 ± 0.01 | 2 / 9 |
| final reply carries the value, test_hand9 | | | 0.81 ± 0.04 | 0.80 ± 0.05 | 3 / 4 |
| episodes right, test_hand8 | 0.30 | 0.42 | 0.62 ± 0.01 | 0.65 ± 0.00 | 18 / 14 |
| episodes right, test_hand7 | 0.23 | 0.47 | 0.56 ± 0.02 | 0.52 ± 0.02 | 3 / 6 |
| episodes right, test_hand6 | 0.22 | 0.44 | 0.59 ± 0.05 | 0.58 ± 0.02 | 6 / 7 |
| episodes right, `mt8_test_ood` (generated) | 0.07 | 0.16 | 0.14 ± 0.03 | 0.92 ± 0.03 | 423 / 1 |
| episodes right, `mt7_test_ood` | 0.13 | 0.30 | 0.84 ± 0.03 | 0.84 ± 0.03 | 36 / 38 |
| episodes right, `mt_test_ood` | 0.27 | 0.66 | 0.84 ± 0.06 | 0.84 ± 0.00 | 29 / 30 |
| right call, single-turn test_ood | 0.70 | 0.90 | 0.96 ± 0.02 | 0.97 ± 0.01 | 9 / 6 |
| abstains when it should, test_ood | 0.55 | 0.60 | 0.96 ± 0.01 | 0.96 ± 0.01 | 2 / 3 |
| right call, test_hand | | | 0.98 ± 0.02 | 0.94 ± 0.02 | |

By part on test_hand9 (episodes right, v7 → v8, three seeds pooled):

| `r1_` list the folder | `r2_` reword | `r3_` follow the pointer | `r4_` search, don't guess | `r5_` the subfolder | `stop_` | `new_` | `base_` |
|---|---|---|---|---|---|---|---|
| 0.28 → 0.61 | 0.67 → 0.83 | 0.33 → 0.67 | 0.73 → 0.67 | 0.53 → 0.67 | 0.50 → 0.50 | 0.25 → 0.13 | 1.00 → 0.96 |

Per-seed tests and the failures are in
[`results/compare-v7-v8/`](../results/compare-v7-v8/).
- **Retrying is partly learned.** Retry episodes go 35/69 → 47/69 over the
  seeds, most on listing the folder after a missing file. No seed is
  significant alone on the whole set (3 / 2, 7 / 1, 6 / 5).
- **Stopping is not, and abstention pays.** The stop twins stay at 0.50.
  Abstention falls on all four hand-written episode sets (10 fixed, 27
  broken), mostly where an error or a listing in the history already
  answers: v8 calls once more.
- **A habit from the generator.** `retry.py`'s first searches are the bare
  topic; v8 drops `k` and the second half of "X and Y" from single searches
  (test_hand 0.98 → 0.94, test_hand5 0.86 → 0.81).
- **Still wrong in every model:** a re-check the user asks for after the
  history settled it, an empty index read as a miss, requests no tool can
  do (answered with `http_get` or `bash`, tools that do not exist).
- **v7 stays the default.**

## Answering documents: askdocs

Training a model to call tools can cost
it its general ability. So the base and the fine-tuned 1.5B answered
[askdocs](https://github.com/Simon-oid/askdocs)' 45 evaluation questions (53
from the v3 rerun on),
which need grounded, cited answers and no tool calls, with the same
retrieval. A 7B judged faithfulness. Reports are in
[`results/askdocs-forgetting/`](../results/askdocs-forgetting/).

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
([`results/askdocs-forgetting-v4/`](../results/askdocs-forgetting-v4/)).
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
[`results/askdocs-forgetting-v5/`](../results/askdocs-forgetting-v5/)): key-fact
recall 0.55, wrong refusals 0.16, correct refusals 1.00, faithfulness 0.89
(base 0.49, 0.21, 1.00, 0.79). The gate flags nothing. Training on episodes,
whose final replies quote tool results, did not cost the model its answering
from documents.

**v6 and the DPO rounds on askdocs.** Same base run, seed 0 each,
2026-11-23 to 11-25
([`results/askdocs-forgetting-v6/`](../results/askdocs-forgetting-v6/)):

| askdocs eval | base 1.5B | v5 | v6 | DPO 1 | DPO 2 | DPO 3 |
|---|---|---|---|---|---|---|
| key-fact recall | 0.49 | 0.55 | 0.66 | 0.56 | 0.53 | **0.70** |
| wrong refusals | 0.21 | 0.16 | **0.02** | 0.19 | 0.16 | 0.05 |
| faithfulness | 0.79 | **0.89** | 0.85 | 0.72 | 0.88 | 0.81 |

The gate flags nothing for any of them. v6, which learned to put the value it
read into its reply, almost never refuses an answerable question (1 of 43)
and recalls more key facts than the base (+0.17 [+0.05, +0.31]). DPO 1's
faithfulness is the lowest, within the gate's noise. DPO 3 recalls the most
key facts (+0.21 [+0.09, +0.34]), a side effect of calling less. One seed
each.

**v7 on askdocs.** Same base run, seed 0, 2026-11-26
([`results/askdocs-forgetting-v7/`](../results/askdocs-forgetting-v7/)):
key-fact recall 0.62 (v6 0.66), wrong refusals 0.07 (v6 0.02), correct
refusals 0.90 (one unanswerable question answered), faithfulness 0.75 (v6
0.85). The gate against the base flags nothing (key facts +0.13 [+0.02,
+0.25]); against v6 every metric slips, each within one seed's interval.

**v8 on askdocs.** Same base run, seed 0, 2026-11-28
([`results/askdocs-forgetting-v8/`](../results/askdocs-forgetting-v8/)):
key-fact recall 0.53 (v7 0.62), wrong refusals 0.02 (v7 0.07), correct
refusals 1.00 (v7 0.90), faithfulness 0.73 (v7 0.75). The gate flags
nothing against the base or against v7 (key facts −0.085 [−0.205,
+0.031]).

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

## How strict level 4 is

Exact matching counts some harmless calls as
wrong. The 7B answered "dump the file" with `offset 1, limit 1000`, and wrote
`User-agent: *` with a trailing newline. Both are wrong here, by rule: an
argument the request did not ask for, or content that is not what was
dictated.
