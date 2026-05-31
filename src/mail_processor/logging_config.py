import logging

from .config import LOG_FILE, LOGS_DIR, DEFAULT_ENCODING


def setup_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding=DEFAULT_ENCODING),
            logging.StreamHandler(),
        ],
    )
