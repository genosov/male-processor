import re

from .models import EmailMessage, ClassificationResult


class EmailClassifier:
    def __init__(self):
        self.rules = {
            "critical": [
                "urgent",
                "critical",
                "server down",
                "критичный инцидент",
                "критический инцидент",
                "ошибка 500",
                "работа остановлена",
                "массовый сбой",
                "падает",
                "срочная помощь",
                "просим срочно проверить",
            ],
            "spam": [
                "discount",
                "winner",
                "buy now",
                "выиграли",
                "подтвердите личность",
                "верификация аккаунта",
                "логин и пароль",
                "перейдите по ссылке",
                "аккаунт будет заблокирован",
                "немедленно подтвердите",
                "secure-login",
                "exclusive offer",
            ],
            "support": [
                "help",
                "support",
                "problem",
                "issue",
                "can't login",
                "ошибка",
                "не открывает",
                "не отвечает",
                "не могу войти",
                "нет доступа",
                "недоступен",
                "запрос доступа",
                "выдать доступ",
                "пропал доступ",
                "доступ запрещён",
                "не запускается",
                "перестал запускаться",
                "зависает",
                "неисправность",
                "сломался",
                "установка",
                "переустановка",
                "нужна помощь",
                "тикет",
            ],
            "business": [
                "contract",
                "invoice",
                "meeting",
                "client",
                "payment",
                "счёт",
                "счет",
                "акт",
                "акт выполненных работ",
                "оплата",
                "договор",
                "договору",
                "закрывающие документы",
                "бухгалтерию",
                "реквизиты",
                "техническое задание",
                "согласование",
            ],
            "info": [
                "notification",
                "newsletter",
                "report",
                "update",
                "announcement",
                "reminder",
                "корпоративный дайджест",
                "дайджест",
                "уведомление",
                "отчёт",
                "отчет",
                "обновления корпоративного портала",
                "напоминаем",
                "плановые технические работы",
                "мониторинг",
            ],
        }
        self.priority = ["critical", "support", "spam", "business", "info"]

    def classify(self, email: EmailMessage) -> ClassificationResult:
        text = self._build_text(email)
        matched_rules = []
        category_scores = {category: 0 for category in self.rules}
        selected_category = "unknown"

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if self._keyword_matches(text, keyword):
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

    def _keyword_matches(self, text: str, keyword: str) -> bool:
        pattern = rf"(?<!\w){re.escape(keyword.lower())}(?!\w)"
        return re.search(pattern, text) is not None
