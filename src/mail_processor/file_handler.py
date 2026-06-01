from .config import INBOX_DIR, PROCESSED_DIR, LOGS_DIR, SUPPORTED_EXTENSIONS
from .models import CATEGORIES
from pathlib import Path
import shutil
import logging 

logger = logging.getLogger(__name__)
class FileHandler:
    def __init__(self):
        self.categories = CATEGORIES
        self._initialize_directories()

    def _initialize_directories(self):
        directories = [INBOX_DIR, PROCESSED_DIR, LOGS_DIR]
        for category in self.categories:
            directories.append(PROCESSED_DIR / category)
        
        for directory_path in directories:
            try:
                directory_path.mkdir(parents=True, exist_ok=True)
            except Exception as error:
                logger.error(f"Error occurred while creating directory {directory_path}: {error}")
    
    def scan_inbox(self) -> list[Path]:
        files = []
        for file in INBOX_DIR.iterdir():
            if file.is_file():
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
    
    def _generate_unique_filename(self, destination_dir: Path, filename: str) -> Path:
        cur_path = destination_dir / filename
        if not cur_path.exists():
            return cur_path
        cur_name = cur_path.stem
        extension = cur_path.suffix
        time_of_creation = int(cur_path.stat().st_ctime)
        new_filename = f"{cur_name}_{time_of_creation}{extension}"
        return destination_dir / new_filename
    
    def move_file_to_category(self, file_path: Path, category: str) -> Path | None:
        target_dir = PROCESSED_DIR / category
        destination_path = self._generate_unique_filename(target_dir, file_path.name)
        if not target_dir.exists():
            logger.exception(f"Target directory {target_dir} does not exist for category {category}")
            return None
        try:
            shutil.move(str(file_path), str(destination_path))
            return destination_path
        except Exception as error:
            logger.exception(f"Error occurred while moving file {file_path} to category {category}: {error}")
            return None

    
