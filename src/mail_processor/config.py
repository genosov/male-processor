from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
INBOX_DIR = DATA_DIR / "inbox"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = DATA_DIR / "logs"

LOG_FILE = LOGS_DIR / "app.log"

DEFAULT_ENCODING = "utf-8"
SUPPORTED_EXTENSIONS = {".txt"}