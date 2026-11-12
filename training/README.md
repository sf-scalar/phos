# Scalar Phos Training Pipeline

This directory contains the parameter-efficient fine-tuning (PEFT) pipelines, configuration files, and dataset preprocessing routines used to build the **Scalar Phos** model family.

## Training Datasets

Both models in the Scalar Phos family are instruction-tuned using a high-quality curated mix of open-source instruction corpora:

* **Primary Corpus:** Filtered subsets of [`teknium/OpenHermes-2.5`](https://huggingface.co/datasets/teknium/OpenHermes-2.5), optimized for multi-turn reasoning, coding, logical deduction, and structured formatting.
* **Formatting & Chat Template:** All data points are formatted using the native base model chat template (`<|begin_of_text|><|start_header_id|>system<|end_header_id|>...`) to preserve upstream instruction-following alignment.

## Hyperparameter Configurations

Fine-tuning utilizes **4-bit QLoRA** (Quantized Low-Rank Adaptation) via Unsloth to minimize VRAM overhead while preserving high task performance.

### Key Architectural Hyperparameters:

* **Quantization:** 4-bit NF4 (`load_in_4bit: true`)
* **LoRA Rank ($r$):** `16`
* **LoRA Alpha ($\alpha$):** `16`
* **LoRA Dropout:** `0.0`
* **Target Modules:** `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`
* **Optimizer:** `adamw_8bit`
* **Max Sequence Length:** `4096` tokens

## Hardware Requirements

* **For Scalar Phos Flash (3B):** Minimum **6 GB VRAM** (tested on NVIDIA T4 16GB at `batch_size=2`, `gradient_accumulation_steps=4`).
* **For Scalar Phos Pro (8B):** Minimum **12 GB VRAM** (tested on NVIDIA T4 16GB at `batch_size=1`, `gradient_accumulation_steps=8`).
* *Note: Training loops require an NVIDIA CUDA-compatible GPU and cannot execute on CPU or Apple Silicon unified memory.*

## How to Run Fine-Tuning

1. Ensure your environment is fully provisioned by running the root setup script:
```bash
python setup.py

```

2. Populate your `.env` file with your Hugging Face write token and optional Weights & Biases API key:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Execute the QLoRA training script pointing to your desired model configuration:
**To train Scalar Phos Flash (3.2B):**
```bash
python training/train_qlora.py --config training/configs/phos_flash_3b.json
```

**To train Scalar Phos Pro (8.0B):**
```bash
python training/train_qlora.py --config training/configs/phos_pro_8b.json
```

## License

All scripts and training configurations in this directory are licensed under the **Apache License 2.0**.
