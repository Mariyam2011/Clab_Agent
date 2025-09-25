from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import AzureChatOpenAI


llm = AzureChatOpenAI(deployment_name="gpt-4o")


class JSONToMarkdownLLMInput(BaseModel):
    data: str = Field(..., description="JSON object/list or JSON string to convert to Markdown using LLM")


@tool("json_to_markdown_llm", args_schema=JSONToMarkdownLLMInput, return_direct=False)
def json_to_markdown_llm(data: str) -> str:
    """Convert JSON data to clean, readable Markdown format using LLM processing."""

    system_instructions = (
        "You are a formatter that converts JSON into clean, readable Markdown. "
        "Output ONLY Markdown content without code fences. "
        "Never include triple backticks. Avoid tables unless specifically asked. "
        "Prefer headings, bullet points, and numbered lists. "
        "Convert the JSON structure faithfully without adding creative content or changing the meaning. "
        "Only format the existing data into Markdown structure."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_instructions),
            ("human", "DATA:\n{data}"),
        ]
    )

    chain: Runnable = prompt | llm | StrOutputParser()

    raw = chain.invoke({"data": data})

    return raw.strip()
