import json
from typing import List, Dict, Any, Optional

from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, constr
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from tools.utils import create_conversation_context, create_user_context

llm = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0.7, max_tokens=4000)


class FormattedActivity(BaseModel):
    position: constr(max_length=50) = Field(..., description="Action verb + unique role (HARD LIMIT ≤50 chars)")
    organization: constr(max_length=100) = Field(
        ..., description="Memorable org/initiative name (HARD LIMIT ≤100 chars)"
    )
    description: constr(max_length=150) = Field(
        ..., description="Did what + numbers + unique method + who benefited (HARD LIMIT ≤150 chars)"
    )

    # ONLY these three fields allowed - strictly enforced
    class Config:
        extra = "forbid"


class FormatActivitiesOutput(BaseModel):
    activities: List[FormattedActivity] = Field(
        ..., description="List of formatted activities with ONLY position, organization, and description fields"
    )


class FormatActivitiesInput(BaseModel):
    user_profile: Optional[Dict[str, Any]] = Field(None, description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")
    blueprint_json: Optional[str] = Field(
        None, description="Optional ActivitiesBlueprintOutput JSON to ground formatting"
    )
    ideas_json: Optional[str] = Field(None, description="Optional ActivityIdeasOutput JSON to ground formatting")
    as_text: bool = Field(
        False, description="Return human-readable Position/Organization/Description lines instead of JSON"
    )


def create_format_activities_prompt_template() -> ChatPromptTemplate:
    system_prompt = (
        "You are an elite U.S. college admissions strategist.\n"
        "Format activities STRICTLY into ONLY three fields: Position, Organization, Description.\n"
        "NO EXTRA FIELDS ALLOWED. Any enhancements must fit within these three fields.\n\n"
        "CHARACTER LIMITS (STRICTLY ENFORCED - count every character including spaces):\n"
        "- Position: MAXIMUM 50 characters (not 51, exactly ≤50 chars)\n"
        "- Organization: MAXIMUM 100 characters (not 101, exactly ≤100 chars)\n"
        "- Description: MAXIMUM 150 characters (not 151, exactly ≤150 chars)\n\n"
        "FORMAT REQUIREMENTS:\n"
        "- Position: [Action verb + Unique role] - must be ≤50 characters\n"
        "- Organization: [Memorable name that explains itself] - must be ≤100 characters\n"
        "- Description: [Did what + specific numbers + unique method + who benefited] - must be ≤150 characters\n\n"
        "ABSOLUTE RULES:\n"
        "- Output ONLY: position, organization, description. Nothing else.\n"
        "- NO extra keys like 'impact', 'alignment', 'notes', 'enhancements', etc.\n"
        "- If any field exceeds its character limit, you MUST rewrite it shorter. Never exceed limits.\n"
        "- Count characters carefully. If you're at 51, you must remove at least 1 character.\n"
        "- All enhancements from ideas must be condensed to fit within the three fields and their limits.\n\n"
        "SOURCES:\n"
        "- If Activities Blueprint JSON and/or Activity Ideas JSON are provided, use them as primary sources.\n"
        "- When ideas_json is provided, you MUST format ALL activities represented in it (across all categories). Do NOT downselect.\n"
        "- Only when no JSON is provided, infer up to 10 plausible activities from conversation/profile and format them.\n\n"
        "OUTPUT RULES:\n"
        "- Your response MUST be a valid JSON object that can be parsed without errors.\n"
        "- Do NOT include any text before or after the JSON object.\n"
        "- Do NOT use markdown code blocks or backticks.\n"
        "- Ensure all strings are properly escaped and all brackets/braces are balanced.\n"
        "- Keep outputs concise but specific; do not fabricate achievements; keep interview-defensible.\n\n"
        "{format_instructions}\n\n"
        "CONTEXT:\n"
        "{user_profile_context}\n"
        "OPTIONAL BLUEPRINT JSON (may be empty):\n"
        "{blueprint_json}\n"
        "OPTIONAL IDEAS JSON (may be empty):\n"
        "{ideas_json}\n"
    )

    user_prompt = (
        "{conversation_context}\n\n"
        "USER QUERY: {user_query}\n"
        "Produce formatted activities now. ONLY include position, organization, and description fields within their character limits."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )


@tool("format_activity_list", args_schema=FormatActivitiesInput, return_direct=False)
def format_activity_list(
    user_profile: Optional[Dict[str, Any]],
    recent_messages: List[BaseMessage],
    blueprint_json: Optional[str] = None,
    ideas_json: Optional[str] = None,
    as_text: bool = False,
) -> str:
    """Format activities STRICTLY into Position (≤50 chars), Organization (≤100 chars), and Description (≤150 chars) ONLY. No extra fields. All enhancements must fit within these three fields and character limits. Returns a valid JSON object. Can be grounded with optional blueprint/ideas JSON or inferred from conversation/profile."""

    conversation_context = create_conversation_context(recent_messages[:-1])
    user_profile_context = create_user_context(user_profile)

    # Heuristics: if the last message contains JSON and blueprint/ideas are missing, attach it
    detected_blueprint = blueprint_json or ""
    detected_ideas = ideas_json or ""
    try:
        last_msg = recent_messages[-1].content if recent_messages else ""
        if last_msg and (last_msg.strip().startswith("{") or last_msg.strip().startswith("[")):
            if not detected_blueprint:
                detected_blueprint = last_msg
            elif not detected_ideas:
                detected_ideas = last_msg
    except Exception:
        pass

    parser = PydanticOutputParser(pydantic_object=FormatActivitiesOutput)
    prompt = create_format_activities_prompt_template()

    chain = prompt | llm | parser

    max_retries = 3

    for attempt in range(max_retries):
        try:
            result = chain.invoke(
                {
                    "conversation_context": conversation_context,
                    "user_profile_context": user_profile_context,
                    "user_query": recent_messages[-1].content,
                    "blueprint_json": detected_blueprint,
                    "ideas_json": detected_ideas,
                    "format_instructions": parser.get_format_instructions(),
                }
            )

            if as_text:
                data = result.dict()
                lines = []
                for a in data.get("activities", []):
                    pos = a.get("position", "")
                    org = a.get("organization", "")
                    desc = a.get("description", "")
                    lines.append(f"Position: {pos} ({len(pos)})")
                    lines.append(f"Organization: {org} ({len(org)})")
                    lines.append(f"Description: {desc} ({len(desc)})")
                    lines.append("")
                return "\n".join(lines).strip()
            else:
                return json.dumps(result.dict(), indent=2)

        except Exception as e:
            return f"Error: {str(e)}"

    return json.dumps({"error": "Maximum retries exceeded"}, indent=2)
