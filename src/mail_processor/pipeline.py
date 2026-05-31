import logging

from .models import CATEGORIES
from .classifier import EmailClassifier
from .file_handler import FileHandler
from .models import ProcessingStats
from .parser import EmailParser


logger = logging.getLogger(__name__)


class ProcessingPipeline:
    def __init__(self) -> None:
        self.file_handler = FileHandler()
        self.parser = EmailParser()
        self.classifier = EmailClassifier()
        self.stats = ProcessingStats()


    def _update_stats(self, category: str, success: bool) -> None:
        if success:
            self.stats.processed_files += 1
        else:
            self.stats.failed_files += 1

        if category not in self.stats.categories_count:
            self.stats.categories_count[category] = 0
        self.stats.categories_count[category] += 1

        def _is_supported_file(self, file_path) -> bool:
            file_format = self.file_handler.classify_file(file_path)
            return file_format != "unknown"


    def run(self) -> ProcessingStats:
        logger.info("Pipeline started")

        files = self.file_handler.scan_inbox()
        self.stats.total_files = len(files)
        logger.info("Found %s files in inbox", self.stats.total_files)

        for file_path in files:
            try:
                self.process_file(file_path)
            except Exception as error:
                logger.exception("Unexpected error while processing file %s", file_path)
                self._update_stats("corrupted", success=False)

        logger.info(
            "Pipeline finished: total=%s, processed=%s, failed=%s",
            self.stats.total_files,
            self.stats.processed_files,
            self.stats.failed_files,
        )

        return self.stats

    def process_file(self, file_path) -> None:
        logger.info("Processing file: %s", file_path)

        try:
            if not self._is_supported_file(file_path):
                logger.warning("Unsupported file format: %s", file_path)

                destination_path = self.file_handler.move_file_to_category(
                    file_path,
                    "unknown",
                )

                if destination_path is None:
                    logger.error("Failed to move unsupported file: %s", file_path)
                    self._update_stats("unknown", success=False)
                    return

                self._update_stats("unknown", success=True)
                return

            email = self.parser.parse(file_path)
            classification = self.classifier.classify(email)
            category = classification.category

            if category not in CATEGORIES:
                logger.warning(
                    "Unknown category '%s' for file %s",
                    category,
                    file_path,
                )
                category = "unknown"

            destination_path = self.file_handler.move_file_to_category(
                file_path,
                category,
            )

            if destination_path is None:
                logger.error(
                    "Failed to move file %s to category %s",
                    file_path,
                    category,
                )
                self._update_stats(category, success=False)
                return

            self._update_stats(category, success=True)  
            logger.info(
                "File processed successfully: %s -> %s",
                file_path,
                category,
            )

        except Exception as error:
            logger.exception("Failed to process file %s", file_path)

            destination_path = self.file_handler.move_file_to_category(
                file_path,
                "corrupted",
            )
            if destination_path is None:
                logger.error("Failed to move corrupted file: %s", file_path)

            self._update_stats("corrupted", success=False)