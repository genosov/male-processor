from src.mail_processor.classifier import EmailClassifier
from src.mail_processor.models import EmailMessage


def test_classifier_detects_critical_email():
    classifier = EmailClassifier()
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject="Urgent problem",
        body="Server down",
    )
    result = classifier.classify(email)
    assert result.category == "critical"


def test_classifier_detects_spam_email():
    classifier = EmailClassifier()
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject="Discount",
        body="Buy now",
    )
    result = classifier.classify(email)
    assert result.category == "spam"


def test_classifier_detects_support_email():
    classifier = EmailClassifier()
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject="Help",
        body="Can't login",
    )
    result = classifier.classify(email)
    assert result.category == "support"


def test_classifier_detects_unknown_email():
    classifier = EmailClassifier()
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject="Party",
        body="My birthday tonight",
    )
    result = classifier.classify(email)
    assert result.category == "unknown"
