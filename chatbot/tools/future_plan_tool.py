"""
Future plan generation tool for college application strategy.
Generates a single ≤100 character future plan line based on user context.
"""

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tools import tool


llm = AzureChatOpenAI(deployment_name="gpt-4o")


def create_future_plan_prompt_template() -> ChatPromptTemplate:
    prompt = """
    You are acting as a college admissions counselor crafting a future plan statement that will make an application stand out. 
    Think critically: What kind of response would *truly* impress an admissions officer? What feels unique, bold, and out-of-the-box, 
    yet still authentic to the student's profile and narrative?

    GOAL: Create ONE powerful 100-character future plan line that makes the student's mission unmistakable.

    FORMULA: [Role/Identity] + [Unique Approach] + [Specific Impact]

    EXCELLENT EXAMPLES (unexpected, specific, memorable):
    - Environmental scientist using tech to empower female farmers
    - Policy leader & artist, challenging gender bias through creative advocacy
    - Computational linguist using AI to decode scripts & empower women globally
    - Sustainability engineer, promoting green technology to combat urban pollution
    - To lead biotech innovations that empower underserved communities

    COUNSELOR'S EXPECTATION:
    - Not vague or cliché (“help people,” “make the world better”).
    - Must fuse different aspects of the student's identity/skills in a surprising way.
    - Should name a specific community or beneficiary (not just “the world”).
    - Must feel like something ONLY this student could say — rooted in their profile and narrative.

    RULES:
    1. Max 100 characters (including spaces).
    2. Use strong, active verbs (designing, reimagining, challenging, decoding).
    3. Must connect clearly to USER CONTEXT.
    4. Output ONLY the single future plan line — no commentary, no extra text.

    USER CONTEXT: {user_context}


    Generate the future plan line:
    """

    return ChatPromptTemplate.from_template(prompt)


class FuturePlanInput(BaseModel):
    user_context: str = Field(..., description="Complete user context")


@tool("generate_future_plan", args_schema=FuturePlanInput, return_direct=False)
def generate_future_plan(user_context: str) -> str:
    prompt: ChatPromptTemplate = create_future_plan_prompt_template()

    chain: Runnable = prompt | llm | StrOutputParser()

    return chain.invoke({"user_context": user_context})
