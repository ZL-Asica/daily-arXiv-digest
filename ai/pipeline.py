import json
import logging
from pathlib import Path
from typing import Dict, List

from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI
from tqdm.auto import tqdm

from .config import settings
from .prompts import get_prompt_chain
from .structure import PaperSummary

logger = logging.getLogger(__name__)


class PaperRefresher:
    def __init__(self):
        self.llm = ChatOpenAI(model=settings.model_name).with_structured_output(
            PaperSummary, method="function_calling"
        )
        self.chain = get_prompt_chain(
            system_template_path=Path(__file__).parent / "system.txt",
            human_template_path=Path(__file__).parent / "template.txt",
            llm=self.llm,
        )

    def load_data(self) -> List[Dict]:
        raw = []
        with settings.input_path.open() as f:
            for line in f:
                raw.append(json.loads(line))
        # dedupe by id
        seen = set()
        unique = []
        for item in raw:
            if (pid := item.get("id")) and pid not in seen:
                seen.add(pid)
                unique.append(item)
        logger.info(f"Loaded {len(unique)} unique records from {settings.input_path}")
        return unique

    def save_result(self, records: List[Dict]):
        with settings.output_path.open("w") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        logger.info(f"Saved {len(records)} enhanced records to {settings.output_path}")

    def run(self):
        data = self.load_data()
        assert len(data) > 0, "No data to process."
        enhanced = []
        for entry in tqdm(data, desc="Processing papers"):
            paper_id = entry.get("id", "<unknown>")
            try:
                summary: PaperSummary = self.chain.invoke(
                    {"content": entry.get("summary", "")}
                )
                entry["AI"] = summary.model_dump()
            except OutputParserException as err:
                logger.error(f"Parsing failed for {paper_id}: {err}")
                entry["AI"] = {field: "Error" for field in PaperSummary.model_fields}
            enhanced.append(entry)
        self.save_result(enhanced)
