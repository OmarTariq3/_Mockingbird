import os
import glob
from yt_dlp import YoutubeDL
from src.config import AUDIO_DIR


def find_audio_file(video_id):
    """Finds existing audio file regardless of extension."""
    patterns = [
        f"{video_id}.mp3",
        f"{video_id}.m4a",
        f"{video_id}.webm",
        f"{video_id}.wav",
    ]

    for ext in patterns:
        path = os.path.join(AUDIO_DIR, ext)
        if os.path.exists(path):
            return path

    # Fallback wildcard search
    files = glob.glob(os.path.join(AUDIO_DIR, f"{video_id}.*"))
    return files[0] if files else None


def download_audio(video_id):
    """Downloads audio using yt-dlp."""
    path = os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s")

    cookies_path = os.path.abspath("cookies.txt")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": path,
        "quiet": True,
        "noplaylist": True,
        "extractaudio": True,
        "audioformat": "mp3",
        "cookiefile": cookies_path,
        "sleep_interval": 3,  # Wait 3 sec between downloads to be polite
        "max_sleep_interval": 10,  # Randomize wait time (3-10s) to look human
        "remote_components": ["ejs:github"],  # JS puzzle solver handled by deno
        # -----------------------
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=True
            )
            return info.get("duration", 0)

    except Exception as e:
        print(f"❌ Error downloading {video_id}: {e}")
        return None


def cleanup_audio(path):
    """Removes audio file after processing."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"⚠️ Could not delete {path}: {e}")
