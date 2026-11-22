"""DPO from a fine-tuned model, on the preference pairs of prefs.py.

    python -m toolcall.export --model Qwen/Qwen2.5-1.5B-Instruct --adapter models/ft-1.5b-v5
    python -m toolcall.dpo --start models/ft-1.5b-v5-merged --out models/dpo-1.5b-v5

The model it starts from is the merged SFT model (export.py writes it). A
new LoRA is trained on top, and the reference policy is that same model
with the adapter switched off, so the KL term keeps DPO close to the SFT
model, not to the base. Prompts are rendered as at evaluation, as in
train.py. The served model is exported the same way, with --model the
merged start: `export --model models/ft-1.5b-v5-merged --adapter <out>`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .data import ROOT
from .prompt import load_tools, render_case, tokenizer

TEMPLATE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"     # its chat template renders the prompts


def examples(path: Path, tools: list[dict]) -> list[dict]:
    rows = [json.loads(x) for x in path.read_text().splitlines()]
    return [{"prompt": render_case(r, TEMPLATE_MODEL, tools), "chosen": r["chosen"],
             "rejected": r["rejected"]} for r in rows]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--start", required=True, help="merged SFT model (export.py)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefs", default=str(ROOT / "data" / "prefs_v5.jsonl"))
    ap.add_argument("--beta", type=float, default=0.1)
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--accum", type=int, default=16)
    ap.add_argument("--max-length", type=int, default=1536)
    ap.add_argument("--seed", type=int, default=20261110)
    ap.add_argument("--max-steps", type=int, default=-1, help="smoke runs")
    args = ap.parse_args()

    train = examples(Path(args.prefs), load_tools())
    tok = tokenizer(TEMPLATE_MODEL)
    longest = max(len(tok(r["prompt"] + max(r["chosen"], r["rejected"], key=len)).input_ids)
                  for r in train) + 1
    if longest > args.max_length:
        raise SystemExit(f"a pair has {longest} tokens > --max-length {args.max_length}")
    print(f"{len(train)} pairs; longest {longest} tokens")

    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from trl import DPOConfig, DPOTrainer

    config = DPOConfig(
        output_dir=args.out, num_train_epochs=args.epochs, max_steps=args.max_steps,
        learning_rate=args.lr, lr_scheduler_type="cosine", warmup_steps=0.1,
        per_device_train_batch_size=args.batch, gradient_accumulation_steps=args.accum,
        gradient_checkpointing=True, bf16=True, beta=args.beta, max_length=args.max_length,
        save_strategy="no", logging_steps=1, report_to="none", seed=args.seed,
        data_seed=args.seed, model_init_kwargs={"dtype": torch.bfloat16})
    lora = LoraConfig(r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05,
                      target_modules="all-linear", task_type="CAUSAL_LM")
    trainer = DPOTrainer(model=args.start, args=config, train_dataset=Dataset.from_list(train),
                         processing_class=tok, peft_config=lora)
    # Both answers must end with the end-of-turn token, or DPO teaches the
    # model to stop (or not) for the wrong reason.
    sample: dict = trainer.train_dataset[0]  # type: ignore[index]
    print("tokenized fields:", sorted(sample))
    for side in ("chosen", "rejected"):
        ids = sample.get(f"{side}_input_ids") or sample.get(f"{side}_ids")
        if ids is None:
            raise SystemExit(f"no tokenized {side} field in {sorted(sample)}")
        text = tok.decode(ids)
        if not text.rstrip().endswith("<|im_end|>"):
            raise SystemExit(f"{side} does not end with <|im_end|>: {text[-80:]!r}")
    trainer.train()
    trainer.save_model(args.out)
    Path(args.out, "dpo_args.json").write_text(json.dumps(vars(args), indent=1))
    Path(args.out, "log_history.json").write_text(json.dumps(trainer.state.log_history,
                                                             indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
