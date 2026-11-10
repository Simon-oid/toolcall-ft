"""Supervised fine-tuning with LoRA: the base model learns to answer each
training request the way its case says (a tool call, a clarifying
question, a refusal, or its own chit-chat reply).

    python -m toolcall.train --model Qwen/Qwen2.5-1.5B-Instruct --out models/ft-1.5b
    python -m toolcall.train ... --dry-run      # build and check the data, no training

The prompt is rendered exactly as at evaluation (prompt.render: our system
text, the six tools, the request), and the loss is computed on the
completion only: the model is not trained to reproduce the 1,000 tokens of
tool schemas it is given. Every example must fit in --max-length; one that
does not is an error, not a silent truncation of the part the loss is on.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .data import load
from .distill import OUT as DISTILLED
from .prompt import load_tools, render, tokenizer


def completion(row: dict, distilled: dict[str, str]) -> str | None:
    """What the model should write for a case (TRL appends the end token)."""
    if row["expected"] is not None:
        return "<tool_call>\n" + json.dumps(row["call"], ensure_ascii=False) + "\n</tool_call>"
    if row["intent"] == "no_tool":
        return distilled.get(row["request"])
    return row["reply"]


def examples(split: str, model: str, tools: list[dict], distilled: dict[str, str]) -> list[dict]:
    out = []
    for row in load(split):
        c = completion(row, distilled)
        if c is None:
            raise SystemExit(f"no target for {row['id']} ({row['intent']}): run toolcall.distill")
        out.append({"prompt": render(row["request"], model, tools), "completion": c})
    return out


def check_lengths(rows: list[dict], model: str, max_length: int) -> int:
    tok = tokenizer(model)
    longest = max(len(tok(r["prompt"] + r["completion"]).input_ids) + 1 for r in rows)
    if longest > max_length:
        raise SystemExit(f"an example has {longest} tokens > --max-length {max_length}: "
                         "it would be truncated where the loss is")
    return longest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--accum", type=int, default=8, help="effective batch = batch x accum")
    ap.add_argument("--max-length", type=int, default=1536)
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tools = load_tools()
    distilled = {json.loads(x)["request"]: json.loads(x)["reply"]
                 for x in DISTILLED.read_text().splitlines()}
    train = examples("train", args.model, tools, distilled)
    val = examples("val", args.model, tools, distilled)
    longest = check_lengths(train + val, args.model, args.max_length)
    print(f"{len(train)} train, {len(val)} val examples; longest {longest} tokens")
    if args.dry_run:
        print(train[0]["prompt"][-200:] + train[0]["completion"])
        return 0

    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from trl import SFTConfig, SFTTrainer

    config = SFTConfig(
        output_dir=args.out, num_train_epochs=args.epochs, learning_rate=args.lr,
        lr_scheduler_type="cosine", warmup_ratio=0.03, weight_decay=0.0,
        per_device_train_batch_size=args.batch, per_device_eval_batch_size=args.batch,
        gradient_accumulation_steps=args.accum, gradient_checkpointing=True,
        bf16=True, max_length=args.max_length, completion_only_loss=True, packing=False,
        eval_strategy="epoch", save_strategy="epoch", save_total_limit=2,
        logging_steps=10, report_to="none", seed=args.seed, data_seed=args.seed,
        model_init_kwargs={"dtype": torch.bfloat16})
    lora = LoraConfig(r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05,
                      target_modules="all-linear", task_type="CAUSAL_LM")
    trainer = SFTTrainer(model=args.model, args=config, peft_config=lora,
                         train_dataset=Dataset.from_list(train),
                         eval_dataset=Dataset.from_list(val),
                         processing_class=tokenizer(args.model))
    sample = trainer.train_dataset[0]
    ids, mask = sample["input_ids"], sample["completion_mask"]
    target = tokenizer(args.model).decode([t for t, m in zip(ids, mask, strict=True) if m])
    print(f"loss is on: {target!r}")
    if target.count("<|im_end|>") != 1 or not target.endswith("<|im_end|>"):
        raise SystemExit("the completion must end with exactly one <|im_end|>")
    trainer.train()
    trainer.save_model(args.out)
    Path(args.out, "train_args.json").write_text(json.dumps(vars(args), indent=1))
    log = [e for e in trainer.state.log_history if "eval_loss" in e or "loss" in e]
    Path(args.out, "log_history.json").write_text(json.dumps(log, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
