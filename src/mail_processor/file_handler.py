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
        
        for directory_path in directories:
            try:
                directory_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                pass
    
    def scan_inbox(self) -> list[Path]:
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
    
    def get_file_metadata(self, file_path: Path) -> dict:
        return {
            "filename": file_path.name,
            "path": str(file_path),
            "size_bytes": file_path.stat().st_size,
            "extension": file_path.suffix.lower(),
            "created_at": file_path.stat().st_ctime,
            "modified": file_path.stat().st_mtime
        }
        
