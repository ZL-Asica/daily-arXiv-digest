from typing import List

from pydantic import BaseModel, Field


class PaperSummary(BaseModel):
    tldr: str = Field(..., description="Too long; didn't read summary")
    motivation: str = Field(..., description="Describe the motivation of the paper")
    method: str = Field(..., description="Methodology of the paper")
    result: str = Field(..., description="Key results of the paper")
    conclusion: str = Field(..., description="Conclusion of the paper")
    key_contributions: List[str] = Field(..., description="Top 2–3 novel contributions")
    limitations: str = Field(..., description="Known limitations or caveats")
    keywords: List[str] = Field(
        ..., description="3–5 author-provided or extracted keywords"
    )
    importance_score: int = Field(
        ...,
        ge=0,
        le=10,
        description="Relevance level (0=none, 10=must-read) based on the user's background",
    )
    read_time_minutes: int = Field(
        ..., description="Estimated time to read (in minutes)"
    )
