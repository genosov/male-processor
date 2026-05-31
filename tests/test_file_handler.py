import pytest

import src.mail_processor.config as config
import src.mail_processor.file_handler as file_handler_module
from src.mail_processor.file_handler import FileHandler


INBOX_DIR = config.INBOX_DIR
PROCESSED_DIR = config.PROCESSED_DIR
LOGS_DIR = config.LOGS_DIR


@pytest.fixture(autouse=True)
def fake_directories(tmp_path, monkeypatch):
    global INBOX_DIR, PROCESSED_DIR, LOGS_DIR

    INBOX_DIR = tmp_path / "inbox"
    PROCESSED_DIR = tmp_path / "processed"
    LOGS_DIR = tmp_path / "logs"

    monkeypatch.setattr(config, "INBOX_DIR", INBOX_DIR)
    monkeypatch.setattr(config, "PROCESSED_DIR", PROCESSED_DIR)
    monkeypatch.setattr(config, "LOGS_DIR", LOGS_DIR)

    monkeypatch.setattr(file_handler_module, "INBOX_DIR", INBOX_DIR)
    monkeypatch.setattr(file_handler_module, "PROCESSED_DIR", PROCESSED_DIR)
    monkeypatch.setattr(file_handler_module, "LOGS_DIR", LOGS_DIR)

def test_initialize_directories():
    filehandler = FileHandler()
    assert INBOX_DIR.exists()
    assert PROCESSED_DIR.exists()
    assert LOGS_DIR.exists()

    for category in filehandler.categories:
        assert (PROCESSED_DIR / category).exists()

def test_scan_inbox_if_empty():
    handler = FileHandler()
    files = handler.scan_inbox()
    assert files == []

def test_scan_inbox_with_files():
    handler = FileHandler()
    file1 = INBOX_DIR / "file1.txt"
    file1.touch()
    file2 = INBOX_DIR / "file2.pdf"
    file2.touch()
    file3 = INBOX_DIR / "file3.json"
    file3.touch()

    files = handler.scan_inbox()

    assert len(files) == 3
    assert file1 in files
    assert file2 in files
    assert file3 in files

def test_classify_file():
    handler = FileHandler()
    file1 = INBOX_DIR / "file1.txt"
    file1.touch()
    file2 = INBOX_DIR / "file2.pdf"
    file2.touch()
    file3 = INBOX_DIR / "file3.json"
    file3.touch()
    assert handler.classify_file(file1) == ".txt"
    assert handler.classify_file(file2) == "unknown"   
    assert handler.classify_file(file3) == "unknown"

def test_get_file_metadata():
    handler = FileHandler()
    file1 = INBOX_DIR / "file.txt"
    file1.touch()
    metadata = handler.get_file_metadata(file1)
    assert metadata["filename"] == "file.txt"
    assert metadata["path"] == str(file1)
    assert metadata["size_bytes"] == 0
    assert metadata["extension"] == ".txt"
    assert isinstance(metadata["created_at"], float)
    assert isinstance(metadata["modified"], float)

def test_move_file_to_category():
    handler = FileHandler()
    file1 = INBOX_DIR / "file.txt"
    file1.touch()
    category = "support"
    destination_path = handler.move_file_to_category(file1, category)
    assert destination_path is not None
    assert destination_path.exists()
    assert not file1.exists()

def test_move_file_to_category_with_the_same_filename():
    handler = FileHandler()
    file1 = INBOX_DIR / "file.txt"
    file1.touch()
    category = "support"
    destination_path1 = handler.move_file_to_category(file1, category)
    assert destination_path1 is not None
    assert destination_path1.exists()
    assert not file1.exists()

    file2 = INBOX_DIR / "file.txt"
    file2.touch()
    destination_path2 = handler.move_file_to_category(file2, category)
    assert destination_path2 is not None
    assert destination_path2.exists()
    assert destination_path1 != destination_path2
    
def test_move_file_to_category_with_nonexistent_category():
    handler = FileHandler()
    file1 = INBOX_DIR / "file.txt"
    file1.touch()
    category = "some_category"
    destination_path = handler.move_file_to_category(file1, category)
    assert destination_path is None
    assert file1.exists()