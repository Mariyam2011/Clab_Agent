"""
Routing tools for orchestrating different application strategy components.
Contains the main routing logic that determines which tools to use based on user requests.
"""

import json
import re
from copy import deepcopy
from typing import Any, Dict, List, Union


from .narrative_tools import (
    generate_narrative_angles,
    generate_future_plan,
    generate_activity_list,
    generate_main_essay_ideas,
)
from .web_tools import web_search, should_use_web

try:
    from langchain_core.tools import tool  # modern
except Exception:
    from langchain.tools import tool  # fallback


# ---------- Helper Functions ----------
def _wants_narrative(s: str) -> bool:
    """Check if user request wants narrative generation."""
    return re.search(r"\b(narrative|angle|angles)\b", s) is not None


def _wants_future(s: str) -> bool:
    """Check if user request wants future plan generation."""
    return re.search(r"\b(future\s*plan|future|plan)\b", s) is not None


def _wants_activities(s: str) -> bool:
    """Check if user request wants activity list generation."""
    return re.search(r"\b(activit(?:y|ies)|extracurriculars?)\b", s) is not None


def _wants_essay(s: str) -> bool:
    """Check if user request wants essay ideas generation."""
    return re.search(r"\b(essay|personal\s*statement|main\s*essay)\b", s) is not None


# ---------- Tools ----------
@tool("route_tool_call", return_direct=True)
def route_tool_call(
    user_request: str,
    user_profile: Union[Dict[str, Any], str],
    memory: Union[Dict[str, Any], None] = None,
    conversation_history: Union[List[Dict[str, str]], str, None] = None,
) -> Any:
    """
    Route user request to the appropriate tool, generating minimal dependencies:
    - "narrative" → generate_narrative_angles
    - "future plan" → narrative → future_plan
    - "activities" → narrative → future_plan → activities
    - "essay" → narrative → future_plan → activities → essay
    - "complete strategy" → generate_complete_application_strategy (all components)
    """
    text = user_request.lower()

    # Initialize/normalize short-term memory container
    if memory is None or not isinstance(memory, dict):
        memory = {}

    # Helpers to fetch cached artifacts from memory if present
    cached_narratives = memory.get("narratives")
    cached_future_plan = memory.get("future_plan")
    cached_activities = memory.get("activities")

    # Opportunistic web enrichment
    enriched_profile = user_profile
    try:
        if should_use_web(text):
            web_payload = web_search.invoke(
                {
                    "query": user_request,
                    "num_results": 5,
                    "rewrite": bool(memory.get("rewrite_queries", False)),
                    "context": memory.get("search_context"),
                }
            )
            memory["web_context"] = web_payload.get("results")
            memory["web_meta"] = {
                "original_query": web_payload.get("original_query"),
                "final_query": web_payload.get("final_query"),
                "rewrite_applied": web_payload.get("rewrite_applied", False),
                "time_window": web_payload.get("time_window"),
            }
            if isinstance(user_profile, dict):
                tmp = deepcopy(user_profile)
                tmp["web_context"] = memory["web_context"]
                enriched_profile = tmp
    except Exception:
        enriched_profile = user_profile

    if _wants_narrative(text):
        result = generate_narrative_angles.invoke({"user_profile": enriched_profile})
        return {
            "type": "narrative",
            "result": result,
            "memory": {
                "narratives": result,
                **(
                    {"web_context": memory.get("web_context")}
                    if memory.get("web_context")
                    else {}
                ),
            },
        }

    if _wants_future(text):
        narratives = cached_narratives or generate_narrative_angles.invoke(
            {"user_profile": enriched_profile}
        )
        result = generate_future_plan.invoke(
            {"user_profile": enriched_profile, "narrative": narratives}
        )
        return {
            "type": "future_plan",
            "result": result,
            "memory": {
                "narratives": narratives,
                "future_plan": result,
                **(
                    {"web_context": memory.get("web_context")}
                    if memory.get("web_context")
                    else {}
                ),
            },
        }

    if _wants_activities(text):
        narratives = cached_narratives or generate_narrative_angles.invoke(
            {"user_profile": enriched_profile}
        )
        future_plan = cached_future_plan or generate_future_plan.invoke(
            {"user_profile": enriched_profile, "narrative": narratives}
        )
        result = generate_activity_list.invoke(
            {
                "user_profile": enriched_profile,
                "narrative": narratives,
                "future_plan": future_plan,
            }
        )
        return {
            "type": "activities",
            "result": result,
            "memory": {
                "narratives": narratives,
                "future_plan": future_plan,
                "activities": result,
                **(
                    {"web_context": memory.get("web_context")}
                    if memory.get("web_context")
                    else {}
                ),
            },
        }

    if _wants_essay(text):
        narratives = cached_narratives or generate_narrative_angles.invoke(
            {"user_profile": enriched_profile}
        )
        future_plan = cached_future_plan or generate_future_plan.invoke(
            {"user_profile": enriched_profile, "narrative": narratives}
        )
        activities = cached_activities or generate_activity_list.invoke(
            {
                "user_profile": enriched_profile,
                "narrative": narratives,
                "future_plan": future_plan,
            }
        )
        result = generate_main_essay_ideas.invoke(
            {
                "user_profile": json.dumps(enriched_profile, ensure_ascii=False),
                "narrative": json.dumps(narratives, ensure_ascii=False),
                "future_plan": future_plan,
                "activity_result": activities,
            }
        )
        return {
            "type": "essay",
            "result": result,
            "memory": {
                "narratives": narratives,
                "future_plan": future_plan,
                "activities": activities,
                **(
                    {"web_context": memory.get("web_context")}
                    if memory.get("web_context")
                    else {}
                ),
            },
        }

    # Explicit web search request
    if re.search(r"\b(web\s*search|search\s*web|search)\b", text):
        payload = web_search.invoke(
            {
                "query": user_request,
                "num_results": 5,
                "rewrite": bool(memory.get("rewrite_queries", False)),
                "context": memory.get("search_context"),
            }
        )
        memory["web_context"] = payload.get("results")
        memory["web_meta"] = {
            "original_query": payload.get("original_query"),
            "final_query": payload.get("final_query"),
            "rewrite_applied": payload.get("rewrite_applied", False),
            "time_window": payload.get("time_window"),
        }
        return {
            "type": "web_search",
            "result": payload,
            "memory": {
                "web_context": memory["web_context"],
                "web_meta": memory["web_meta"],
            },
        }

    return {
        "error": "Unknown request type. Try: narrative, future plan, activities, essay, or 'search'."
    }
