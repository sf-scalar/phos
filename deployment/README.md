# Scalar Phos Deployment Guide

This directory contains the deployment artifacts, container configurations, and local inference scripts for serving the **Scalar Phos** model family across edge devices, laptops, and developer workstations.

## Route 1: Local Edge Inference via Ollama (Recommended)

Ollama allows running quantized GGUF binaries (`Q4_K_M`) locally with minimal memory footprints (~2.2 GB RAM for Flash, ~4.8 GB RAM for Pro).

### Step 1: Install & Start Ollama

Ensure Ollama is installed on your system, then start the background service:

```bash
ollama serve
```

### Step 2: Build & Run Custom Modelfiles

Using the provided Modelfiles in this folder, register and run your models:

* **For Scalar Phos Flash (3.2B):**
```bash
ollama create scalar-phos-flash -f deployment/ollama/Modelfile.flash
ollama run scalar-phos-flash
```

* **For Scalar Phos Pro (8.0B):**
```bash
ollama create scalar-phos-pro -f deployment/ollama/Modelfile.pro
ollama run scalar-phos-pro
```

## Route 2: Local Web UI via Gradio (`app.py`)

You can launch a ChatGPT-style local web interface that connects directly to your local Ollama instance:

1. Ensure dependencies are installed (`pip install -r requirements.txt`).
2. Verify Ollama is running in the background.
3. Launch the web app:
```bash
python deployment/app.py
```

4. Open your browser at `http://127.0.0.1:7860`.

## Route 3: Programmatic Python Inference (`transformers` + `peft`)

If you want to load the base architecture and dynamically layer your Hugging Face LoRA adapters via Python:

```bash
python deployment/python/inference_peft.py \
    --base_model meta-llama/Llama-3.2-3B-Instruct \
    --adapter scalar-ai/scalar-phos-flash \
    --prompt "Explain machine learning in one sentence."
```

## License

All scripts, Modelfiles, and deployment code in this directory are licensed under the **Apache License 2.0**. Model weights remain governed by their respective Llama Community Licenses.
