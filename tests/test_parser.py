import sys
from pathlib import Path
import pytest
sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "mail_processor"))
from src.mail_processor.parser import EmailParser


def test_parse_normal_email(tmp_path):
    email_file= tmp_path / "mail.txt"
    email_file.write_text("From: user@mail.com\nSubject: Test mail\n\nHello",encoding="utf-8" )
    email = EmailParser().parse(email_file)
    assert email.filename == "mail.txt"
    assert email.source_path == str(email_file)
    assert email.sender == "user@mail.com"
    assert email.subject == "Test mail"
    assert email.body == "Hello"
    assert email.raw_content == "From: user@mail.com\nSubject: Test mail\n\nHello"

def test_parse_without_headers(tmp_path):
    email_file= tmp_path / "mail.txt"
    email_file.write_text("Line1\nLine2",encoding="utf-8" )
    email = EmailParser().parse(email_file)
    assert email.filename == "mail.txt"
    assert email.source_path == str(email_file)
    assert email.sender == "unknown_sender"
    assert email.subject == ""
    assert email.body == "Line1 Line2"
    assert email.raw_content == "Line1\nLine2"

def test_empty_file(tmp_path):
    email_file = tmp_path / "empty.txt"
    email_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError) as error:
        EmailParser().parse(email_file)
    assert "empty" in str(error.value)

def test_wrong_extension(tmp_path):
    email_file = tmp_path / "empty.doc"
    email_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError) as error:
        EmailParser().parse(email_file)
    assert ".doc" in str(error.value)

def test_missing_file(tmp_path):
    email_file = tmp_path / "missing.txt"
    with pytest.raises(FileNotFoundError) as error:
        EmailParser().parse(email_file)
    assert "missing.txt" in str(error.value)






    
