#!/usr/bin/env python3
"""
Scalar Phos — Local PEFT Inference Script
Dynamically loads base model architecture + Hugging Face LoRA adapters.
Licensed under the Apache License 2.0
"""

import argparse
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from huggingface_hub import file_exists


def parse_args():
    parser = argparse.ArgumentParser(description="Run inference with Scalar Phos PEFT adapters")
    parser.add_argument("--base_model", type=str, default="meta-llama/Llama-3.2-3B-Instruct", help="Base Hugging Face model ID")
    parser.add_argument("--adapter", type=str, default="scalar-ai/scalar-phos-flash", help="Hugging Face LoRA adapter ID")
    parser.add_argument("--prompt", type=str, default="Explain quantum computing in two concise sentences.", help="Input prompt")
    return parser.parse_args()


def main():
    args = parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"=== Initializing Scalar Phos Inference ===")
    print(f"Base Model : {args.base_model}")
    print(f"Adapter    : {args.adapter}")
    print(f"Device     : {device.upper()}\n")

    # 1. Load Tokenizer & Base Model
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
        device_map="auto",
        use_safetensors=True,
    )

    # 2. Attach PEFT Adapters
    adapter_weights = os.path.join(args.adapter, "adapter_model.safetensors")
    if not (
        os.path.isfile(adapter_weights)
        if os.path.isdir(args.adapter)
        else file_exists(args.adapter, "adapter_model.safetensors")
    ):
        raise ValueError(f"Adapter {args.adapter} must provide adapter_model.safetensors")

    model = PeftModel.from_pretrained(base_model, args.adapter)
    model.eval()

    # 3. Format Prompt & Generate
    inputs = tokenizer(args.prompt, return_tensors="pt").to(device)

    print(f"Prompt: \"{args.prompt}\"\n")
    print("Generating response...")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\n--- Model Output ---")
    print(response)
    print("--------------------")


if __name__ == "__main__":
    main()
