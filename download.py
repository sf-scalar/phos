import os
import sys
from huggingface_hub import snapshot_download, login, HfApi


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


def print_banner():
    print("\n")
    print(
        f"  {badge('SCALAR PHOS')}  {Theme.BOLD}{Theme.WHITE}Model Download{Theme.RESET}"
    )
    print(
        f"  {Theme.GRAY}Hugging Face Hub Sync  •  LoRA Adapters  •  GGUF Binaries{Theme.RESET}"
    )


def check_auth():
    """Verifies Hugging Face authentication status from environment or cache."""
    hf_token = os.environ.get("HF_TOKEN")
    
    # Try loading from local .env if present
    if not hf_token and os.path.exists(".env"):
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        hf_token = line.strip().split("=", 1)[1]
                        os.environ["HF_TOKEN"] = hf_token
                        break
        except Exception:
            pass

    section("Authentication Status")
    if hf_token:
        print(f"  {badge('AUTH', 'pass')} {Theme.WHITE}Found `HF_TOKEN` environment variable.{Theme.RESET}")
        try:
            login(token=hf_token, add_to_git_credential=False)
            print(f"  {Theme.GREEN}Successfully authenticated with Hugging Face Hub.{Theme.RESET}")
        except Exception as e:
            print(f"  {badge('WARN', 'warn')} {Theme.YELLOW}Token validation warning: {e}{Theme.RESET}")
    else:
        print(
            f"  {badge('NOTICE', 'warn')} {Theme.YELLOW}No `HF_TOKEN` detected in environment or `.env`.{Theme.RESET}"
        )
        print(
            f"    {Theme.SILVER}Public repositories will download fine, but gated access or private telemetry requires a token.{Theme.RESET}"
        )


def download_model(repo_id, local_dir=None):
    """Downloads a model repository snapshot from Hugging Face."""
    section(f"Downloading: {repo_id}")
    print(f"  {Theme.SILVER}Target Repository : https://huggingface.co/{repo_id}{Theme.RESET}")
    if local_dir:
        print(f"  {Theme.SILVER}Destination Path  : ./{local_dir}{Theme.RESET}")
    print(f"  {Theme.GRAY}Fetching metadata and syncing shards (this may take a moment depending on connection)...{Theme.RESET}\n")

    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            resume_download=True,
            token=os.environ.get("HF_TOKEN")
        )
        print(f"\n  {badge('SUCCESS', 'pass')} {Theme.WHITE}Successfully downloaded `{repo_id}`!{Theme.RESET}")
    except Exception as e:
        print(f"\n  {badge('ERROR', 'error')} {Theme.RED}Failed to download `{repo_id}`.{Theme.RESET}")
        print(f"  {Theme.RED}Details: {e}{Theme.RESET}")


def interactive_menu():
    print_banner()
    check_auth()

    section("Select Target Models")
    print(f"  {Theme.WHITE}[1]{Theme.RESET} {Theme.BOLD}Scalar Phos Flash (3.2B){Theme.RESET} — `scalar-ai/scalar-phos-flash` (Fast edge model, LoRA + GGUF)")
    print(f"  {Theme.WHITE}[2]{Theme.RESET} {Theme.BOLD}Scalar Phos Pro (8.0B){Theme.RESET}   — `scalar-ai/scalar-phos-pro` (High-reasoning model, LoRA + GGUF)")
    print(f"  {Theme.WHITE}[3]{Theme.RESET} {Theme.BOLD}Both Models{Theme.RESET}               — Download the complete Scalar Phos ecosystem")
    print(f"  {Theme.WHITE}[4]{Theme.RESET} {Theme.DIM}Exit{Theme.RESET}")

    try:
        choice = input(f"\n  {Theme.BOLD}{Theme.WHITE}Enter your selection [1-4]: {Theme.RESET}").strip()
    except KeyboardInterrupt:
        print(f"\n\n  {Theme.GRAY}Download cancelled by user.{Theme.RESET}\n")
        sys.exit(0)

    if choice == "1":
        download_model("scalar-ai/scalar-phos-flash", local_dir="scalar-phos-flash")
    elif choice == "2":
        download_model("scalar-ai/scalar-phos-pro", local_dir="scalar-phos-pro")
    elif choice == "3":
        download_model("scalar-ai/scalar-phos-flash", local_dir="scalar-phos-flash")
        download_model("scalar-ai/scalar-phos-pro", local_dir="scalar-phos-pro")
    elif choice == "4":
        print(f"\n  {Theme.GRAY}Exiting downloader. Have a great day!{Theme.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n  {badge('ERROR', 'error')} {Theme.RED}Invalid selection. Please run the script again and choose 1–4.{Theme.RESET}\n")


if __name__ == "__main__":
    interactive_menu()
