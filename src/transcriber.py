import whisper
import torch
import time
from src.config import MODEL_SIZE, LANGUAGE


def load_whisper_model():
    """Load the Whisper model."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Loading Whisper model '{MODEL_SIZE}' on {device}...")
    return whisper.load_model(MODEL_SIZE, device=device)


def transcribe(audio_path, model):
    """
    Transcribes audio using Whisper's built-in progress bar.
    """
    try:
        start_time = time.time()

        # verbose=False + status messages
        # By setting verbose=False but NOT suppressing stderr,
        # Whisper's internal tqdm progress bar will show up.
        print(f"   🎙️  Transcribing {audio_path.split('/')[-1]}...")

        result = model.transcribe(
            audio_path,
            language=LANGUAGE,
            verbose=False,  # Keeps the 'Matrix' text away
            fp16=torch.cuda.is_available(),
        )

        total_time = time.time() - start_time
        print(f"   ✅ Finished in {total_time:.1f}s")

        return result["text"]

    except KeyboardInterrupt:
        # Standard Python interrupt handling
        print("\n\n🛑 Stop signal received. Saving progress...")
        raise
    except Exception as e:
        print(f"\n❌ Transcription error: {e}")
        return None
