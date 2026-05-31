import logging

from .config import LOG_FILE, LOGS_DIR

def setup_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logic.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, endcoding="unf-8"),
            logging.StreamHandler(),
        ],
    )