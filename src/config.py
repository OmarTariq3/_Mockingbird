import os

# =============================================================================
# 📂 PROJECT PATHS (Do Not Modify)
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
OUTPUT_FILE = os.path.join(DATA_DIR, "transcripts.csv")

# =============================================================================
# ⚙️ PROCESSING SETTINGS
# =============================================================================
# How many videos to process before saving a backup checkpoint.
# Lower = Safer (less data loss on crash). Higher = Slightly faster.
BATCH_SIZE = 25

# =============================================================================
# 📝 INPUT DATA CONFIGURATION
# =============================================================================

# 1. COLUMN MAPPING
# What is the header name of the column containing YouTube IDs in your CSV/Sheet?
# Common examples: "video_id", "id", "url", "Link"
VIDEO_ID_COLUMN = "video_id"

# 2. INPUT SOURCE SELECTION
# -----------------------------------------------------------------------------
# OPTION A: Local CSV File (Recommended for most users)
# Put your CSV file inside the 'data/' folder and write its filename here.
# Set this to None if you want to use Google Sheets instead.
# Example: LOCAL_INPUT_FILE = "my_video_list.csv"
LOCAL_INPUT_FILE = "input.csv"

# OPTION B: Google Sheets (Remote)
# If LOCAL_INPUT_FILE is None, the script will fetch data from this Sheet ID.
# Ensure the Sheet is "Anyone with the link can view".
SHEET_ID = "ID goes here"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Helper logic to build full path (Do not modify)
if LOCAL_INPUT_FILE:
    LOCAL_INPUT_FILE = os.path.join(DATA_DIR, LOCAL_INPUT_FILE)

# =============================================================================
# 🧠 AI MODEL SETTINGS
# =============================================================================
# Model Size: Determines accuracy vs. speed.
# Options: "tiny", "base", "small", "medium", "large-v3", "turbo"
# "turbo" is recommended for high-end GPUs (RTX 3060+).
MODEL_SIZE = "turbo"

# Language Code: Improves accuracy if known.
# Examples: "en" (English), "ar" (Arabic), "fr" (French), "es" (Spanish)
# Set to None to let Whisper auto-detect language (slower).
LANGUAGE = "ar"
