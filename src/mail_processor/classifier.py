from .models import EmailMessage, ClassificationResult


class EmailClassifier:
    def classify(self, email: EmailMessage) -> ClassificationResult:
        text = self._build_text(email)
        critical_keywords = ["urgent", "critical", "server down"]
        if any(keyword in text for keyword in critical_keywords):
            return ClassificationResult("critical", ["critical_keywords"])
        return ClassificationResult("unknown", [])

    def _build_text(self, email: EmailMessage) -> str:
        text = (email.subject + " " + email.body).lower()
        return text
