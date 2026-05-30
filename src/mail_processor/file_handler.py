from config import (
    ROOT_DIR, DATA_DIR, INBOX_DIR, PROCESSED_DIR, LOGS_DIR,
    LOG_FILE, DEFAULT_ENCODING, SUPPORTED_EXTENSIONS
)
from models import CATEGORIES
from pathlib import Path


class FileHandler:
    def __init__(self):
        self.categories = CATEGORIES
        self.initialize_directories()

    def initialize_directories(self):
        directories = [INBOX_DIR, PROCESSED_DIR, LOGS_DIR]
        for category in self.categories:
            directories.append(PROCESSED_DIR / category)
    
    def scan_inbox(self) -> list[str]:
        files = []
        
        for file in INBOX_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(file)

        return files
    
    def classify_file(self, file_path: Path) -> str:
        for extension in SUPPORTED_EXTENSIONS:
            if extension == file_path.suffix.lower():
                return extension
        return "unknown"
    

        