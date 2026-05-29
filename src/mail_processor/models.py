from dataclasses import dataclass, field


@dataclass
class EmailMessage:
    filename: str
    source_path: str = ""

    subject: str = ""
    sender: str = "unknown_sender"
    recipients: list[str] = field(default_factory=list)

    body: str = ""
    raw_content: str = ""

    detected_format: str = "unknown"
    metadata: dict[str, str] = field(default_factory=dict)