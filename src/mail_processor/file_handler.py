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
    
    def move_file_to_category(self, file_path: Path, category: str) -> Path:
        target_dir = PROCESSED_DIR / category
        target_path = target_dir / file_path.name
        
        try:
            file_path.rename(target_path)
            return target_path
        except Exception as e:
            raise Exception(f"Failed to move file {file_path} to {target_path}: {str(e)}")
    
    def handle_unknown_file(self, file_path: Path) -> bool:
        return self.move_file_to_category(file_path, "unknown")
    
    def handle_corrupted_file(self, file_path: Path) -> bool:
        return self.move_file_to_category(file_path, "corrupted")
    
    
