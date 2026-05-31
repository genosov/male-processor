from pathlib import Path

from src.mail_processor.models import ClassificationResult, EmailMessage, ProcessingStats
from src.mail_processor.pipeline import ProcessingPipeline


class FakeFileHandler:
    def __init__(self, files=None, move_result=None):
        self.files = files or []
        self.move_result = move_result
        self.moved_files = []

    def scan_inbox(self):
        return self.files

    def move_file_to_category(self, file_path, category):
        self.moved_files.append((file_path, category))
        if self.move_result is not None:
            return self.move_result
        return Path("/processed") / category / Path(file_path).name


class FakeParser:
    def __init__(self, email=None, error=None):
        self.email = email or EmailMessage(
            filename="mail.txt",
            source_path="/inbox/mail.txt",
            subject="Help",
            body="Can't login",
        )
        self.error = error
        self.parsed_files = []

    def parse(self, file_path):
        self.parsed_files.append(file_path)
        if self.error is not None:
            raise self.error
        return self.email


class FakeClassifier:
    def __init__(self, category):
        self.category = category
        self.classified_emails = []

    def classify(self, email):
        self.classified_emails.append(email)
        return ClassificationResult(
            category=self.category,
            matched_rules=[f"{self.category}: test"],
        )


def make_pipeline(file_handler=None, parser=None, classifier=None):
    pipeline = ProcessingPipeline.__new__(ProcessingPipeline)
    pipeline.file_handler = file_handler or FakeFileHandler()
    pipeline.parser = parser or FakeParser()
    pipeline.classifier = classifier or FakeClassifier("support")
    pipeline.stats = ProcessingStats()
    return pipeline


def test_update_stats_counts_successful_file():
    pipeline = make_pipeline()

    pipeline._update_stats("support", success=True)

    assert pipeline.stats.processed_files == 1
    assert pipeline.stats.failed_files == 0
    assert pipeline.stats.categories_count == {"support": 1}


def test_update_stats_counts_failed_file():
    pipeline = make_pipeline()

    pipeline._update_stats("corrupted", success=False)

    assert pipeline.stats.processed_files == 0
    assert pipeline.stats.failed_files == 1
    assert pipeline.stats.categories_count == {"corrupted": 1}


def test_process_file_moves_successfully_classified_email():
    file_path = Path("/inbox/mail.txt")
    file_handler = FakeFileHandler()
    parser = FakeParser()
    classifier = FakeClassifier("support")
    pipeline = make_pipeline(file_handler, parser, classifier)

    pipeline.process_file(file_path)

    assert parser.parsed_files == [file_path]
    assert classifier.classified_emails == [parser.email]
    assert file_handler.moved_files == [(file_path, "support")]
    assert pipeline.stats.processed_files == 1
    assert pipeline.stats.failed_files == 0
    assert pipeline.stats.categories_count == {"support": 1}


def test_process_file_replaces_invalid_category_with_unknown():
    file_path = Path("/inbox/mail.txt")
    file_handler = FakeFileHandler()
    pipeline = make_pipeline(
        file_handler=file_handler,
        parser=FakeParser(),
        classifier=FakeClassifier("unexpected"),
    )

    pipeline.process_file(file_path)

    assert file_handler.moved_files == [(file_path, "unknown")]
    assert pipeline.stats.categories_count == {"unknown": 1}


def test_process_file_counts_failure_when_move_returns_none():
    file_path = Path("/inbox/mail.txt")
    file_handler = FakeFileHandler(move_result=None)
    file_handler.move_file_to_category = lambda path, category: None
    pipeline = make_pipeline(file_handler=file_handler)

    pipeline.process_file(file_path)

    assert pipeline.stats.processed_files == 0
    assert pipeline.stats.failed_files == 1
    assert pipeline.stats.categories_count == {"support": 1}


def test_process_file_moves_corrupted_when_parser_fails():
    file_path = Path("/inbox/broken.txt")
    file_handler = FakeFileHandler()
    parser = FakeParser(error=ValueError("broken email"))
    pipeline = make_pipeline(file_handler=file_handler, parser=parser)

    pipeline.process_file(file_path)

    assert file_handler.moved_files == [(file_path, "corrupted")]
    assert pipeline.stats.processed_files == 0
    assert pipeline.stats.failed_files == 1
    assert pipeline.stats.categories_count == {"corrupted": 1}


def test_run_sets_total_files_and_processes_all_files():
    files = [Path("/inbox/first.txt"), Path("/inbox/second.txt")]
    pipeline = make_pipeline(file_handler=FakeFileHandler(files=files))

    stats = pipeline.run()

    assert stats.total_files == 2
    assert stats.processed_files == 2
    assert stats.failed_files == 0
    assert stats.categories_count == {"support": 2}
