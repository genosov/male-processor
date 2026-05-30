from .models import EmailMessage, ClassificationResult


class EmailClassifier:
    def __init__(self):
        self.rules = {
            "critical": ["urgent", "critical", "server down"],
            "spam": ["discount", "winner", "buy now"],
            "support": ["help", "support", "problem", "issue", "can't login"],
            "business": ["contract", "invoice", "meeting", "client", "payment"],
            "info": [
                "notification",
                "newsletter",
                "report",
                "update",
                "announcement",
                "reminder",
                ],
        }

    def classify(self, email: EmailMessage) -> ClassificationResult:
        text = self._build_text(email)
        for category, keywords in self.rules.items():
            if any(keyword in text for keyword in keywords):
                return ClassificationResult(category, [f"{category}_keywords"])
        return ClassificationResult("unknown", [])

    def _build_text(self, email: EmailMessage) -> str:
        text = (email.subject + " " + email.body).lower().strip()
        return text

