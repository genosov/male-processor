import pytest

from src.mail_processor.classifier import EmailClassifier
from src.mail_processor.models import EmailMessage, ClassificationResult


def classify_email(subject: str, body: str) -> ClassificationResult:
    email = EmailMessage(
        filename="test.txt",
        source_path="test.txt",
        subject=subject,
        body=body,
    )
    classifier = EmailClassifier()
    return classifier.classify(email)


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
        (
            "URGENT INCIDENT",
            "SERVER DOWN",
            "critical",
            ["critical: urgent", "critical: server down"],
        ),
        (
            "   Discount   ",
            "   Buy now   ",
            "spam",
            ["spam: discount", "spam: buy now"],
        ),
        (
            "Критический инцидент",
            "Работа остановлена, ошибка 500",
            "critical",
            [
                "critical: критический инцидент",
                "critical: ошибка 500",
                "critical: работа остановлена",
                "support: ошибка",
            ],
        ),
        (
            "Запрос доступа к VPN",
            "У сотрудника пропал доступ",
            "support",
            ["support: запрос доступа", "support: пропал доступ"],
        ),
        (
            "Счёт на оплату",
            "Оплата по договору, прикладываем акт",
            "business",
            ["business: счёт", "business: акт", "business: оплата", "business: договору"],
        ),
        (
            "Корпоративный дайджест",
            "Напоминаем про плановые технические работы",
            "info",
            [
                "info: корпоративный дайджест",
                "info: дайджест",
                "info: напоминаем",
                "info: плановые технические работы",
            ],
        ),
        (
            "Вы выиграли iPhone",
            "Подтвердите личность и перейдите по ссылке",
            "spam",
            [
                "spam: выиграли",
                "spam: подтвердите личность",
                "spam: перейдите по ссылке",
            ],
        ),
        (
            "Актуальная инструкция",
            "Клиент просит прислать актуальную версию инструкции",
            "business",
            ["business: клиент"],
        ),
        (
            "Вопрос от клиента по заявке",
            "Внешний партнёр сообщает об ошибке при подключении к API",
            "support",
            [
                "support: ошибке",
                "support: заявке",
                "support: ошибке при подключении",
                "business: клиента",
                "business: партнёр",
                "business: внешний партнёр",
            ],
        ),
        (
            "Неисправность оборудования: сканер",
            "Нужна помощь, устройство не определяется системой",
            "support",
            [
                "support: неисправность",
                "support: оборудования",
                "support: не определяется системой",
                "support: нужна помощь",
            ],
        ),
        (
            "Корпоративный дайджест",
            "В этом выпуске: итоги квартала и новые сотрудники",
            "info",
            [
                "info: корпоративный дайджест",
                "info: дайджест",
                "info: итоги квартала",
                "info: новые сотрудники",
            ],
        ),
        (
            "Срочно подтвердите личность",
            "Ваш пароль истекает, ответив на это письмо укажите логин и пароль",
            "spam",
            [
                "spam: подтвердите личность",
                "spam: логин и пароль",
                "spam: срочно подтвердите",
                "spam: пароль истекает",
                "spam: ответив на это письмо",
            ],
        ),
    ],
)
def test_classifier_detects_email_category_and_rules(subject, body, expected_category, expected_matched_rules):
    result = classify_email(subject, body)
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
            "support",
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
    result = classify_email(subject, body)
    assert result.category == expected_category
    assert result.matched_rules == expected_matched_rules


@pytest.mark.parametrize(
    "subject, body, expected_category, expected_matched_rules",
    [
        (
            "Buy now",
            "Client payment invoice",
            "business",
            [
                "spam: buy now",
                "business: invoice",
                "business: client",
                "business: payment",
            ],
        ),
    ],
)
def test_classifier_prefers_higher_score_when_not_critical(subject, body, expected_category, expected_matched_rules):
    result = classify_email(subject, body)
    assert result.category == expected_category
    assert result.matched_rules == expected_matched_rules


@pytest.mark.parametrize(
    "subject, body, expected_category, expected_matched_rules",
    [
        (
            "Urgent invoice",
            "Client payment meeting",
            "critical",
            [
                "critical: urgent",
                "business: invoice",
                "business: meeting",
                "business: client",
                "business: payment",
            ],
        ),
    ],
)
def test_classifier_prioritizes_critical_over_score(subject, body, expected_category, expected_matched_rules):
    result = classify_email(subject, body)
    assert result.category == expected_category
    assert result.matched_rules == expected_matched_rules
