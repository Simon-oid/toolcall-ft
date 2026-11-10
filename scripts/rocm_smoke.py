#!/usr/bin/env python3
"""ROCm smoke test: can this GPU fine-tune with LoRA, how fast, how much memory?

A few dozen LoRA steps of a small instruct model on a fixed batch of tool
calls; checks the loss falls (the step really trains) and reports
tokens/s and peak memory. Run before planning training on this machine.

    python scripts/rocm_smoke.py [--model Qwen/Qwen2.5-1.5B-Instruct] [--steps 40]
"""

from __future__ import annotations

import argparse
import time

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--seq", type=int, default=512)
    ap.add_argument("--checkpointing", action="store_true")
    args = ap.parse_args()
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16).cuda()
    if args.checkpointing:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0,
                                             target_modules="all-linear", task_type="CAUSAL_LM"))
    model.print_trainable_parameters()
    text = ('<tool_call>{"name": "fs_read", "arguments": {"path": "notes/plan.md", "limit": 20}}'
            '</tool_call> ') * 64
    ids = tok(text, return_tensors="pt").input_ids[:, :args.seq].repeat(args.batch, 1).cuda()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4)
    torch.cuda.reset_peak_memory_stats()
    losses, t0 = [], None
    for step in range(args.steps):
        if step == 3:                       # skip warm-up (kernel compilation, allocator)
            torch.cuda.synchronize()
            t0 = time.perf_counter()
        loss = model(input_ids=ids, labels=ids).loss
        loss.backward()
        opt.step()
        opt.zero_grad(set_to_none=True)
        losses.append(loss.item())
    torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    tokens = (args.steps - 3) * args.batch * ids.shape[1]
    peak = torch.cuda.max_memory_allocated() / 2**30
    print(f"{args.model}: loss {losses[0]:.3f} -> {losses[-1]:.3f}; "
          f"{tokens / dt:.0f} tokens/s; {dt / (args.steps - 3) * 1000:.0f} ms/step "
          f"(batch {args.batch} x {ids.shape[1]}); peak {peak:.2f} GiB")
    ok = losses[-1] < losses[0] * 0.5
    print("PASS" if ok else "FAIL: the loss did not fall")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
