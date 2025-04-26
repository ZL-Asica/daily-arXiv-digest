import os

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

__all__ = ["get_prompt_chain"]


# Base system instruction embedding user background and output schema
_BASE_SYSTEM = f"""
You are an expert AI research assistant. Your mission is to transform an arXiv paper’s content into a structured summary following the given schema.

Respond with valid JSON strictly matching the schema. Do not include any additional commentary or fields. Use empty strings or 0 for missing values. Do not add any extra commentary or prose.

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
