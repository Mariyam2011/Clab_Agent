# tools.py
import json
from typing import Any, Dict, Optional, Union

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from prompt_templates.narratives import create_narrative_angles_prompt_template
from prompt_templates.Future_plan import create_future_plan_prompt_template
from prompt_templates.Activity import create_activity_list_generator_prompt_template
from prompt_templates.Main_essay import create_main_essay_ideas_prompt_template

try:
    from langchain_core.tools import tool  # modern
except Exception:
    from langchain.tools import tool       # fallback

# Add logging to track tool calls and catch issues early
import logging
logging.basicConfig(level=logging.INFO)

# Initialize LLM
llm = AzureChatOpenAI(deployment_name="gpt-4o")

# ---------- Input Schemas ----------
class NarrativeAnglesInput(BaseModel):
    user_profile: Union[ Dict[str, Any],str] = Field(..., description="Student profile dict or JSON string")
# - Change input schemas to handle both dict and string
#class NarrativeAnglesInput(BaseModel):
#    student_profile: Union[Dict[str, Any], str] = Field(..., description="Student profile")

class FuturePlanInput(BaseModel):
    user_profile: Union[ Dict[str, Any],str] = Field(..., description="Student profile dict or JSON string")
    narrative: str = Field(..., description="One narrative angle object or JSON string")


class ActivityListInput(BaseModel):
    user_profile:Union[ Dict[str, Any],str] = Field(..., description="Student profile dict or JSON string")
    narrative: str = Field(..., description="One narrative angle object or JSON string")
    future_plan: str = Field(..., description="Future plan single-line statement")


class MainEssayIdeasInput(BaseModel):
    user_profile:Union[ Dict[str, Any],str] = Field(..., description="Student profile dict or JSON string")
    narrative: Union[Dict[str, Any], str] = Field(..., description="One narrative angle object")
    future_plan: str = Field(..., description="Future plan single-line statement")
    activity_result: str = Field(..., description="Activity list text result")

class CompleteStrategyInput(BaseModel):
    student_profile: Union[Dict[str, Any], str] = Field(..., description="Student profile dict or JSON string")


# ---------- Helper Functions ----------
def _parse_input(input_data: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Parse input data that could be either a dict or JSON string"""
    if isinstance(input_data, str):
        try:
            return json.loads(input_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON string: {e}")
            raise ValueError(f"Invalid JSON string: {e}")
    return input_data

def _safe_json_parse(raw_output: str) -> Dict[str, Any]:
    """Safely parse JSON output with fallback extraction"""
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parsing failed: {e}")
        # Try to extract JSON from the response
        import re
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        raise ValueError(f"Invalid JSON response: {raw_output[:200]}...")


# ---------- Tool Implementations ----------
@tool("generate_narrative_angles", args_schema=NarrativeAnglesInput, return_direct=False)
def generate_narrative_angles(user_profile: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Generate 3–5 narrative angles as JSON."""
    prompt: ChatPromptTemplate = create_narrative_angles_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    raw = chain.invoke({"user_profile": json.dumps(user_profile)})
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Invalid JSON from model", "raw": raw}


@tool("generate_future_plan", args_schema=FuturePlanInput, return_direct=False)
def generate_future_plan(user_profile: Union[Dict[str, Any], str], narrative: Dict[str, Any]) -> str:
    """Generate a single ≤100 character future plan line."""
    prompt: ChatPromptTemplate = create_future_plan_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain.invoke({
        "user_profile": json.dumps(user_profile),
        "narrative": narrative
    })


@tool("generate_activity_list", args_schema=ActivityListInput, return_direct=False)
def generate_activity_list(user_profile: Union[Dict[str, Any], str], narrative: Dict[str, Any], future_plan: str) -> str:
    """Generate enhanced activities and 3 new signature activities."""
    prompt: ChatPromptTemplate = create_activity_list_generator_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain.invoke({
        "user_profile": json.dumps(user_profile),
        "narrative": narrative,
        "future_plan": future_plan
    })


@tool("generate_main_essay_ideas", args_schema=MainEssayIdeasInput, return_direct=False)
def generate_main_essay_ideas(user_profile: Union[Dict[str, Any], str], narrative: Union[Dict[str, Any], str], future_plan: str, activity_result: str) -> Dict[str, Any]:

        # normalize everything into dicts
    if isinstance(user_profile, str):
        user_profile = json.loads(user_profile)
    if isinstance(narrative, str):
        narrative = json.loads(narrative)
    
    prompt: ChatPromptTemplate = create_main_essay_ideas_prompt_template()
    chain: Runnable = prompt | llm | StrOutputParser()
    raw = chain.invoke({
        "user_profile": json.dumps(user_profile,ensure_ascii=False),
        "narrative": json.dumps(narrative ,ensure_ascii=False),
        "future_plan": future_plan,
        "activity_result": activity_result
    })
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Invalid JSON from model", "raw": raw}


@tool("generate_complete_application_strategy", return_direct=False)
def generate_complete_application_strategy(user_profile: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Generate a complete application strategy by chaining narrative → future plan → activities → main essay ideas."""

    # Step 1: Generate narratives
    narratives = generate_narrative_angles.invoke({"user_profile": user_profile})
    #narratives = generate_narrative_angles(user_profile=user_profile)
    if "error" in narratives:
        return {"error": "Failed at narrative stage", "details": narratives}

    # Step 2: Generate future plan
    future_plan = generate_future_plan.invoke({"user_profile": user_profile, "narrative": narratives})
    #future_plan = generate_future_plan(user_profile=user_profile, narrative=narratives)
    if not future_plan or "error" in str(future_plan).lower():
        return {"error": "Failed at future plan stage", "details": future_plan}

    # Step 3: Generate activity list
    activities = generate_activity_list.invoke({"user_profile": user_profile, "narrative": narratives, "future_plan": future_plan})
    #activities = generate_activity_list(user_profile=user_profile, narrative=narratives, future_plan=future_plan)
    if not activities or "error" in str(activities).lower():
        return {"error": "Failed at activities stage", "details": activities}

    # Step 4: Generate main essay ideas
    essay_ideas = generate_main_essay_ideas.invoke({"user_profile": user_profile, "narrative": narratives, "future_plan": future_plan, "activity_result": activities})
    #essay_ideas = generate_main_essay_ideas(user_profile=user_profile, narrative=narratives, future_plan=future_plan, activity_result=activities)
    if "error" in essay_ideas:
        return {"error": "Failed at essay stage", "details": essay_ideas}

    # Final combined result
    return {
        "narratives": narratives,
        "future_plan": future_plan,
        "activities": activities,
        "essay_ideas": essay_ideas
    }
