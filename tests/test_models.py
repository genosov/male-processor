from src.mail_processor.models import (
    CATEGORIES,
    ClassificationResult,
    EmailMessage,
    ProcessingResult,
    ProcessingStats,
)


def test_categories_include_supported_pipeline_categories():
    assert CATEGORIES == [
        "critical",
        "support",
        "business",
        "info",
        "spam",
        "unknown",
        "corrupted",
    ]


def test_email_message_defaults():
    email = EmailMessage(
        filename="mail.txt",
        source_path="/tmp/mail.txt",
    )

    assert email.filename == "mail.txt"
    assert email.source_path == "/tmp/mail.txt"
    assert email.subject == ""
    assert email.sender == "unknown_sender"
    assert email.body == ""
    assert email.raw_content == ""


def test_classification_result_uses_independent_matched_rules_lists():
    first_result = ClassificationResult(category="support")
    second_result = ClassificationResult(category="spam")

    first_result.matched_rules.append("support: help")

    assert first_result.matched_rules == ["support: help"]
    assert second_result.matched_rules == []


def test_processing_result_defaults_to_success_without_error():
    result = ProcessingResult(
        filename="mail.txt",
        source_path="/tmp/inbox/mail.txt",
        destination_path="/tmp/processed/support/mail.txt",
        category="support",
    )

    assert result.success is True
    assert result.error == ""


def test_processing_stats_defaults():
    stats = ProcessingStats()

    assert stats.total_files == 0
    assert stats.processed_files == 0
    assert stats.failed_files == 0
    assert stats.categories_count == {}
