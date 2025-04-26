import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    """Application settings from environment, CLI args override."""

    def __init__(self) -> None:
        if Path(".env").exists():
            load_dotenv()
        self.model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.categories: str = os.getenv("CATEGORIES", "cs.HC,cs.CL")
        self.input_path: Path = Path(os.getenv("INPUT_FILE", "data.jsonl"))
        self.output_path: Path = Path(os.getenv("OUTPUT_FILE", "data_enhanced.jsonl"))
        # set via CLI -p/--pdf_folder
        self.pdf_folder: Path | None = None
        # Set a env variable SEEN_FILE to a file path to store seen IDs
        self.seen_file: Path = Path(os.getenv("SEEN_FILE", "contents/seen_ids.txt"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
