import pytest

from src.mail_processor.parser import EmailParser


def test_parse_normal_email(tmp_path):
    email_file = tmp_path / "mail.txt"
    email_file.write_text(
        "From: user@mail.com\nSubject: Test mail\n\nHello",
        encoding="utf-8",
    )

    email = EmailParser().parse(email_file)

    assert email.filename == "mail.txt"
    assert email.source_path == str(email_file)
    assert email.sender == "user@mail.com"
    assert email.subject == "Test mail"
    assert email.body == "Hello"
    assert email.raw_content == "From: user@mail.com\nSubject: Test mail\n\nHello"


def test_parse_without_headers(tmp_path):
    email_file = tmp_path / "mail.txt"
    email_file.write_text("Line1\nLine2", encoding="utf-8")

    email = EmailParser().parse(email_file)

    assert email.filename == "mail.txt"
    assert email.source_path == str(email_file)
    assert email.sender == "unknown_sender"
    assert email.subject == ""
    assert email.body == "Line1 Line2"
    assert email.raw_content == "Line1\nLine2"


def test_parse_russian_headers(tmp_path):
    email_file = tmp_path / "mail.txt"
    email_file.write_text(
        "\n".join(
            [
                "От кого: Иван Петров <i.petrov@company.ru>",
                "Кому: it-support@company.ru",
                "Дата: 01.06.2026",
                "Тема: Запрос доступа",
                "",
                "Прошу выдать доступ к VPN.",
            ]
        ),
        encoding="utf-8",
    )

    email = EmailParser().parse(email_file)

    assert email.sender == "Иван Петров <i.petrov@company.ru>"
    assert email.subject == "Запрос доступа"
    assert email.body == "Прошу выдать доступ к VPN."
    assert "Кому:" not in email.body
    assert "Дата:" not in email.body


def test_parse_removes_service_headers_from_body(tmp_path):
    email_file = tmp_path / "mail.txt"
    email_file.write_text(
        "\n".join(
            [
                "From: user@mail.com",
                "To: it-support@company.ru",
                "Date: 2026-06-01",
                "Subject: Test",
                "",
                "First line",
                "Second line",
            ]
        ),
        encoding="utf-8",
    )

    email = EmailParser().parse(email_file)

    assert email.body == "First line Second line"
    assert "To:" not in email.body
    assert "Date:" not in email.body


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
