"""A trained LoRA adapter -> one GGUF file llama.cpp can serve.

    python -m toolcall.export --model Qwen/Qwen2.5-1.5B-Instruct --adapter models/ft-1.5b

1. merge the adapter into the base weights (bf16): the served model is one
   plain set of weights, no adapter to load at runtime;
2. save it in Hugging Face format next to the adapter (<adapter>-merged/);
3. convert with llama.cpp's own convert_hf_to_gguf.py to Q8_0, the same
   quantization as the base model it is compared with, so a difference in
   the evaluation is the training, not the quantization.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

LLAMA_CPP = Path(os.environ.get("LLAMA_CPP", Path.home() / "src" / "llama.cpp"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--outtype", default="q8_0")
    args = ap.parse_args()

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    adapter = Path(args.adapter)
    merged = adapter.parent / f"{adapter.name}-merged"
    base = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16)
    model = PeftModel.from_pretrained(base, adapter).merge_and_unload()
    model.save_pretrained(merged, safe_serialization=True)
    AutoTokenizer.from_pretrained(args.model).save_pretrained(merged)

    gguf = adapter.parent / f"{adapter.name}-{args.outtype}.gguf"
    subprocess.run([sys.executable, str(LLAMA_CPP / "convert_hf_to_gguf.py"), str(merged),
                    "--outfile", str(gguf), "--outtype", args.outtype], check=True)
    print(f"-> {gguf} ({gguf.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
