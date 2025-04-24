from pydantic import BaseModel, Field


class PaperSummary(BaseModel):
    tldr: str = Field(..., description="Too long; didn't read summary")
    motivation: str = Field(..., description="Describe the motivation of the paper")
    method: str = Field(..., description="Methodology of the paper")
    result: str = Field(..., description="Key results of the paper")
    conclusion: str = Field(..., description="Conclusion of the paper")
