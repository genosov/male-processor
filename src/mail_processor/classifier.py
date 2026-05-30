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
        category_scores = {"critical": 0, "spam": 0, "support": 0, "business": 0, "info": 0}
        selected_category = "unknown"

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in text:
                    matched_rules.append(f"{category}: {keyword}")
                    category_scores[category] = category_scores.get(category, 0) + 1

        if category_scores["critical"] > 0:
            selected_category = "critical"
        else:
            best_score = 0

            for category in self.priority:
                score = category_scores[category]
                if score > best_score:
                    best_score = score
                    selected_category = category

        return ClassificationResult(selected_category, matched_rules)

    def _build_text(self, email: EmailMessage) -> str:
        text = (email.subject + " " + email.body).lower().strip()
        return text
