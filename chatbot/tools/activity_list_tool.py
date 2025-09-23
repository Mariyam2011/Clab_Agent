"""
Activity list generation tool for college application strategy.
Generates enhanced activities and 3 new signature activities based on user context.
"""

import json
from typing import Any, Dict, Union

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tools import tool


llm = AzureChatOpenAI(deployment_name="gpt-4o")


def create_activity_list_generator_prompt_template() -> ChatPromptTemplate:
    prompt = """
    You are acting as a U.S. college admissions counselor. 
    Critically think: what kind of activity list would make this student stand out at the world’s most selective universities? 
    Activities should feel authentic, unique, and interview-defensible, while highlighting hidden impact and originality.

    USER CONTEXT: {user_context}

    TASK: Transform existing activities into standout accomplishments AND invent three new signature activities that are bold, unexpected, and deeply connected to the student’s mission.

    FORMAT REQUIREMENTS:
    - Position: [50 characters max]
    - Organization: [100 characters max]
    - Description: [150 characters max]

    CRITICAL AUTHENTICITY WARNING:
    - Enhance by revealing hidden impact, creative methods, and overlooked beneficiaries.
    - Do NOT inflate numbers or invent fictional elements. Every claim must be defensible in an interview.
    - Admissions officers can immediately detect exaggeration.

    FOR EACH ACTIVITY PROVIDE:
    1. **Enhanced Version of Existing:**
       - Current: [What they currently have]
       - Elevated: [Deeper framing, hidden impact, measurable results]
       - Position: [Action verb + unique role, ≤50 chars]
       - Organization: [Memorable org name, ≤100 chars]
       - Description: [What was done + specific numbers + unique method + who benefited, ≤150 chars]

    2. **Three New Signature Activities:**
       - Must target an overlooked community
       - Must use an unexpected method
       - Must create measurable change
       - Must include a memorable initiative name

    COUNSELOR'S EXPECTATION:
    - Every activity should demonstrate leadership, creativity, and impact.
    - Activities must progress logically (early involvement → initiative → leadership → scaling).
    - Each line should make an admissions officer pause and think: “Only this student could have done this.”

    OUTPUT: Return exactly one JSON object. Do not include any trailing commas. 
    Do not include explanations, comments, or text outside the JSON. 
    Every string value must be a single line. If you must break lines, use "\\n"
    Do not wrap your output in Markdown or code fences. Return only the JSON object.
    """

    return ChatPromptTemplate.from_template(prompt)


class ActivityListInput(BaseModel):
    user_context: str = Field(..., description="Complete user context")


@tool("generate_activity_list", args_schema=ActivityListInput, return_direct=False)
def generate_activity_list(user_context: str) -> str:
    prompt: ChatPromptTemplate = create_activity_list_generator_prompt_template()

    chain: Runnable = prompt | llm | StrOutputParser()

    return chain.invoke({"user_context": user_context})
