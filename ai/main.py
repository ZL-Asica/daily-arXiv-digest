import argparse
import logging
from pathlib import Path

from .config import settings
from .pipeline import PaperRefresher


def parse_args():
    parser = argparse.ArgumentParser(
        description="Enhance paper abstracts with AI-generated summaries."
    )
    parser.add_argument(
        "-i", "--input_file", required=True, help="Path to input JSONL file"
    )
    parser.add_argument(
        "-o", "--output_file", required=True, help="Path to output JSONL file"
    )
    parser.add_argument(
        "-p", "--pdf_folder", help="Folder containing downloaded PDFs to include"
    )
    return parser.parse_args()


def main():
    """Enhance paper abstracts with AI-generated summaries."""
    args = parse_args()
    assert args.input_file and args.output_file, (
        "Both input and output files must be provided."
    )

    settings.input_path = Path(args.input_file)
    settings.output_path = Path(args.output_file)
    settings.pdf_folder = Path(args.pdf_folder) if args.pdf_folder else None

    if settings.pdf_folder is not None:
        print(f"PDF folder set to: {settings.pdf_folder}")

    # configure logging
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting PaperRefresher...")

    refresher = PaperRefresher()
    refresher.run()
    logger.info("Completed all tasks.")


if __name__ == "__main__":
    main()
