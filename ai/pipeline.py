import json
import logging
from typing import Dict, List

import pymupdf4llm
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI
from tqdm.auto import tqdm

from .config import settings
from .prompts import get_prompt_chain
from .structure import PaperSummary

logger = logging.getLogger(__name__)


class PaperRefresher:
    def __init__(self) -> None:
        # load seen IDs
        self.seen: set[str] = set()
        if settings.seen_file.exists():
            self.seen = set(
                line.strip()
                for line in settings.seen_file.read_text().splitlines()
                if line.strip()
            )

        # build LLM
        self.llm = ChatOpenAI(model=settings.model_name).with_structured_output(
            PaperSummary, method="function_calling"
        )
        self.chain = get_prompt_chain(self.llm)

    def load_data(self) -> List[Dict]:
        raw = []
        with settings.input_path.open() as f:
            for line in f:
                raw.append(json.loads(line))

        unique = []
        targets = [c.strip() for c in settings.categories.split(",")]
        for item in raw:
            pid = item.get("id")
            if not pid or pid in self.seen:
                continue
            if item.get("categories", [None])[0] not in targets:
                continue
            unique.append(item)

        logger.info(f"Loaded {len(unique)} new records (excluding seen).")
        return unique

    def save_seen(self, pid: str):
        # append to seen file
        with settings.seen_file.open("a") as f:
            f.write(pid + "\n")

    def run(self) -> None:
        entries = self.load_data()
        if len(entries) == 0:
            logger.info("No new records to process.")
            return

        enhanced = []
        for entry in tqdm(entries, desc="Processing papers"):
            pid = entry["id"]
            # prepare inputs
            abstract = entry.get("summary", "")
            comment = entry.get("comment") or ""
            content = abstract + (f"\n\narXiv Comment: {comment}" if comment else "")

            # optionally load PDF text
            pdf_text = ""
            if settings.pdf_folder:
                pdf_path = settings.pdf_folder / f"{pid}.pdf"
                if pdf_path.exists():
                    pdf_text = pymupdf4llm.to_markdown(str(pdf_path))

            # invoke LLM
            try:
                summary: PaperSummary = self.chain.invoke(
                    {
                        "abstract": content,
                        "pdf_content": pdf_text,
                    }
                )
                entry["AI"] = summary.model_dump()
            except OutputParserException as err:
                logger.error(f"Parsing failed for {pid}: {err}")
                entry["AI"] = {f: "Error" for f in PaperSummary.model_fields}

            enhanced.append(entry)
            # mark seen
            self.save_seen(pid)

        # write output
        with settings.output_path.open("w") as f:
            for rec in enhanced:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Remove pdf folder if it exists
        if settings.pdf_folder and settings.pdf_folder.exists():
            for pdf in settings.pdf_folder.glob("*.pdf"):
                pdf.unlink()
            settings.pdf_folder.rmdir()

        logger.info(
            f"Saved {len(enhanced)} enhanced records to {settings.output_path}."
        )
