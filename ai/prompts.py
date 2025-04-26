import os

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

__all__ = ["get_prompt_chain"]


# Base system instruction embedding user background and output schema
_BASE_SYSTEM = f"""
You are a rigorous AI research assistant specializing in arXiv content. Your task is twofold:

1. Convert an arXiv paper’s title, abstract (and full text, if provided) into a structured JSON summary matching the given schema.
2. Assign a relevance score from 0 to 10 based **strictly** on the user’s background and interests.

Relevance Scoring Guidelines:
  • 0––1: Irrelevant to the user’s domain.
  • 2––3: Marginal relevance; unlikely to be useful.
  • 4––6: Moderately relevant; worth glancing at after higher-priority papers.
  • 7––8: Highly relevant; important to read when time allows.
  • 9––10: Core papers the user must read immediately.
Use the full range—avoid clustering scores at 8–10. Only papers closely aligned with the user’s stated research warrant a 9 or 10.

**Important**  
• Respond **strictly** with valid JSON that matches the schema—no extra fields or commentary.  
• If any field is unavailable, use an empty string or 0.  
• Do **not** add prose, explanations, or examples outside the JSON.

User Background:
{os.getenv("USER_BACKGROUND", "<no background provided>")[:500]}
"""

# Template without PDF
_HUMAN_NO_PDF = """
Abstract:
{abstract}

Please provide a concise summary with given schema.
"""

# Template with PDF
_HUMAN_WITH_PDF = """
Abstract:
{abstract}

Full Text:
{pdf_content}

Please provide a concise summary with given schema.
"""


def get_prompt_chain(llm, include_pdf: bool = False) -> ChatPromptTemplate:
    # System message with background and schema instructions
    system = SystemMessagePromptTemplate.from_template(_BASE_SYSTEM)

    # Choose human prompt based on whether PDF is included
    if include_pdf:
        human = HumanMessagePromptTemplate.from_template(
            template=_HUMAN_WITH_PDF,
            input_variables=["abstract", "pdf_content"],
        )
    else:
        human = HumanMessagePromptTemplate.from_template(
            template=_HUMAN_NO_PDF,
            input_variables=["abstract"],
        )

    prompt = ChatPromptTemplate.from_messages([system, human])
    return prompt | llm
