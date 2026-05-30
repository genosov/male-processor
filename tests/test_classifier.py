import pytest

from src.mail_processor.classifier import EmailClassifier
from src.mail_processor.models import EmailMessage


@pytest.mark.parametrize(
    "subject, body, expected_category",
    [
        ("Urgent problem", "Server down", "critical"),
        ("Discount", "Buy now", "spam"),
        ("Help", "Can't login", "support"),
        ("Party", "My birthday tonight", "unknown"),
    ],
)
def test_classifier_detects_email_category(subject, body, expected_category):
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject=subject,
        body=body,
    )
    classifier = EmailClassifier()
    result = classifier.classify(email)
    assert result.category == expected_category
