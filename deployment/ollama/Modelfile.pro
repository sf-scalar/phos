# ==============================================================================
# Scalar Phos Pro (8.0B) — Ollama Modelfile
# Licensed under the Apache License 2.0 (Code) / Llama 3.1 Community License (Weights)
# ==============================================================================

FROM hf.co/scalar-ai/scalar-phos-pro:Q4_K_M

# Inference Parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"

# System Persona
SYSTEM "You are Scalar Phos Pro, an advanced reasoning and instruction-following language model developed by Scalar AI."
