# Contributing to Scalar Phos

Thank you for your interest in contributing to **Scalar Phos**! Whether you are fixing a bug in the CLI utilities, adding new evaluation benchmarks, optimizing QLoRA training configurations, or improving documentation, your contributions help make efficient open-weights models more accessible.

## Ways to Contribute

* **Bug Reports & Hardware Diagnostics:** Report issues encountered on specific GPUs, OS platforms, or Python runtimes.
* **Training & Fine-Tuning Recipes:** Submit new hyperparameter configs (`training/configs/`) or dataset formatting templates (`training/data_prep.py`).
* **Evaluation Benchmarks:** Expand `evaluation/run_lm_eval.sh` or improve log-parsing reports in `evaluation/parse_results.py`.
* **Deployment & Edge Runtimes:** Add container definitions, quantized Modelfiles, or lightweight inference examples in `deployment/`.
* **Documentation:** Clarify setup instructions, fix typos, or expand guides across folder `README.md` files.

## Development Setup

Before making changes, ensure your local environment is configured cleanly:

1. **Fork & Clone the Repository:**
   ```bash
   git clone https://github.com/sf-scalar/scalar-phos.git
   cd scalar-phos
   ```

2. **Create an Isolated Virtual Environment (Python 3.11–3.13 recommended):**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Run Diagnostics & Provision Dependencies:**
```bash
python setup.py
```

## Pull Request Workflow

1. **Create a Feature or Fix Branch:**
Always branch off `main` using a descriptive name:
```bash
git checkout -b fix/eval-parser-formatting
```

2. **Keep Changes Focused:**
Submit separate pull requests for unrelated changes (e.g., do not bundle a new Ollama Modelfile with a training script refactor).

4. **Verify Your Changes:**
* Ensure CLI utilities (`setup.py`, `download.py`) run cleanly without breaking cross-platform compatibility (Linux, macOS, Windows).
* If modifying training or evaluation scripts, test with a dry run or small sample subset (`--max_samples 50`).
* Update the relevant folder `README.md` if you add new CLI flags, config keys, or scripts.

4. **Commit & Push:**
Write clear, concise commit messages:
```bash
git add .
git commit -m "fix: handle missing accuracy keys in parse_results.py"
git push origin fix/eval-parser-formatting
```

5. **Open a Pull Request:**
Open a PR against `main` detailing what changed, why it was needed, and any hardware/environment specs used for testing.

## Licensing & Contributor Agreement

By submitting a contribution to this repository, you agree that your code, scripts, and documentation will be licensed under the **Apache License 2.0** (as specified in the root `LICENSE` file). Any contributions referencing or packaging base model weights must remain compliant with the upstream **Meta Llama Community Licenses** and `USE_POLICY.md`.

## Code of Conduct

All contributors and maintainers are expected to foster an open, respectful, and constructive technical community. Please review `CODE_OF_CONDUCT.md` before participating in issues or pull requests.
