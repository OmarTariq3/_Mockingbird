import platform
import subprocess
import sys
import os


def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing: {command}")
        sys.exit(1)


def get_system_info():
    system = platform.system().lower()
    processor = platform.machine().lower()
    return system, processor


def install_torch(system, processor):
    print(f"🔍 Detected System: {system.capitalize()} | Processor: {processor}")

    # 1. MAC OS (Apple Silicon / Intel)
    if system == "darwin":
        print(
            "🍎 macOS detected. Installing PyTorch with MPS (Metal Performance Shaders) support..."
        )
        run_command("pip install torch torchaudio")
        # macOS binaries automatically include MPS support in the standard package.

    # 2. LINUX or WINDOWS
    else:
        # Check for NVIDIA GPU (via nvidia-smi)
        try:
            subprocess.check_call(
                "nvidia-smi",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            has_nvidia = True
        except:
            has_nvidia = False

        if has_nvidia:
            print("🟢 NVIDIA GPU detected.")
            # SPECIAL CASE: RTX 50-Series (Blackwell) or very new cards
            # We default to Stable CUDA 12.1 unless the user specifically needs Nightly (like you did).
            # For general users, CUDA 12.1 is the safest "modern" bet.
            print("🚀 Installing PyTorch with CUDA 12.1 support...")
            run_command(
                "pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121"
            )

        # Check for AMD GPU (Linux only usually)
        elif system == "linux" and os.path.exists("/dev/kfd"):
            print("🔴 AMD ROCm GPU detected.")
            print("🚀 Installing PyTorch with ROCm 6.0 support...")
            run_command(
                "pip install torch torchaudio --index-url https://download.pytorch.org/whl/rocm6.0"
            )

        # Fallback: CPU Only
        else:
            print(
                "⚠️ No GPU detected. Installing CPU-only version (Running Whisper will be slow!)."
            )
            run_command(
                "pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu"
            )


def install_requirements():
    print("\n📦 Installing standard dependencies from requirements.txt...")
    run_command("pip install -r requirements.txt")


if __name__ == "__main__":
    print("=== 🛠️  Mockingbird Dependency Installer 🛠️ ===\n")

    # 1. Install System-Specific PyTorch
    system, processor = get_system_info()
    install_torch(system, processor)

    # 2. Install General Requirements
    install_requirements()

    print("\n✅ Installation Complete! Activate your venv and run: python main.py")
