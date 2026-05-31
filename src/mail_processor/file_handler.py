from config import INBOX_DIR, PROCESSED_DIR, LOGS_DIR, SUPPORTED_EXTENSIONS
from models import CATEGORIES
from pathlib import Path
import shutil

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
    
    def generate_unique_filename(self, destination_dir: Path, filename: str) -> Path:
        cur_path = destination_dir / filename
        if not cur_path.exists():
            return cur_path
        cur_name = cur_path.stem
        extension = cur_path.suffix
        time_of_creation = int(cur_path.stat().st_ctime)
        new_filename = f"{cur_name}_{time_of_creation}{extension}"
        return destination_dir / new_filename
    
    def move_file_to_category(self, file_path: Path, category: str) -> Path:
        target_dir = PROCESSED_DIR / category
        destination_path = self.generate_unique_filename(target_dir, file_path.name)
        try:
            shutil.move(str(file_path), str(destination_path))
            return destination_path
        except Exception as e:
            pass 

    
