"""
Formatting and conversion tools.
Contains tools for converting JSON to Markdown and other formatting operations.
"""

import ast
import json
from typing import Any, Dict, List, Union

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .utilities import strip_fences_and_labels

try:
    from langchain_core.tools import tool  # modern
except Exception:
    from langchain.tools import tool  # fallback

# Initialize LLM
llm = AzureChatOpenAI(deployment_name="gpt-4o")


# ---------- Input Schemas ----------
class JSONToMarkdownLLMInput(BaseModel):
    data: Union[Dict[str, Any], List[Any], str] = Field(
        ...,
        description="JSON object/list or JSON string to convert to Markdown using LLM",
    )
    title: str | None = Field(
        default=None, description="Optional top-level title for the Markdown output"
    )
    style_hint: str | None = Field(
        default=None,
        description="Optional style guidance (e.g., 'Complete Application Strategy format').",
    )


# ---------- Tools ----------
@tool("json_to_markdown_llm", args_schema=JSONToMarkdownLLMInput, return_direct=False)
def json_to_markdown_llm(data: Union[Dict[str, Any], List[Any], str]) -> str:
    """Convert JSON to Markdown using the LLM. Returns pure Markdown (no code fences)."""
    try:
        py = (
            data
            if isinstance(data, (dict, list))
            else json.loads(strip_fences_and_labels(str(data)))
        )
    except Exception:
        try:
            py = ast.literal_eval(str(data))
        except Exception as e:
            return f"Error: {e}"

    json_str = json.dumps(py, ensure_ascii=False, indent=2)

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
            ("human", "JSON:\n{json}"),
        ]
    )

    chain: Runnable = prompt | llm | StrOutputParser()

    raw = chain.invoke({"json": json_str})

    md = strip_fences_and_labels(raw)

    return md.strip()
