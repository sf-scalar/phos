#!/usr/bin/env bash
# ==============================================================================
# Scalar Phos — Standardized Evaluation Script
# Wraps EleutherAI lm-evaluation-harness with vLLM & T4-safe memory flags
# Licensed under the Apache License 2.0
# ==============================================================================

set -euo pipefail

MODEL_ID="${1:-scalar-ai/scalar-phos-flash}"
TASK="${2:-mmlu_pro}"
BATCH_SIZE="${3:-1}"
MAX_MODEL_LEN="${4:-4096}"
GPU_MEM_UTIL="${5:-0.6}"
OUTPUT_DIR="./eval_results"

mkdir -p "$OUTPUT_DIR"

echo "=============================================================================="
echo "  Scalar Phos Evaluation Runner"
echo "  Model: $MODEL_ID"
echo "  Task:  $TASK"
echo "=============================================================================="

lm_eval \
    --model vllm \
    --model_args pretrained="$MODEL_ID",dtype=bfloat16,gpu_memory_utilization="$GPU_MEM_UTIL",max_model_len="$MAX_MODEL_LEN" \
    --tasks "$TASK" \
    --batch_size "$BATCH_SIZE" \
    --output_path "$OUTPUT_DIR" \
    --log_samples

echo ""
echo "Evaluation complete. Raw logs saved to $OUTPUT_DIR/"
