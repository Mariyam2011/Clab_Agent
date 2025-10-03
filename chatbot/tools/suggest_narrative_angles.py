"""
Narrative angles generation tool for college application strategy.
Generates 3-5 narrative angles based on user context.
"""

from typing import List, Dict, Any, Optional
from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from tools.utils import create_conversation_context, create_user_context

from langchain_core.messages import BaseMessage


llm = AzureChatOpenAI(deployment_name="gpt-4o")


def create_narrative_angles_prompt_template() -> ChatPromptTemplate:
    system_prompt = """You are an elite U.S. college admissions narrative strategist. 
    Your task is to analyze the given student profile and generate 3-5 unique narrative angles 
    that admissions officers would find both surprising and inevitable.  

    STRATEGY RULES:
    1. Find the Invisible Thread → Identify a hidden connection between the student's activities, origins, struggles, and ambitions.
    2. Fuse Identity with Purpose → Show how their background directly fuels their academic and life mission.
    3. Anchor in a Crystallizing Moment → Use a vivid, sensory, emotionally-charged scene to ground the story.
    4. Make It Actionable → Propose a named initiative that feels ambitious yet achievable.
    5. Organic Alignment → Suggest majors that naturally grow out of the story—never forced.

    OUTPUT FORMAT:
    You must output ONLY a valid JSON object in the following structure. 
    No commentary, no extra text.

    IMPORTANT JSON RULES:
    - All text must be on single lines - NO line breaks within string values
    - Escape all quotes and special characters properly
    - Use \\n for line breaks within text if needed
    - Ensure all JSON is properly formatted and valid

    {{
      "narrative_angles": [
        {{
          "title": "string - action-oriented, unexpected pairing",
          "positioning": "string - one sentence that makes admissions officers lean forward",
          "essay_concept": "string - single line paragraph describing essay journey: opening scene → personal connection → broader realization → action → future vision",
          "anchor_scene": "string - 3-5 sentences, vivid, sensory, emotional, all in one line using \\n if needed",
          "unexpected_twist": "string - why this combination surprises",
          "signature_initiative": {{
            "name": "string",
            "description": "string - what it does and for whom"
          }},
          "natural_major_fit": ["string", "string", "string"]
        }}
      ]
    }}

    {user_profile_context}
    """

    user_prompt = """{conversation_context}
    
    USER QUERY: {user_query}

    Analyze the student profile and produce 3-5 narrative angles in the exact JSON structure above.

    Return exactly one JSON object. Do not include any trailing commas. 
    Do not include explanations, comments, or text outside the JSON. 
    Every string value must be a single line. If you must break lines, use "\\n"
    """

    return ChatPromptTemplate.from_messages([("system", system_prompt), ("user", user_prompt)])


class NarrativeAnglesInput(BaseModel):
    user_profile: Optional[Dict[str, Any]] = Field(None, description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")


@tool("suggest_narrative_angles", args_schema=NarrativeAnglesInput, return_direct=False)
def suggest_narrative_angles(user_profile: Optional[Dict[str, Any]], recent_messages: List[BaseMessage]) -> str:
    """Generate unique narrative angles for college application strategy based on user context."""
    conversation_context = create_conversation_context(recent_messages[:-1])

    user_profile_context = create_user_context(user_profile)

    prompt: ChatPromptTemplate = create_narrative_angles_prompt_template()

    chain: Runnable = prompt | llm | StrOutputParser()

    return chain.invoke(
        {
            "conversation_context": conversation_context,
            "user_profile_context": user_profile_context,
            "user_query": recent_messages[-1].content,
        }
    )
