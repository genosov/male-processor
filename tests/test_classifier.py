import pytest

from src.mail_processor.classifier import EmailClassifier
from src.mail_processor.models import EmailMessage


@pytest.mark.parametrize(
    "subject, body, expected_category, expected_matched_rules",
    [
        ("Urgent problem", "Server down", "critical", ["critical_keywords"]),
        ("Discount", "Buy now", "spam", ["spam_keywords"]),
        ("Help", "Can't login", "support", ["support_keywords"]),
        ("Party", "My birthday tonight", "unknown", []),
        ("", "", "unknown", []),
        ("Invoice", "Client payment", "business", ["business_keywords"]),
        ("Newsletter", "Product update", "info", ["info_keywords"]),
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
    "subject, body, expected_category",
    [
        ("Urgent discount", "Server down, buy now", "critical"),
        ("Critical help", "Can't login", "critical"),
        ("Discount help", "Can't login, buy now", "spam"),
    ],
)
def test_classifier_resolves_category_priority(subject, body, expected_category):
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject=subject,
        body=body,
    )
    classifier = EmailClassifier()
    result = classifier.classify(email)
    assert result.category == expected_category
