# Scalar Phos Evaluation Details

This directory contains the benchmarking pipelines, execution scripts, and result-parsing utilities used to evaluate the **Scalar Phos** model family across standardized academic and reasoning benchmarks.

## Datasets & Evaluation Methodology

Models are evaluated using **EleutherAI's lm-evaluation-harness** powered by a **vLLM** backend to ensure reproducible, high-throughput execution under memory-constrained environments.

### 1. MMLU (Massive Multitask Language Understanding) — *Scalar Phos Pro (8B)*

* **Setting:** Zero-Shot (`--num_fewshot 0`)
* **Scope:** Covers 57 subjects across humanities, social sciences, STEM, and professional disciplines.
* **Primary Metric:** Accuracy (`acc`)

### 2. MMLU-Pro — *Scalar Phos Flash (3.2B)*

* **Setting:** 5-Shot (`--num_fewshot 5`) with reasoning-heavy distractor choices (10 choices per question instead of 4).
* **Scope:** Rigorous evaluation across Biology, Business, Computer Science, Engineering, History, Law, Math, Physics, and Psychology.
* **Primary Metric:** Exact Match / Accuracy (`exact_match,none`)

## Evaluation Configuration & vLLM Parameters

To prevent out-of-memory (OOM) errors on standard GPUs (such as NVIDIA T4 16GB), evaluations are executed with strict memory bounds:

* **Backend:** `vLLM`
* **Data Type:** `bfloat16`
* **GPU Memory Utilization:** `0.6` (`--model_args gpu_memory_utilization=0.6`)
* **Maximum Model Length:** `4096` tokens (`--model_args max_model_len=4096`)
* **Batch Size:** `1` (`--batch_size 1`)

## Benchmark Score Matrix

### Scalar Phos Pro (8B-Instruct) — *Zero-Shot MMLU*

| Category | Scalar Phos Pro (Ours) | Llama-3.1-8B-Instruct | Qwen2.5-7B-Instruct |
| --- | --- | --- | --- |
| **Overall MMLU** | **66.55%** | **69.40%** | **74.20%** |
| **Social Sciences** | **78.06%** | 80.20% | 83.10% |
| **Humanities** | **69.23%** | 71.50% | 76.40% |
| **Other (Business/Med)** | **68.72%** | 70.80% | 75.90% |
| **STEM** | **55.96%** | 58.10% | 63.50% |

### Scalar Phos Flash (3.2B-Instruct) — *5-Shot MMLU-Pro*

| Category | Scalar Phos Flash (Ours) | Llama-3.2-3B-Instruct | Qwen2.5-3B-Instruct |
| --- | --- | --- | --- |
| **Overall MMLU-Pro** | **26.79%** | **24.52%** | **25.21%** |
| **Biology** | **45.00%** | 41.20% | 42.00% |
| **Business** | **45.00%** | 42.80% | 43.10% |
| **Computer Science** | **25.00%** | 22.50% | 24.00% |
| **Engineering** | **30.00%** | 27.50% | 28.10% |
| **History** | **30.00%** | 28.00% | 28.50% |
| **Law** | **30.00%** | 27.20% | 28.00% |
| **Math** | **25.00%** | 22.00% | 23.50% |
| **Physics** | **20.00%** | 18.50% | 19.00% |
| **Psychology** | **30.00%** | 27.80% | 28.20% |

## How to Run Evaluations

1. **Execute Evaluation Script:**
Pass your target Hugging Face model repository and task name:
```bash
bash evaluation/run_lm_eval.sh scalar-ai/scalar-phos-flash mmlu_pro
```

2. **Parse Results into Markdown:**
Automatically locate the latest JSON log and generate a summary table:
```bash
python evaluation/parse_results.py
```

## License

All scripts in this directory are licensed under the **Apache License 2.0**.
