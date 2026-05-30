from dataclasses import dataclass
from pathlib import Path
from models import EmailMessage
from config import DEFAULT_ENCODING, SUPPORTED_EXTENSIONS
class EmailParser:
    def parse(self, filePath):
        cur_source_path = Path(filePath)
        if not cur_source_path.exists():
            raise FileNotFoundError(f"File does not exist: {cur_source_path}")
        if cur_source_path.suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {cur_source_path.suffix}")
        if cur_source_path.stat().st_size == 0:
            raise ValueError(f"Email file is empty: {cur_source_path}")
        cur_name = cur_source_path.name 
        cur_sender =  "unknown_sender"
        cur_subject = ""
        cur_raw_content = cur_source_path.read_text(encoding="utf-8")
        cur_body = cur_raw_content
        lines = cur_raw_content.splitlines()
        from_who_variants = ["From:", "От кого:", "ot kogo:", "от кого:"]
        subject_variants = ["Тема:", "tema:", "Subject:"]
        other_variants = ["To:", "Кому:", "Komu:", "Date:", "Дата:", "Data:"]
        for line in  lines:
            if any(line.startswith(x) for x in from_who_variants):
                cur_sender = line[line.index(':') + 1:].strip()
                cur_body = cur_body.replace(line, "", 1).strip()
            if any(line.startswith(x) for x in subject_variants):
                cur_subject = line[line.index(':') + 1:].strip()
                cur_body = cur_body.replace(line, "", 1).strip()
            if any(line.startswith(x) for x in other_variants):
                cur_body = cur_body.replace(line, "", 1).strip()
        cur_body = " ".join(cur_body.split())   
        return EmailMessage(filename=cur_name,source_path=str(cur_source_path),\
                            subject=cur_subject,sender=cur_sender,\
                                body=cur_body,raw_content=cur_raw_content)

