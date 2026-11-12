import os
import platform
import shutil
import subprocess
import sys


# ==============================================================================
# THEME & BRAND PALETTE (Monochrome Base with Semantic Accents)
# ==============================================================================
class Theme:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    INVERT = "\033[7m"  # Black text on White background (Brand Signature)

    WHITE = "\033[97m"  # Pure Bright White
    SILVER = "\033[37m"  # Standard Light Gray
    GRAY = "\033[90m"  # Muted Charcoal / Border Gray

    # Semantic Accent Colors
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[36m"


# Enable ANSI escape codes natively on Windows terminals
if os.name == "nt":
    os.system("")


def badge(text, status="neutral"):
    if status == "pass" or status == "optimal":
        return f"{Theme.BOLD}\033[42m\033[30m {text} {Theme.RESET}"
    elif status == "warn":
        return f"{Theme.BOLD}\033[43m\033[30m {text} {Theme.RESET}"
    elif status == "error":
        return f"{Theme.BOLD}\033[41m\033[97m {text} {Theme.RESET}"
    return f"{Theme.BOLD}{Theme.INVERT} {text} {Theme.RESET}"


def section(title):
    line = "─" * 68
    print(f"\n{Theme.GRAY}{line}{Theme.RESET}")
    print(f"  {Theme.BOLD}{Theme.WHITE}{title}{Theme.RESET}")
    print(f"{Theme.GRAY}{line}{Theme.RESET}")


def advisory_note(title, explanation, recommendation):
    """Prints a structured technical advisory block with colored recommendations."""
    print(f"\n  {Theme.BOLD}{Theme.WHITE}▸ {title}{Theme.RESET}")
    print(f"    {Theme.SILVER}{explanation}{Theme.RESET}")
    print(
        f"    {Theme.CYAN}{Theme.BOLD}Recommendation:{Theme.RESET} {Theme.ITALIC}{Theme.SILVER}{recommendation}{Theme.RESET}"
    )


def print_banner():
    print("\n")
    print(
        f"  {badge('SCALAR PHOS')}  {Theme.BOLD}{Theme.WHITE}Environment Setup{Theme.RESET}"
    )


def get_system_specs():
    """Gathers cross-platform hardware specs without external dependencies."""
    os_name = platform.system()
    py_ver = sys.version_info

    _, _, free_bytes = shutil.disk_usage(".")
    free_gb = free_bytes / (1024**3)

    ram_gb = 0.0
    try:
        if os_name == "Linux":
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        ram_gb = int(line.split()[1]) / (1024**2)
                        break
        elif os_name == "Windows":
            out = subprocess.check_output(
                ["wmic", "computersystem", "get", "TotalPhysicalMemory"], text=True
            )
            ram_bytes = [int(s) for s in out.split() if s.isdigit()][0]
            ram_gb = ram_bytes / (1024**3)
        elif os_name == "Darwin":
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True)
            ram_gb = int(out.strip()) / (1024**3)
    except Exception:
        pass

    has_nvidia = False
    vram_gb = 0.0
    gpu_name = "None (CPU / Integrated Graphics)"

    if shutil.which("nvidia-smi"):
        try:
            smi_out = (
                subprocess.check_output(
                    [
                        "nvidia-smi",
                        "--query-gpu=name,memory.total",
                        "--format=csv,noheader,nounits",
                    ],
                    text=True,
                )
                .strip()
                .splitlines()[0]
            )
            raw_name, vram_mb = smi_out.split(",")
            gpu_name = raw_name.strip()
            vram_gb = float(vram_mb.strip()) / 1024
            has_nvidia = True
        except Exception:
            pass

    if os_name == "Darwin" and platform.machine() == "arm64":
        gpu_name = f"Apple Silicon Unified Memory ({platform.processor() or 'ARM64'})"

    return {
        "os": f"{os_name} {platform.release()}",
        "arch": platform.machine(),
        "python": f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}",
        "py_tuple": (py_ver.major, py_ver.minor),
        "ram_gb": ram_gb,
        "disk_gb": free_gb,
        "has_nvidia": has_nvidia,
        "gpu_name": gpu_name,
        "vram_gb": vram_gb,
    }


def run_diagnostics():
    specs = get_system_specs()

    # --------------------------------------------------------------------------
    # 1. SYSTEM INFORMATION MATRIX
    # --------------------------------------------------------------------------
    section("System Information")

    rows = [
        ("Operating System", f"{specs['os']} ({specs['arch']})"),
        ("Python Runtime", f"Python {specs['python']}"),
        ("System Memory (RAM)", f"{specs['ram_gb']:.1f} GB" if specs["ram_gb"] > 0 else "Unknown"),
        ("Available Storage", f"{specs['disk_gb']:.1f} GB Free"),
        ("Compute Accelerator", specs["gpu_name"]),
        ("Dedicated VRAM", f"{specs['vram_gb']:.1f} GB" if specs["has_nvidia"] else "Shared / None"),
    ]

    for label, val in rows:
        print(
            f"  {Theme.GRAY}│{Theme.RESET} {Theme.SILVER}{label:<22}{Theme.RESET} {Theme.BOLD}{Theme.WHITE}{val}{Theme.RESET}"
        )

    # --------------------------------------------------------------------------
    # 2. ARCHITECTURAL ASSESSMENT & RECOMMENDATIONS
    # --------------------------------------------------------------------------
    section("Architectural Assessment & Recommendations")

    # Python Runtime Check
    if (3, 11) <= specs["py_tuple"] <= (3, 13):
        print(
            f"  {badge('PASS', 'pass')} {Theme.WHITE}Runtime Version Verified (Python {specs['python']}){Theme.RESET}"
        )
    else:
        print(
            f"  {badge('WARN', 'warn')} {Theme.YELLOW}Runtime Version Mismatch (Python {specs['python']}){Theme.RESET}"
        )
        advisory_note(
            "Kernel & Wheel Compatibility",
            "Unsloth, Triton, and vLLM rely on pre-compiled CUDA wheels targeted specifically at Python 3.11 through 3.13. Running outside this window frequently triggers source-build failures.",
            "Provision an isolated virtual environment using Python 3.11 or 3.12.",
        )

    # Storage Check
    if specs["disk_gb"] >= 30.0:
        print(
            f"  {badge('PASS', 'pass')} {Theme.WHITE}Storage Capacity Verified ({specs['disk_gb']:.1f} GB Available){Theme.RESET}"
        )
    else:
        print(
            f"  {badge('WARN', 'warn')} {Theme.YELLOW}Constrained Disk Overhead ({specs['disk_gb']:.1f} GB Available){Theme.RESET}"
        )
        advisory_note(
            "Model Shard & Quantization Staging",
            "Fine-tuning Llama models requires caching base safetensors (~6–16 GB), writing intermediate LoRA checkpoints, and staging temporary FP16 merges before GGUF quantization.",
            "Free up at least 30 GB of NVMe/SSD space or set `HF_HOME` to point to a secondary high-capacity drive.",
        )

    # Compute & VRAM Tier Analysis
    vram = specs["vram_gb"]
    ram = specs["ram_gb"]

    if specs["has_nvidia"] and vram >= 14.0:
        print(
            f"  {badge('OPTIMAL', 'pass')} {Theme.WHITE}Full-Stack Training & Evaluation Workstation ({vram:.1f} GB VRAM){Theme.RESET}"
        )
        advisory_note(
            "Compute Capabilities",
            "Your GPU meets or exceeds the memory envelope of an NVIDIA T4 (16 GB). You can execute 4-bit QLoRA fine-tuning and GGUF export locally.",
            "Train both Scalar Phos Flash (3B) and Pro (8B) locally. Keep `gpu_memory_utilization=0.6` during evaluation runs to prevent KV-cache OOMs.",
        )

    elif specs["has_nvidia"] and 4.0 <= vram < 14.0:
        print(
            f"  {badge('PARTIAL', 'warn')} {Theme.YELLOW}Entry-Level CUDA Accelerator ({vram:.1f} GB VRAM){Theme.RESET}"
        )
        advisory_note(
            "Memory Envelope & Batch Sizing",
            "4-bit QLoRA on a 3.2B parameter model requires ~3.5–4.5 GB of VRAM at batch size 1, whereas an 8B model requires ~6.5–8.0 GB before activation overhead.",
            "Use this machine for Scalar Phos Flash (3B) adapter tuning with `per_device_train_batch_size=1`. Offload 8B Pro training to Google Colab.",
        )

    else:
        print(
            f"  {badge('EDGE MODE', 'neutral')} {Theme.WHITE}CPU / Integrated Graphics Execution Profile ({ram:.1f} GB System RAM){Theme.RESET}"
        )
        advisory_note(
            "Training vs. Edge Inference Separation",
            "Unsloth quantization kernels and vLLM require an NVIDIA CUDA architecture and cannot execute training loops on CPU or integrated graphics. However, quantized GGUF binaries (`Q4_K_M`) require only ~2.2 GB of RAM for Scalar Phos Flash (3B).",
            "Adopt a split workflow: execute QLoRA training on cloud T4 GPUs (Google Colab), and use this machine as a zero-cost local inference node via Ollama (`ollama run hf.co/scalar-ai/scalar-phos-flash:Q4_K_M`).",
        )


def install_environment():
    section("Dependency Provisioning")

    if not os.path.exists("requirements.txt"):
        print(
            f"  {badge('ERROR', 'error')} {Theme.RED}`requirements.txt` not found in root directory.{Theme.RESET}"
        )
        return

    print(f"  {Theme.SILVER}[1/3] Upgrading pip build toolchain...{Theme.RESET}")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False
    )

    print(
        f"  {Theme.SILVER}[2/3] Resolving Unsloth & PyTorch CUDA kernels...{Theme.RESET}"
    )
    res = subprocess.run(
        [sys.executable, "-m", "pip", "install", "unsloth"], check=False
    )
    if res.returncode != 0:
        print(
            f"  {Theme.GRAY}      Note: Unsloth skipped or failed (expected on CPU-only/macOS environments).{Theme.RESET}"
        )

    print(
        f"  {Theme.SILVER}[3/3] Installing repository packages from requirements.txt...{Theme.RESET}"
    )
    req_res = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        check=False,
    )

    if not os.path.exists(".env.example"):
        with open(".env.example", "w") as f:
            f.write("# Scalar Phos Environment Configuration\n")
            f.write("# Rename this file to .env and populate your tokens\n\n")
            f.write("HF_TOKEN=hf_your_hugging_face_write_token_here\n")
            f.write("WANDB_API_KEY=\n")
        print(
            f"  {Theme.GREEN}[+] Generated `.env.example` credential template.{Theme.RESET}"
        )

    print()
    if req_res.returncode == 0:
        print(
            f"  {badge('COMPLETE', 'pass')} {Theme.WHITE}Development environment successfully provisioned.{Theme.RESET}"
        )
    else:
        print(
            f"  {badge('NOTICE', 'warn')} {Theme.YELLOW}Some GPU-specific packages exited with warnings. Review logs above.{Theme.RESET}"
        )


if __name__ == "__main__":
    print_banner()
    run_diagnostics()

    if "--check-only" in sys.argv:
        print(
            f"\n  {Theme.GRAY}Diagnostic mode complete. Run `python setup.py` without flags to provision packages.{Theme.RESET}\n"
        )
        sys.exit(0)

    section("Interactive Provisioning")
    try:
        prompt = f"  {Theme.BOLD}{Theme.WHITE}Proceed with installing dependencies into active Python environment? [y/N]: {Theme.RESET}"
        choice = input(prompt).strip().lower()
    except KeyboardInterrupt:
        print(f"\n\n  {Theme.GRAY}Setup aborted by user.{Theme.RESET}\n")
        sys.exit(0)

    if choice == "y":
        install_environment()
    else:
        print(
            f"\n  {Theme.GRAY}Provisioning skipped. Hardware diagnostics complete.{Theme.RESET}\n"
        )
