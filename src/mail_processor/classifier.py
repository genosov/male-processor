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
        self.priority = ["critical", "spam", "support", "business", "info"]

    def classify(self, email: EmailMessage) -> ClassificationResult:
        text = self._build_text(email)
        matched_rules = []
        matched_categories = set()
        selected_category = "unknown"

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in text:
                    matched_rules.append(f"{category}: {keyword}")
                    matched_categories.add(category)

        for category in self.priority:
            if category in matched_categories:
                selected_category = category
                break

        return ClassificationResult(selected_category, matched_rules)

    def _build_text(self, email: EmailMessage) -> str:
        text = (email.subject + " " + email.body).lower().strip()
        return text
