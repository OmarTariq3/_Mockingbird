# 🐦 _Mockingbird

![Python](https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991.svg?style=for-the-badge&logo=openai&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-FF0000.svg?style=for-the-badge&logo=youtube&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)

**_Mockingbird** is a robust, modular, and GPU-accelerated audio transcription pipeline designed for production-scale workflows. It automates the extraction of audio from YouTube using `yt-dlp` and processes it locally using OpenAI's **Whisper** models.

Optimized for **NVIDIA GPUs (CUDA)** but compatible with Apple Silicon and CPU, _Mockingbird handles authentication challenges, resumes interrupted jobs automatically, and delivers high-fidelity transcripts without relying on expensive cloud APIs.

---

## ✨ Key Features

* **🚀 GPU Acceleration:** Fully optimized for CUDA (NVIDIA) and MPS (Apple Silicon).
* **🧠 Smart Resume:** Automatically tracks progress. Interruptions (Ctrl+C) save your state instantly.
* **🛡️ Anti-Bot Evasion:** Integrated with **Deno** and `cookies.txt` to handle YouTube's latest "Sign in to confirm you’re not a bot" challenges.
* **📊 Dual Input Support:** Reads video lists from a local CSV *or* connects directly to Google Sheets.
* **⚡ Whisper Turbo:** Default configuration uses the `turbo` model—offering `large-v3` accuracy at 8x the speed.
* **🧹 Auto-Cleanup:** Manages disk space by automatically deleting heavy audio files after successful transcription.

---

## ⚙️ System Requirements

### 1. Hardware (VRAM Guide)
Select a model based on your GPU memory. The default is `turbo` (Best balance).

| Model | Parameters | VRAM Required | Relative Speed | Quality |
| :--- | :--- | :--- | :--- | :--- |
| `tiny` | 39 M | ~1 GB | ~32x | Low |
| `base` | 74 M | ~1 GB | ~16x | Decent |
| `small` | 244 M | ~2 GB | ~6x | Good |
| `medium` | 769 M | ~5 GB | ~2x | Very Good |
| **`turbo`** | **809 M** | **~6 GB** | **~8x** | **Excellent** |
| `large-v3` | 1550 M | ~10 GB | 1x | Best |

### 2. Software Prerequisites
Before running the Python script, ensure you have these installed globally:

* **FFmpeg:** Required for audio conversion.
    * *Arch:* `sudo pacman -S ffmpeg`
    * *Ubuntu:* `sudo apt install ffmpeg`
    * *Mac:* `brew install ffmpeg`
    * *Windows:* `winget install ffmpeg`
* **Deno:** Required for solving YouTube JS challenges.
    * *Arch:* `sudo pacman -S deno`
    * *Mac/Linux:* `curl -fsSL https://deno.land/install.sh | sh`
    * *Windows:* `winget install Deno.Deno`

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/_Mockingbird.git](https://github.com/yourusername/_Mockingbird.git)
cd _Mockingbird
```

Here is the rest of the `README.md` file, continuing from where it cut off. You can append this directly to the previous part.

### 2. Create Virtual Environment
**Linux / macOS:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 3. Install Dependencies

We provide a smart installer that detects your OS/GPU and installs the correct PyTorch version (CUDA/ROCm/MPS) automatically.

```bash
python install.py

```

> **Manual Alternative:** If you prefer manual installation:
> * **NVIDIA (CUDA 12.1):** `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121`
> * **Mac (Silicon):** `pip install torch torchaudio`
> * **Then:** `pip install -r requirements.txt`
> 
> 

---

## 🔧 Configuration

### 1. Authentication (`cookies.txt`)

To download age-restricted or high-traffic videos, you must authenticate as a human.

1. Install the **"Get cookies.txt LOCALLY"** extension for Chrome/Firefox.
2. Log in to YouTube.
3. Export cookies and save the file as `cookies.txt` in the root folder.

### 2. Input Data (`src/config.py`)

You can configure the pipeline to read from a local file or Google Sheets.

**Option A: Local CSV (Recommended)**

1. Place a file named `input.csv` in the `data/` folder.
2. Ensure it has a column with YouTube IDs (e.g., `video_id`).
3. Update `src/config.py`:
```python
LOCAL_INPUT_FILE = "data/input.csv"
VIDEO_ID_COLUMN = "video_id"

```


**Option B: Google Sheets**

1. Set `LOCAL_INPUT_FILE = None`.
2. Add your Sheet ID in `src/config.py`.

---

## 🚀 Usage

Once configured, simply run the main orchestrator:

```bash
python main.py

```

**During Execution:**

* **Monitor:** The terminal will show a live progress bar for downloads and transcription.
* **Pause:** Press `Ctrl + C` **once** to safely stop. The script will finish the current batch, save progress to `data/transcripts.csv`, and exit.
* **Resume:** Run `python main.py` again. It will skip any videos already in `transcripts.csv`.

---

## 📂 Project Structure

```text
_Mockingbird/
├── cookies.txt          # YouTube Auth (Ignored by Git)
├── install.py           # Smart dependency installer
├── main.py              # Application Entry Point
├── requirements.txt     # Standard libraries
├── data/
│   ├── audio/           # Temp storage (Auto-cleared)
│   ├── backups/         # Backup Batch sessions
│   ├── input.csv        # Source video list
│   └── transcripts.csv  # Final Output
└── src/
    ├── config.py        # Settings (Model size, paths)
    ├── audio_manager.py # yt-dlp logic (Deno + Cookies)
    ├── transcriber.py   # Whisper inference engine
    └── data_handler.py  # CSV merging and state management

```

---

## ⚖️ License & Acknowledgements

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

**Acknowledgements:**

* **[OpenAI Whisper](https://github.com/openai/whisper):** State-of-the-art speech recognition model.
* **[yt-dlp](https://github.com/yt-dlp/yt-dlp):** The engine behind the media extraction.

```

```
