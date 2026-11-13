<div align="center">

[![scalar](https://github.com/user-attachments/assets/39ffab3f-b3c5-4b5d-b1a6-1f13f41460f5)]()

**Open-Source Research, Training Pipelines, and Evaluation Suite for Parameter-Efficient Language Models**

[![Toolkit](https://img.shields.io/badge/Toolkit-Unsloth_|_PEFT-000000?style=flat-square&logo=python&logoColor=white)]()
[![Framework](https://img.shields.io/badge/Framework-PyTorch_|_vLLM-000000?style=flat-square&logo=pytorch&logoColor=white)]()
[![Deployment](https://img.shields.io/badge/Formats-LoRA_|_GGUF-000000?style=flat-square&logo=huggingface&logoColor=white)]()
[![Organization](https://img.shields.io/badge/Hugging_Face-scalar--ai-000000?style=flat-square&logo=huggingface&logoColor=white)]()

</div>

## Overview

**Scalar Phos** is a family of instruction-tuned, open-weights language models developed by **Scalar AI**. This repository serves as the central hub containing all training configurations, dataset formatting utilities, evaluation harnesses, deployment recipes, and CLI execution tooling used across the **Scalar Phos** ecosystem.

Our goal is to produce parameter-efficient models that preserve high-level general reasoning while remaining lightweight enough to deploy on consumer hardware, free-tier accelerators, and edge devices.

## Model Matrix

| Model Name | Base Model | Params | Key Feature / Benchmark | Hugging Face Repo | Status |
| --- | --- | --- | --- | --- | --- |
| **Scalar Phos Pro** | Llama-3.1-8B-Instruct | 8.0B | **66.55% MMLU** — Domain reasoning & instruction following | [`scalar-ai/scalar-phos-pro`](https://huggingface.co/scalar-ai/scalar-phos-pro) | Released |
| **Scalar Phos Flash** | Llama-3.2-3B-Instruct | 3.2B | **26.79% MMLU-Pro** — Low-latency, high-throughput edge model | [`scalar-ai/scalar-phos-flash`](https://huggingface.co/scalar-ai/scalar-phos-flash) | Released |
| **Scalar Phos Bit** | Llama-3.2-1B-Instruct | 1.2B | Ultra-lightweight edge reasoning for embedded devices | — | Pipeline |

## Benchmark Highlights

Models across the Scalar Phos family are evaluated using EleutherAI's `lm-evaluation-harness` with standard zero-shot (MMLU) and 5-shot (MMLU-Pro) setups (full breakdown in [`evaluation/README.md`](./evaluation/README.md)):

* **Scalar Phos Pro (8B):** Achieves **66.55%** on zero-shot MMLU, demonstrating strong capability retention across Social Sciences (78.06%), Humanities (69.23%), and STEM (55.96%).
* **Scalar Phos Flash (3B):** Achieves **26.79%** on 5-shot MMLU-Pro via vLLM, outperforming baseline 3B-class architectures in Biology (45.0%), Business (45.0%), Law (30.0%), and Engineering (30.0%).

## Environment Setup & Model Acquisition

Run the built-in CLI tools to verify your system's hardware compatibility (RAM, disk overhead, Python runtime, and CUDA VRAM) and pull model weights from Hugging Face:

```bash
# 1. Inspect hardware compatibility & install dependencies
python setup.py

# 2. Configure environment variables
cp .env.example .env

# 3. Interactively download Scalar Phos weights or GGUF binaries
python download.py
```

## Quickstart

### 1. Local Edge Execution (Ollama)

Run quantized `Q4_K_M` GGUF binaries directly on consumer hardware (macOS / Windows / Linux):

```bash
# Run Scalar Phos Flash (3.2B)
ollama run hf.co/scalar-ai/scalar-phos-flash:Q4_K_M

# Run Scalar Phos Pro (8.0B)
ollama run hf.co/scalar-ai/scalar-phos-pro:Q4_K_M
```

### 2. Local Web UI (Gradio)

Launch a local chat interface backed by your active Ollama instance (see [`deployment/README.md`](./deployment/README.md)):

```bash
python deployment/app.py
```

### 3. Python (`transformers` + `peft`)

Load LoRA adapters dynamically over the base architecture using `peft`:

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model_id = "meta-llama/Llama-3.2-3B-Instruct"
adapter_id = "scalar-ai/scalar-phos-flash"

tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, adapter_id)

prompt = "Explain quantum computing in two simple sentences."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training & Evaluation

### Training Pipeline

Fine-tuning for the Phos series relies on **4-bit QLoRA** powered by [Unsloth](https://github.com/unslothai/unsloth) for low VRAM consumption and high memory efficiency (full guide in [`training/README.md`](./training/README.md)):

```bash
# Optional: Format raw instruction datasets into the Llama 3 chat template
python training/data_prep.py --max_samples 1000

# Train Scalar Phos Flash (3.2B)
python training/train_qlora.py --config training/configs/phos_flash_3b.json

# Train Scalar Phos Pro (8.0B)
python training/train_qlora.py --config training/configs/phos_pro_8b.json
```

### Evaluation Harness

Evaluations are executed via `lm-eval` with T4-optimized memory controls (`gpu_memory_utilization=0.6`, `max_model_len=4096`):

```bash
# Run benchmark evaluation
bash evaluation/run_lm_eval.sh scalar-ai/scalar-phos-flash mmlu_pro

# Parse latest JSON output log into a Markdown table
python evaluation/parse_results.py
```

## Compliance, Licensing & Contributing

This repository uses a dual-licensing structure to separate the codebase from the underlying model weights:

* **Code, Scripts & Documentation:** All source code, training configurations, evaluation scripts, and documentation in this GitHub repository are licensed under the **[Apache License 2.0](./LICENSE)**.
* **Model Weights & Adapters:** The fine-tuned model weights, LoRA adapters, and GGUF binaries hosted on Hugging Face are governed by their respective upstream base model licenses—specifically the **[Meta Llama 3.1 Community License](https://www.llama.com/llama3_1/license/)** (for Scalar Phos Pro) and **[Meta Llama 3.2 Community License](https://www.llama.com/llama3_2/license/)** (for Scalar Phos Flash & Bit).

Please review [USE_POLICY.md](./USE_POLICY.md) for acceptable use guidelines, [NOTICE](./NOTICE) for upstream attribution requirements, and [CONTRIBUTING.md](./CONTRIBUTING.md) if you would like to contribute to the project.
