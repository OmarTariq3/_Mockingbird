import pandas as pd
import os
from datetime import datetime
from src.config import (
    SHEET_URL,
    LOCAL_INPUT_FILE,
    OUTPUT_FILE,
    BACKUP_DIR,
    VIDEO_ID_COLUMN,
)


def load_data():
    """Loads fresh data from Local CSV or Google Sheets."""

    if LOCAL_INPUT_FILE and os.path.exists(LOCAL_INPUT_FILE):
        print(f"📂  Loading input data from LOCAL file: {LOCAL_INPUT_FILE}")
        df_fresh = pd.read_csv(LOCAL_INPUT_FILE)
    else:
        print("☁️  Loading input data from GOOGLE SHEETS...")
        df_fresh = pd.read_csv(SHEET_URL)

    if VIDEO_ID_COLUMN not in df_fresh.columns:
        raise ValueError(
            f"❌ Error: Input data is missing the column '{VIDEO_ID_COLUMN}'. Found: {list(df_fresh.columns)}"
        )

    # Normalize the ID column to strings (crucial for IDs starting with 0 or containing numbers)
    df_fresh[VIDEO_ID_COLUMN] = df_fresh[VIDEO_ID_COLUMN].astype(str).str.strip()

    if os.path.exists(OUTPUT_FILE):
        print("resume found: Loading existing progress...")
        df_existing = pd.read_csv(OUTPUT_FILE)

        # Use the config variable for merging too
        if VIDEO_ID_COLUMN in df_existing.columns:
            df_existing[VIDEO_ID_COLUMN] = (
                df_existing[VIDEO_ID_COLUMN].astype(str).str.strip()
            )

            # Map existing transcripts based on the dynamic column name
            existing_map = df_existing.set_index(VIDEO_ID_COLUMN)["transcript"].dropna()
            df_fresh["transcript"] = (
                df_fresh[VIDEO_ID_COLUMN]
                .map(existing_map)
                .fillna(df_fresh.get("transcript", pd.NA))
            )

    return df_fresh


def get_resume_index(df):
    """Finds the first row without a transcript."""
    remaining = df[df["transcript"].isna()]
    if remaining.empty:
        return None
    return remaining.index[0]


def save_progress(df, batch_label=None):
    """Saves main file and a timestamped backup."""
    df.to_csv(OUTPUT_FILE, index=False)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = (
        f"backup_{batch_label}_{timestamp}.csv"
        if batch_label
        else f"backup_{timestamp}.csv"
    )

    backup_path = os.path.join(BACKUP_DIR, backup_name)
    df.to_csv(backup_path, index=False)
    print(f"💾 Saved progress to {OUTPUT_FILE}")
