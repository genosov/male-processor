import logging

from extensions.analytics_report.report_generator import generate_excel_report

from .logging_config import setup_logging
from .pipeline import ProcessingPipeline


logger = logging.getLogger(__name__)


def print_stats(stats) -> None:
    print(f"Total files: {stats.total_files}")
    print(f"Processed files: {stats.processed_files}")
    print(f"Failed files: {stats.failed_files}")

    if stats.categories_count:
        print("Categories:")
        for category, count in stats.categories_count.items():
            print(f"  {category}: {count}")


def main() -> int:
    try:
        setup_logging()
        logger.info("Application started")

        pipeline = ProcessingPipeline()
        stats = pipeline.run()

        print_stats(stats)

        try:
            report_path = generate_excel_report(stats)
            print(f"Excel report created: {report_path}")
        except Exception:
            logger.exception("Failed to generate Excel report")

        logger.info("Application finished successfully")
        return 0
    except Exception:
        logger.exception("Application finished with error")
        print("Processing failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
