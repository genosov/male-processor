import pytest

from src.mail_processor.classifier import EmailClassifier
from src.mail_processor.models import EmailMessage


@pytest.mark.parametrize(
    "subject, body, expected_category, expected_matched_rules",
    [
        (
            "Urgent incident",
            "Server down",
            "critical",
            ["critical: urgent", "critical: server down"],
        ),
        ("Discount", "Buy now", "spam", ["spam: discount", "spam: buy now"]),
        ("Help", "Can't login", "support", ["support: help", "support: can't login"]),
        ("Party", "My birthday tonight", "unknown", []),
        ("", "", "unknown", []),
        (
            "Invoice",
            "Client payment",
            "business",
            ["business: invoice", "business: client", "business: payment"],
        ),
        ("Newsletter", "Product update", "info", ["info: newsletter", "info: update"]),
    ],
)
def test_classifier_detects_email_category_and_rules(subject, body, expected_category, expected_matched_rules):
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject=subject,
        body=body,
    )
    classifier = EmailClassifier()
    result = classifier.classify(email)
    assert result.category == expected_category
    assert result.matched_rules == expected_matched_rules


@pytest.mark.parametrize(
    "subject, body, expected_category, expected_matched_rules",
    [
        (
            "Urgent discount",
            "Server down, buy now",
            "critical",
            [
                "critical: urgent",
                "critical: server down",
                "spam: discount",
                "spam: buy now",
            ],
        ),
        (
            "Critical help",
            "Can't login",
            "critical",
            [
                "critical: critical",
                "support: help",
                "support: can't login",
            ],
        ),
        (
            "Discount help",
            "Can't login, buy now",
            "spam",
            [
                "spam: discount",
                "spam: buy now",
                "support: help",
                "support: can't login",
            ],
        ),
    ],
)
def test_classifier_resolves_category_priority(subject, body, expected_category, expected_matched_rules):
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject=subject,
        body=body,
    )
    classifier = EmailClassifier()
    result = classifier.classify(email)
    assert result.category == expected_category
    assert result.matched_rules == expected_matched_rules
