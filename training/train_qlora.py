#!/usr/bin/env python3
"""
Scalar Phos — QLoRA Fine-Tuning Pipeline
Powered by Unsloth & Hugging Face TRL / PEFT
Licensed under the Apache License 2.0
"""

import argparse
import json
import os
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import FastLanguageModel


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune Scalar Phos models via 4-bit QLoRA")
    parser.add_argument("--config", type=str, required=True, help="Path to training config JSON file")
    return parser.parse_args()


def main():
    args = parse_args()

    # Load configuration
    with open(args.config, "r") as f:
        config = json.load(f)

    model_name = config["model_name"]
    max_seq_length = config.get("max_seq_length", 4096)
    load_in_4bit = config.get("load_in_4bit", True)
    dataset_id = config["dataset_id"]
    output_dir = config["output_dir"]

    print(f"=== Initializing Scalar Phos Training: {model_name} ===")

    # 1. Load Model & Tokenizer via Unsloth
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        load_in_4bit=load_in_4bit,
    )

    # 2. Setup PEFT / QLoRA Adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r=config.get("lora_rank", 16),
        target_modules=config.get("target_modules", ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]),
        lora_alpha=config.get("lora_alpha", 16),
        lora_dropout=config.get("lora_dropout", 0.0),
        bias=config.get("bias", "none"),
        use_gradient_checkpointing=config.get("use_gradient_checkpointing", "unsloth"),
        random_state=config.get("random_state", 3407),
    )

    # 3. Load Dataset
    dataset = load_dataset(dataset_id, split="train")

    # 4. Configure Trainer
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field=config.get("dataset_text_field", "text"),
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=config.get("per_device_train_batch_size", 2),
            gradient_accumulation_steps=config.get("gradient_accumulation_steps", 4),
            warmup_steps=config.get("warmup_steps", 5),
            max_steps=config.get("max_steps", 60),
            learning_rate=config.get("learning_rate", 2e-4),
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=1,
            output_dir=output_dir,
            optim=config.get("optim", "adamw_8bit"),
            seed=3407,
        ),
    )

    # 5. Execute Training
    print("Starting QLoRA training run...")
    trainer_stats = trainer.train()
    print("Training complete!")

    # 6. Save LoRA Adapters
    adapter_path = os.path.join(output_dir, "lora_adapters")
    model.save_pretrained(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    print(f"Adapters saved successfully to {adapter_path}")


if __name__ == "__main__":
    main()
