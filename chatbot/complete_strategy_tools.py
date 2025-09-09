import ast
import json
from typing import Any, Dict, Union

from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from prompt_templates.narratives import create_narrative_angles_prompt_template
from prompt_templates.Future_plan import create_future_plan_prompt_template
from prompt_templates.Activity import create_activity_list_generator_prompt_template
from prompt_templates.Main_essay import create_main_essay_ideas_prompt_template

from tools import generate_narrative_angles, generate_future_plan, generate_activity_list, generate_main_essay_ideas

try:
    from langchain_core.tools import tool  # modern
except Exception:
    from langchain.tools import tool  # fallback

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = AzureChatOpenAI(deployment_name="gpt-4o")

def _strip_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # remove opening fence and optional language
        s = s[3:]
        if s.lower().startswith("json"):
            s = s[4:]
        # remove trailing fence
        if s.rstrip().endswith("```"):
            s = s.rstrip()[:-3]
    return s.strip()

def _coerce_json(raw):
    if not isinstance(raw, str):
        return raw
    s = _strip_fences(raw)
    try:
        return json.loads(s)
    except Exception:
        pass
    # best-effort: extract biggest {...}
    try:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start:end+1])
    except Exception:
        pass
    # last resort
    try:
        return ast.literal_eval(s)
    except Exception:
        return None

# ---------- Input Schema ----------

class CompleteStrategyInput(BaseModel):
    user_profile: Union[Dict[str, Any], str] = Field(
        ..., description="Student profile dict or JSON string"
    )


# ---------- Complete Strategy Tool ----------

@tool("generate_complete_application_strategy", args_schema=CompleteStrategyInput, return_direct=True)
def generate_complete_application_strategy(user_profile: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """Generate a complete application strategy in a narrative → future plan → activities → essay flow."""

    # Step 1: Narratives
    narratives = generate_narrative_angles.invoke({"user_profile": user_profile})
    if "error" in narratives:
        return {"error": "Failed at narrative stage", "details": narratives}

    # Ensure list format
    narrative_list = narratives.get("narrative_angles", narratives) if isinstance(narratives, dict) else narratives
    if not isinstance(narrative_list, list):
        return {"error": "Narratives not in expected list format", "raw": narratives}

    strategy_flow = []
    for narrative in narrative_list:
        # Step 2: Future plan
        future_plan = generate_future_plan.invoke(
            {"user_profile": user_profile, "narrative": narrative}
        )
        if not future_plan or "error" in str(future_plan).lower():
            strategy_flow.append({
                "narrative": narrative,
                "error": "Failed at future plan stage",
                "details": future_plan
            })
            continue

        # Step 3: Activities
        activities = generate_activity_list.invoke(
            {
                "user_profile": user_profile,
                "narrative": narrative,
                "future_plan": future_plan,
            }
        )
        if not activities or "error" in str(activities).lower():
            strategy_flow.append({
                "narrative": narrative,
                "future_plan": future_plan,
                "error": "Failed at activities stage",
                "details": activities
            })
            continue

        # Step 4: Essay
        essay_ideas = generate_main_essay_ideas.invoke(
            {
                "user_profile": user_profile,
                "narrative": narrative,
                "future_plan": future_plan,
                "activity_result": activities,
            }
        )
        if "error" in essay_ideas:
            strategy_flow.append({
                "narrative": narrative,
                "future_plan": future_plan,
                "activities": activities,
                "error": "Failed at essay stage",
                "details": essay_ideas
            })
            continue

        # Successful flow
        strategy_flow.append({
            "narrative": narrative,
            "future_plan": future_plan,
            "activities": activities,
            "essay_ideas": essay_ideas,
        })

    return {"complete_strategy": strategy_flow}


# ---------- Router Layer ----------

@tool("route_tool_call_complete", return_direct=True)
def route_tool_call_complete(user_request: str, user_profile: Union[Dict[str, Any], str]) -> Any:
    """
    Route user request. Only supports:
    - "complete strategy" → generate_complete_application_strategy
    """
    request_lower = user_request.lower()

    if "complete" in request_lower or "strategy" in request_lower:
        result = generate_complete_application_strategy.invoke({
        "user_request": "complete strategy",
        "user_profile": user_profile
})
        return json.dumps(result, ensure_ascii=False, indent=2)

    return {"error": "Unknown request type. Try: complete strategy."}
