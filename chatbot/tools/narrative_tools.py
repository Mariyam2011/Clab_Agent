"""
Narrative generation tools for college application strategy.
Contains tools for generating narrative angles, future plans, activities, and essay ideas.
"""

import ast
import json
from typing import Any, Dict, Union

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from prompt_templates.narratives import create_narrative_angles_prompt_template
from prompt_templates.future_plan import create_future_plan_prompt_template
from prompt_templates.activity_list import (
    create_activity_list_generator_prompt_template,
)
from prompt_templates.main_essay import create_main_essay_ideas_prompt_template

from .utilities import coerce_json_best_effort

try:
    from langchain_core.tools import tool  # modern
except Exception:
    from langchain.tools import tool  # fallback

# Initialize LLM
llm = AzureChatOpenAI(deployment_name="gpt-4o")


# ---------- Input Schemas ----------
class NarrativeAnglesInput(BaseModel):
    user_profile: Union[Dict[str, Any], str] = Field(
        ..., description="Student profile dict or JSON string"
    )


class FuturePlanInput(BaseModel):
    user_profile: Union[Dict[str, Any], str] = Field(
        ..., description="Student profile dict or JSON string"
    )
    narrative: Union[Dict[str, Any], str] = Field(
        ..., description="One narrative angle object or JSON string"
    )


class ActivityListInput(BaseModel):
    user_profile: Union[Dict[str, Any], str] = Field(
        ..., description="Student profile dict or JSON string"
    )
    narrative: Union[Dict[str, Any], str] = Field(
        ..., description="One narrative angle object or JSON string"
    )
    future_plan: str = Field(..., description="Future plan single-line statement")


class MainEssayIdeasInput(BaseModel):
    user_profile: Union[Dict[str, Any], str] = Field(
        ..., description="Student profile dict or JSON string"
    )
    narrative: Union[Dict[str, Any], str] = Field(
        ..., description="One narrative angle object"
    )
    future_plan: str = Field(..., description="Future plan single-line statement")
    activity_result: str = Field(..., description="Activity list text result")


# ---------- Tools ----------
@tool(
    "generate_narrative_angles", args_schema=NarrativeAnglesInput, return_direct=False
)
def generate_narrative_angles(
    user_profile: Union[Dict[str, Any], str],
) -> Dict[str, Any]:
    """Generate 3-5 narrative angles as JSON."""
    if isinstance(user_profile, str):
        try:
            user_profile = json.loads(user_profile)
        except json.JSONDecodeError:
            try:
                user_profile = ast.literal_eval(user_profile)
            except (ValueError, SyntaxError):
                return {"error": "Invalid user_profile format", "raw": user_profile}

    prompt: ChatPromptTemplate = create_narrative_angles_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    raw = chain.invoke({"user_profile": json.dumps(user_profile)})
    parsed = coerce_json_best_effort(raw)
    if isinstance(parsed, (dict, list)):
        return parsed  # expected dict with narrative_angles or list
    return {"error": "Invalid JSON from model", "raw": raw}


@tool("generate_future_plan", args_schema=FuturePlanInput, return_direct=False)
def generate_future_plan(
    user_profile: Union[Dict[str, Any], str], narrative: Union[Dict[str, Any], str]
) -> str:
    """Generate a single ≤100 character future plan line."""
    if isinstance(user_profile, str):
        try:
            user_profile = json.loads(user_profile)
        except json.JSONDecodeError:
            try:
                user_profile = ast.literal_eval(user_profile)
            except (ValueError, SyntaxError):
                return f"Error: Invalid user_profile format: {user_profile}"

    prompt: ChatPromptTemplate = create_future_plan_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain.invoke(
        {"user_profile": json.dumps(user_profile), "narrative": narrative}
    )


@tool("generate_activity_list", args_schema=ActivityListInput, return_direct=False)
def generate_activity_list(
    user_profile: Union[Dict[str, Any], str],
    narrative: Union[Dict[str, Any], str],
    future_plan: str,
) -> str:
    """Generate enhanced activities and 3 new signature activities."""
    if isinstance(user_profile, str):
        try:
            user_profile = json.loads(user_profile)
        except json.JSONDecodeError:
            try:
                user_profile = ast.literal_eval(user_profile)
            except (ValueError, SyntaxError):
                return f"Error: Invalid user_profile format: {user_profile}"

    prompt: ChatPromptTemplate = create_activity_list_generator_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain.invoke(
        {
            "user_profile": json.dumps(user_profile),
            "narrative": narrative,
            "future_plan": future_plan,
        }
    )


@tool("generate_main_essay_ideas", args_schema=MainEssayIdeasInput, return_direct=False)
def generate_main_essay_ideas(
    user_profile: Union[Dict[str, Any], str],
    narrative: Union[Dict[str, Any], str],
    future_plan: str,
    activity_result: str,
) -> Dict[str, Any]:
    """Generate comprehensive main essay ideas based on narrative, future plan, and activities."""

    if isinstance(user_profile, str):
        try:
            user_profile = json.loads(user_profile)
        except json.JSONDecodeError:
            try:
                user_profile = ast.literal_eval(user_profile)
            except (ValueError, SyntaxError):
                return {"error": "Invalid user_profile format", "raw": user_profile}

    if isinstance(narrative, str):
        try:
            narrative = json.loads(narrative)
        except json.JSONDecodeError:
            try:
                narrative = ast.literal_eval(narrative)
            except (ValueError, SyntaxError):
                return {"error": "Invalid narrative format", "raw": narrative}

    prompt: ChatPromptTemplate = create_main_essay_ideas_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    raw = chain.invoke(
        {
            "user_profile": json.dumps(user_profile, ensure_ascii=False),
            "narrative": json.dumps(narrative, ensure_ascii=False),
            "future_plan": future_plan,
            "activity_result": activity_result,
        }
    )
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Invalid JSON from model", "raw": raw}
