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
    