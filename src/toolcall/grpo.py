"""GRPO from a fine-tuned model, rewarded by the evaluation's own scorer.

    python -m toolcall.grpo --start models/ft-1.5b-v7-merged --out models/grpo-1.5b-v7

As in dpo.py, the model it starts from is the merged SFT model and a new
LoRA is trained on top; with --beta > 0 the reference is that same model
with the adapter off. Each prompt is a turn of the SFT training data
(train, mt_train_g, mt7_train: what v7 saw), rendered as at evaluation,
and its --generations sampled replies are scored by score_cases, the
scorer and C judge that evaluate.py uses, so the reward is the metric:

  a call turn      1 if the call is right (level 4), PARTIAL if it parses
                   and passes the tool's schema but is not right, else 0
  a no-call turn   1 if the model abstained and, where the turn asks for
                   it, the reply carries the fact the tool returned, else 0

GRPO learns only from groups whose replies disagree; TRL logs the share
of groups that all score the same (frac_reward_zero_std). On v7's own
training turns that share is 47 of 48 (a 6-step smoke): sampled at T=1, v7
is right on almost all of them. --hard-from keeps only the turns where a
sample of the start model was wrong (sample.py --all), so every group has
a chance to disagree.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from .data import load
from .evaluate import score_cases, step_right
from .prefs import GARBAGE
from .prompt import load_tools, render_case, tokenizer
from .sample import right

TEMPLATE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"     # its chat template renders the prompts
SPLITS = ("train", "mt_train_g", "mt7_train")
PARTIAL = 0.5          # a well-formed call that is not the right one


def case_rewards(cases: list[dict], replies: list[str]) -> list[float]:
    """One reward per reply, scored against its case."""
    out = []
    for row in score_cases(cases, replies):
        if step_right(row):
            out.append(1.0)
        elif row["expected"] is not None and row["score"]["levels"]["schema"]:
            out.append(PARTIAL)
        else:
            out.append(0.0)
    return out


def reward(prompts: list[str], completions: list[str], case: list[str],
           **_: object) -> list[float | None]:
    """TRL's reward-function signature: dataset columns arrive as keyword lists."""
    return list(case_rewards([json.loads(c) for c in case], completions))


def hard_ids(sampled: Path) -> set[str]:
    """Turns where the sample (sample.py --all) is wrong and not server garbage."""
    rows = [json.loads(x) for x in sampled.read_text().splitlines()]
    return {r["id"] for r in rows if not right(r) and not GARBAGE.match(r["reply"])}


def select_cases(splits: list[str], limit: int | None = None, seed: int = 20261110,
                 hard_from: Path | None = None) -> list[dict]:
    """The training turns, shuffled, cut to --limit, then to the hard ones."""
    cases = [c for s in splits for c in load(s)]
    random.Random(seed).shuffle(cases)
    cases = cases[:limit] if limit else cases
    if hard_from is not None:
        hard = hard_ids(hard_from)
        cases = [c for c in cases if c["id"] in hard]
    return cases


def prompts_and_cases(splits: list[str], limit: int | None = None, seed: int = 20261110,
                      hard_from: Path | None = None) -> list[dict]:
    tools = load_tools()
    cases = select_cases(splits, limit, seed, hard_from)
    return [{"prompt": render_case(c, TEMPLATE_MODEL, tools),
             "case": json.dumps(c, ensure_ascii=False)} for c in cases]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--start", required=True, help="merged SFT model (export.py)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--splits", default=",".join(SPLITS))
    ap.add_argument("--generations", type=int, default=8, help="replies per prompt")
    ap.add_argument("--batch", type=int, default=16, help="completions per micro-batch")
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--max-completion", type=int, default=256)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--beta", type=float, default=0.04, help="KL to the start model")
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--limit", type=int, default=None, help="first N shuffled prompts")
    ap.add_argument("--hard-from", type=Path, default=None,
                    help="results.jsonl of sample.py --all: train only where it was wrong")
    ap.add_argument("--max-steps", type=int, default=-1, help="smoke runs")
    args = ap.parse_args()
    if (args.batch * args.accum) % args.generations:
        raise SystemExit("--batch x --accum must be a multiple of --generations")

    train = prompts_and_cases(args.splits.split(","), args.limit, args.seed, args.hard_from)
    if not train:
        raise SystemExit("no prompts to train on")
    per_step = args.batch * args.accum // args.generations
    print(f"{len(train)} prompts; {per_step} prompts x {args.generations} replies per step; "
          f"{len(train) * args.epochs / per_step:.0f} steps", flush=True)

    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from trl import GRPOConfig, GRPOTrainer

    config = GRPOConfig(
        output_dir=args.out, num_train_epochs=args.epochs, max_steps=args.max_steps,
        learning_rate=args.lr, lr_scheduler_type="cosine", warmup_steps=0.05,
        per_device_train_batch_size=args.batch, gradient_accumulation_steps=args.accum,
        # Generate one micro-batch at a time: TRL's default generates the
        # whole step's replies at once (64 x ~1.1k tokens), which runs a 16 GB
        # card out of memory.
        steps_per_generation=1,
        num_generations=args.generations, max_completion_length=args.max_completion,
        temperature=args.temperature, beta=args.beta, gradient_checkpointing=True,
        bf16=True, save_strategy="no", logging_steps=1, report_to="none", seed=args.seed,
        data_seed=args.seed, model_init_kwargs={"dtype": torch.bfloat16})
    lora = LoraConfig(r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05,
                      target_modules="all-linear", task_type="CAUSAL_LM")
    trainer = GRPOTrainer(model=args.start, reward_funcs=reward, args=config,
                          train_dataset=Dataset.from_list(train),
                          processing_class=tokenizer(TEMPLATE_MODEL), peft_config=lora)
    trainer.train()
    trainer.save_model(args.out)
    Path(args.out, "grpo_args.json").write_text(json.dumps(vars(args), indent=1, default=str))
    Path(args.out, "log_history.json").write_text(json.dumps(trainer.state.log_history,
                                                             indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
