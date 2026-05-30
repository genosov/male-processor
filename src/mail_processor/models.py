from dataclasses import dataclass, field


CATEGORIES = [
    "critical",
    "support",
    "business",
    "info",
    "spam",
    "unknown",
    "corrupted",
]


@dataclass
class EmailMessage:
    filename: str
    source_path: str
    subject: str = ""
    sender: str = "unknown_sender"
    body: str = ""
    raw_content: str = ""


@dataclass
class ClassificationResult:
    category: str
    matched_rules: list[str] = field(default_factory=list)


@dataclass
class ProcessingResult:
    filename: str
    source_path: str
    destination_path: str
    category: str
    success: bool = True
    error: str = ""


@dataclass
class ProcessingStats:
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    categories_count: dict[str, int] = field(default_factory=dict)