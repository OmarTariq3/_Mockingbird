import time
import os
from src.config import BATCH_SIZE, AUDIO_DIR, BACKUP_DIR, VIDEO_ID_COLUMN
from src.audio_manager import download_audio, find_audio_file, cleanup_audio
from src.transcriber import load_whisper_model, transcribe
from src.data_handler import load_data, get_resume_index, save_progress


def process_batch(df, start, end, model):
    """Process a single batch of videos."""
    for idx in range(start, end):
        row = df.iloc[idx]
        video_id = row[VIDEO_ID_COLUMN]

        if pd.notna(row.get("transcript")):
            continue

        print(f"Processing {idx + 1}/{len(df)}: {video_id}")

        # 1. Download
        audio_path = find_audio_file(video_id)

        if not audio_path:
            duration_secs = download_audio(video_id)

            if duration_secs:
                print(f"   ⏱️  Duration: {format_seconds(duration_secs)}")

                audio_path = find_audio_file(video_id)
            else:
                continue  # Skip if download failed

        # 2. Transcribe
        if audio_path:
            text = transcribe(audio_path, model)
            if text:
                df.loc[idx, "transcript"] = text
                print("✅ Transcribed")
                cleanup_audio(audio_path)
            else:
                print("❌ Transcription failed (empty result)")


def format_seconds(seconds):
    """Converts 350 -> '05:50'"""
    if not seconds:
        return "?"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"  # Hours:Mins:Secs
    return f"{m}:{s:02d}"  # Mins:Secs


def main():
    # Setup directories
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Initialization
    model = load_whisper_model()
    df = load_data()
    start_index = get_resume_index(df)

    if start_index is None:
        print("🎉 All videos already processed!")
        return

    total_batches = ((len(df) - start_index) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"🏁 Starting at index {start_index} | Total Batches: {total_batches}")

    # Main Loop
    for i, batch_start in enumerate(range(start_index, len(df), BATCH_SIZE)):
        batch_num = i + 1
        batch_end = min(batch_start + BATCH_SIZE, len(df))

        print(
            f"\n=== Batch {batch_num}/{total_batches} (Rows {batch_start}-{batch_end}) ==="
        )

        try:
            process_batch(df, batch_start, batch_end, model)
            save_progress(df, batch_label=str(batch_num))
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Saving...")
            save_progress(df, batch_label="interrupted")
            break
        except Exception as e:
            print(f"\n💥 Critical Batch Error: {e}")
            save_progress(df, batch_label="error")


if __name__ == "__main__":
    import pandas as pd  # Local import if needed

    main()
