#!/usr/bin/env python3
"""
Scalar Phos — Dataset Preparation & Formatting Utility
Formats raw instruction datasets into Llama 3.1 / 3.2 chat template structures.
Licensed under the Apache License 2.0
"""

import argparse
import json
import os
from datasets import Dataset, load_dataset


def parse_args():
    parser = argparse.ArgumentParser(description="Format raw instruction datasets for Scalar Phos training")
    parser.add_argument("--input_path", type=str, default="", help="Path to local raw JSON/JSONL dataset file (optional)")
    parser.add_argument("--dataset_id", type=str, default="teknium/OpenHermes-2.5", help="Hugging Face dataset identifier")
    parser.add_argument("--output_path", type=str, default="./processed_data.json", help="Path to save processed dataset")
    parser.add_argument("--max_samples", type=int, default=1000, help="Number of samples to process (for quick testing)")
    return parser.parse_args()


# Llama 3.1 / 3.2 Chat Template Formatting Prompt Engineering
LLAMA_CHAT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "You are Scalar Phos, an efficient, high-performance language model developed by Scalar AI.<|eot_id|>\n"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{instruction}<|eot_id|>\n"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "{response}<|eot_id|>"
)


def format_sample(example):
    """Maps raw dataset fields into the formatted text string required by SFTTrainer."""
    # Adjust keys ('instruction', 'input', 'output') based on your raw dataset schema
    instruction = example.get("instruction", example.get("prompt", ""))
    input_text = example.get("input", "")
    response = example.get("output", example.get("response", ""))

    if input_text:
        full_instruction = f"{instruction}\n\nContext:\n{input_text}"
    else:
        full_instruction = instruction

    formatted_text = LLAMA_CHAT_TEMPLATE.format(
        instruction=full_instruction,
        response=response
    )
    
    return {"text": formatted_text}


def main():
    args = parse_args()

    print(f"=== Scalar Phos Data Preparation Utility ===")
    
    # 1. Load dataset (either local or from Hugging Face Hub)
    if args.input_path and os.path.exists(args.input_path):
        print(f"Loading local dataset from: {args.input_path}")
        dataset = load_dataset("json", data_files=args.input_path, split="train")
    else:
        print(f"Loading Hugging Face dataset: {args.dataset_id} (Subset: {args.max_samples} samples)")
        dataset = load_dataset(args.dataset_id, split=f"train[:{args.max_samples}]")

    # 2. Apply formatting transformation
    print("Formatting samples into Llama 3 chat template...")
    processed_dataset = dataset.map(
        format_sample,
        remove_columns=dataset.column_names,
        desc="Formatting dataset"
    )

    # 3. Save processed dataset to disk
    output_dir = os.path.dirname(args.output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    processed_dataset.to_json(args.output_path)
    print(f"\n✅ Successfully processed {len(processed_dataset)} samples!")
    print(f"Saved formatted dataset to: {args.output_path}")
    print("\nSample formatted output preview:")
    print("-" * 60)
    print(processed_dataset[0]["text"][:500] + "...\n[TRUNCATED]")
    print("-" * 60)


if __name__ == "__main__":
    main()
