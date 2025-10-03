import json
from typing import List, Dict, Any, Optional

from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from tools.utils import create_conversation_context, create_user_context

llm = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0.7, max_tokens=4000)

ACTIVITY_CATEGORIES = [
    "Olympiad / Competition",
    "Council/ Leadership Position",
    "Research Project",
    "Research Paper",
    "Passion Project",
    "Community Service",
    "Unique Activity",
    "Hobby",
    "Publications / Podcast / Blogs",
    "Sports / Other Activity",
]


class ActivityBlueprintItem(BaseModel):
    title: str = Field(..., description="Short, interview-defensible activity title")
    organization: str = Field(..., description="Org/Initiative name or context")
    description: str = Field(..., description="Impact + method + result, concise but specific")


class CategoryCounts(BaseModel):
    category: str = Field(..., description="Category name from the predefined list")
    existing: int = Field(..., description="Number of existing activities in this category")
    missing: int = Field(..., description="Number of missing activities to be created in this category")


class ActivitiesBlueprintOutput(BaseModel):
    categories: List[CategoryCounts] = Field(
        ..., description="Per-category counts (only include categories with total > 0)"
    )
    total: int = Field(..., description="Total number of activities across all categories")


class ActivitiesBlueprintInput(BaseModel):
    user_profile: Optional[Dict[str, Any]] = Field(None, description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")
    target_total: int = Field(10, description="Target total number of activities (N+M)")


def create_activities_blueprint_prompt_template() -> ChatPromptTemplate:
    system_prompt = (
        "You are an elite U.S. college admissions strategist.\n"
        "Categorize activities STRICTLY using the categories below.\n"
        "For each category: (1) map 'Existing Activities' from the student's profile; (2) if weak or empty, add realistic 'Missing Activities' that align with profile and goals.\n"
        "Do not cap the number of activities in a category — include as many as the profile/context justifies.\n"
        "Also produce per-category counts and a total ONLY.\n"
        "CRITICAL: The TOTAL number of activities across ALL categories (Existing + Missing combined) MUST be exactly {target_total}. If fewer than {target_total} exist, add Missing items to reach {target_total}. If more than {target_total} exist, select the most representative {target_total} and omit the rest.\n\n"
        "CATEGORIES (use exactly these labels):\n"
        f"- {ACTIVITY_CATEGORIES[0]}\n"
        f"- {ACTIVITY_CATEGORIES[1]}\n"
        f"- {ACTIVITY_CATEGORIES[2]}\n"
        f"- {ACTIVITY_CATEGORIES[3]}\n"
        f"- {ACTIVITY_CATEGORIES[4]}\n"
        f"- {ACTIVITY_CATEGORIES[5]}\n"
        f"- {ACTIVITY_CATEGORIES[6]}\n"
        f"- {ACTIVITY_CATEGORIES[7]}\n"
        f"- {ACTIVITY_CATEGORIES[8]}\n"
        f"- {ACTIVITY_CATEGORIES[9]}\n\n"
        "OUTPUT RULES:\n"
        "- Your response MUST be a valid JSON object that can be parsed without errors.\n"
        "- Do NOT include any text before or after the JSON object.\n"
        "- Do NOT use markdown code blocks or backticks.\n"
        "- Ensure all strings are properly escaped and all brackets/braces are balanced.\n"
        "- Include ONLY categories with total counts > 0 (existing + missing > 0).\n"
        "- Distribute counts based on the student profile and conversation; categories may have more than one item.\n"
        "- Counts per category must be non-negative integers and the final 'total' field must be exactly {target_total}.\n\n"
        "{format_instructions}\n\n"
        "CONTEXT:\n"
        "{user_profile_context}\n"
    )
    user_prompt = "{conversation_context}\n\nUSER QUERY: {user_query}\nProduce the activities blueprint JSON now, honoring the target total of {target_total}."

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )


@tool("create_activities_blueprint", args_schema=ActivitiesBlueprintInput, return_direct=False)
def create_activities_blueprint(
    user_profile: Optional[Dict[str, Any]],
    recent_messages: List[BaseMessage],
    target_total: int = 10,
) -> str:
    """Generate per-category counts and a total as a valid JSON object.

    Behavior:
    - For each fixed category, infer counts of Existing and Missing based on profile/context; omit categories with total 0.
    - Categories can have any non-negative counts; include as many as justified by the profile/context.
    - Output a JSON object with 'categories' array and 'total' field.
    - The TOTAL number of activities across all categories (Existing + Missing) MUST be exactly {target_total}. If fewer exist, add Missing to reach {target_total}; if more, select the most representative {target_total} to count.
    """

    conversation_context = create_conversation_context(recent_messages[:-1]) if recent_messages else ""
    user_profile_context = create_user_context(user_profile)
    last_user_query = recent_messages[-1].content if recent_messages else ""

    parser = PydanticOutputParser(pydantic_object=ActivitiesBlueprintOutput)
    prompt = create_activities_blueprint_prompt_template()

    chain = prompt | llm | parser

    max_retries = 3

    for attempt in range(max_retries):
        try:
            result = chain.invoke(
                {
                    "conversation_context": conversation_context,
                    "user_profile_context": user_profile_context,
                    "user_query": last_user_query,
                    "target_total": target_total,
                    "format_instructions": parser.get_format_instructions(),
                }
            )

            return json.dumps(result.dict(), indent=2)

        except Exception:
            continue

    # Fallback: return JSON with exactly target_total, omitting empty categories
    categories_used = ACTIVITY_CATEGORIES[:3]
    per_category = target_total // 3
    remainder = target_total % 3
    counts_missing = [per_category + (1 if i < remainder else 0) for i in range(3)]

    fallback_output = {
        "categories": [
            {"category": cat, "existing": 0, "missing": m} for cat, m in zip(categories_used, counts_missing)
        ],
        "total": target_total,
    }
    return json.dumps(fallback_output, indent=2)
