from pathlib import Path

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

__all__ = ["get_prompt_chain"]


def get_prompt_chain(system_template_path: Path, human_template_path: Path, llm):
    system_text = system_template_path.read_text()
    human_text = human_template_path.read_text()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_text),
            HumanMessagePromptTemplate.from_template(template=human_text),
        ]
    )

    return prompt | llm
