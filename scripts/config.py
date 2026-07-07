from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folders
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
SCREENSHOT_DIR = DATA_DIR / "screenshots"
PROCESSED_DIR = DATA_DIR / "processed"

# Output folders
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = BASE_DIR / "reports"

# Create folders automatically
for folder in [
    RAW_DIR,
    SCREENSHOT_DIR,
    PROCESSED_DIR,
    OUTPUT_DIR,
    REPORT_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)
