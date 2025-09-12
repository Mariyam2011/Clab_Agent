import ast
import json
import re
import os
import requests
from copy import deepcopy
from typing import Any, Dict, Union, List, Optional

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
    from langchain.tools import tool  # fallback

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = AzureChatOpenAI(deployment_name="gpt-4o")

# ---------- Helpers ----------
def _strip_fences_and_labels(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = s[3:]
        first_newline = s.find("\n")
        if first_newline != -1:
            s = s[first_newline + 1 :]
        if s.rstrip().endswith("```"):
            s = s.rstrip()[:-3]
    if s.lower().startswith("json "):
        s = s[5:]
    return s.strip()


def _coerce_json_best_effort(raw: Any) -> Any:
    if not isinstance(raw, str):
        return raw
    s = _strip_fences_and_labels(raw)
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start : end + 1])
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        return None

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


class JSONToMarkdownLLMInput(BaseModel):
    data: Union[Dict[str, Any], List[Any], str] = Field(
        ..., description="JSON object/list or JSON string to convert to Markdown using LLM"
    )
    title: str | None = Field(
        default=None, description="Optional top-level title for the Markdown output"
    )
    style_hint: str | None = Field(
        default=None,
        description="Optional style guidance (e.g., 'Complete Application Strategy format').",
    )

# ---------- Tools ----------

class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query for the web")
    num_results: int = Field(default=5, description="Number of results to return (1-10)")
    time_window: Optional[str] = Field(
        default=None,
        description="Optional recency filter, e.g., 'd7' (7 days), 'm1' (1 month)")
    rewrite: bool = Field(default=False, description="Rewrite the query with LLM before searching")
    context: Optional[str] = Field(default=None, description="Optional domain context for rewriting")


class QueryRewriteInput(BaseModel):
    raw_query: str = Field(..., description="Original user query to be rewritten")
    context: Optional[str] = Field(
        default=None,
        description="Optional context about the search domain (e.g., 'college admissions', 'scholarships')")

@tool("rewrite_search_query", args_schema=QueryRewriteInput, return_direct=False)
def rewrite_search_query(raw_query: str, context: Optional[str] = None) -> str:
    """Rewrite a user search query to be clearer and more specific for web search."""
    system_instructions = (
        "You are a query rewriting expert. Improve the user's search query for web search. "
        "Keep it concise (<= 20 words), unambiguous, and include key entities, constraints, and intent. "
        "Prefer neutral phrasing, avoid stopwords, avoid quotes unless necessary, and do not add hallucinated facts. "
        "Return ONLY the rewritten query, no extra text."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "Context (optional): {ctx}\n\nOriginal query: {q}\n\nRewritten query:"),
    ])
    chain: Runnable = prompt | llm | StrOutputParser()
    rewritten = chain.invoke({"ctx": context or "", "q": raw_query})
    return rewritten.strip()

def _use_tavily(query: str, num_results: int, time_window: Optional[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "search_depth": "advanced",
            "max_results": max(1, min(num_results, 10)),
        }
        if time_window:
            payload["time_window"] = time_window
        resp = requests.post("https://api.tavily.com/search", headers=headers, json=payload, timeout=30)
        data = resp.json()
        results = []
        for item in (data.get("results") or [])[:num_results]:
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "snippet": item.get("content") or item.get("snippet"),
                "source": "tavily",
            })
        return results
    except Exception:
        return []


def perform_web_search(
    query: str,
    num_results: int = 5,
    time_window: Optional[str] = None,
    rewrite: bool = False,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """Search using Tavily with optional LLM rewriting and return metadata + results."""
    original_query = query
    final_query = query
    if rewrite:
        try:
            final_query = rewrite_search_query.invoke({"raw_query": query, "context": context})  # type: ignore
            if isinstance(final_query, dict) and "error" in final_query:
                final_query = original_query
            elif isinstance(final_query, dict) and "rewritten" in final_query:
                final_query = final_query.get("rewritten") or original_query
            elif not isinstance(final_query, str):
                final_query = original_query
        except Exception:
            final_query = original_query

    results = _use_tavily(final_query, num_results, time_window)
    return {
        "original_query": original_query,
        "final_query": final_query,
        "results": results,
        "count": len(results),
        "time_window": time_window,
        "rewrite_applied": bool(rewrite) and final_query != original_query,
    }


def _should_use_web(user_text: str) -> bool:
    text = user_text.lower()
    triggers = [
        r"\b(current|latest|recent|today|now|this\s+year|202\d|202[0-9])\b",
        r"\b(news|update|changes?|deadlines?|rankings?|requirements?)\b",
        r"\bsearch\b|\bweb\b|\bonline\b",
    ]
    for pat in triggers:
        if re.search(pat, text):
            return True
    return False


@tool("web_search", args_schema=WebSearchInput, return_direct=False)
def web_search(
    query: str,
    num_results: int = 5,
    time_window: Optional[str] = None,
    rewrite: bool = False,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """Search the web and return metadata + list of sources with title, url, snippet."""
    payload = perform_web_search(
        query=query,
        num_results=num_results,
        time_window=time_window,
        rewrite=rewrite,
        context=context,
    )
    return payload

@tool("generate_narrative_angles", args_schema=NarrativeAnglesInput, return_direct=False)
def generate_narrative_angles(user_profile: Union[Dict[str, Any], str]) -> Dict[str, Any]:
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
    parsed = _coerce_json_best_effort(raw)
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

    def wants_narrative(s: str) -> bool:
        return re.search(r"\b(narrative|angle|angles)\b", s) is not None

    def wants_future(s: str) -> bool:
        return re.search(r"\b(future\s*plan|future|plan)\b", s) is not None

    def wants_activities(s: str) -> bool:
        return re.search(r"\b(activit(?:y|ies)|extracurriculars?)\b", s) is not None

    def wants_essay(s: str) -> bool:
        return re.search(r"\b(essay|personal\s*statement|main\s*essay)\b", s) is not None

    # Opportunistic web enrichment
    enriched_profile = user_profile
    try:
        if _should_use_web(text):
            web_payload = web_search.invoke({
                "query": user_request,
                "num_results": 5,
                "rewrite": bool(memory.get("rewrite_queries", False)),
                "context": memory.get("search_context"),
            })
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

    if wants_narrative(text):
        result = generate_narrative_angles.invoke({"user_profile": enriched_profile})
        return {
            "type": "narrative",
            "result": result,
            "memory": {"narratives": result, **({"web_context": memory.get("web_context")} if memory.get("web_context") else {})},
        }

    if wants_future(text):
        narratives = cached_narratives or generate_narrative_angles.invoke({"user_profile": enriched_profile})
        result = generate_future_plan.invoke({"user_profile": enriched_profile, "narrative": narratives})
        return {
            "type": "future_plan",
            "result": result,
            "memory": {"narratives": narratives, "future_plan": result, **({"web_context": memory.get("web_context")} if memory.get("web_context") else {})},
        }

    if wants_activities(text):
        narratives = cached_narratives or generate_narrative_angles.invoke({"user_profile": enriched_profile})
        future_plan = cached_future_plan or generate_future_plan.invoke({"user_profile": enriched_profile, "narrative": narratives})
        result = generate_activity_list.invoke({
            "user_profile": enriched_profile,
            "narrative": narratives,
            "future_plan": future_plan,
        })
        return {
            "type": "activities",
            "result": result,
            "memory": {"narratives": narratives, "future_plan": future_plan, "activities": result, **({"web_context": memory.get("web_context")} if memory.get("web_context") else {})},
        }

    if wants_essay(text):
        narratives = cached_narratives or generate_narrative_angles.invoke({"user_profile": enriched_profile})
        future_plan = cached_future_plan or generate_future_plan.invoke({"user_profile": enriched_profile, "narrative": narratives})
        activities = cached_activities or generate_activity_list.invoke({
            "user_profile": enriched_profile,
            "narrative": narratives,
            "future_plan": future_plan,
        })
        result = generate_main_essay_ideas.invoke({
            "user_profile": json.dumps(enriched_profile, ensure_ascii=False),
            "narrative": json.dumps(narratives, ensure_ascii=False),
            "future_plan": future_plan,
            "activity_result": activities,
        })
        return {
            "type": "essay",
            "result": result,
            "memory": {"narratives": narratives, "future_plan": future_plan, "activities": activities, **({"web_context": memory.get("web_context")} if memory.get("web_context") else {})},
        }
    # Explicit web search request
    if re.search(r"\b(web\s*search|search\s*web|search)\b", text):
        payload = web_search.invoke({
            "query": user_request,
            "num_results": 5,
            "rewrite": bool(memory.get("rewrite_queries", False)),
            "context": memory.get("search_context"),
        })
        memory["web_context"] = payload.get("results")
        memory["web_meta"] = {
            "original_query": payload.get("original_query"),
            "final_query": payload.get("final_query"),
            "rewrite_applied": payload.get("rewrite_applied", False),
            "time_window": payload.get("time_window"),
        }
        return {"type": "web_search", "result": payload, "memory": {"web_context": memory["web_context"], "web_meta": memory["web_meta"]}}
    return {"error": "Unknown request type. Try: narrative, future plan, activities, essay, or 'search'."}


@tool("json_to_markdown_llm", args_schema=JSONToMarkdownLLMInput, return_direct=False)
def json_to_markdown_llm(data: Union[Dict[str, Any], List[Any], str]) -> str:
    """Convert JSON to Markdown using the LLM. Returns pure Markdown (no code fences)."""
    try:
        py = data if isinstance(data, (dict, list)) else json.loads(_strip_fences_and_labels(str(data)))
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

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "JSON:\n{json}"),
    ])

    chain: Runnable = prompt | llm | StrOutputParser()

    raw = chain.invoke({"json": json_str})

    md = _strip_fences_and_labels(raw)

    return md.strip()
