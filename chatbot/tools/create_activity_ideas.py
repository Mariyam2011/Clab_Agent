import json
import re
from typing import List, Dict, Any, Optional

from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from tools.utils import create_conversation_context, create_user_context

llm = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0.7, max_tokens=4000)


class ExistingEnhancement(BaseModel):
    elevated_title: Optional[str] = Field(
        None, description="Sharper, interview-defensible title aligned with future goals (≤50 chars if possible)"
    )
    elevated_organization: Optional[str] = Field(
        None,
        description="Improved org/initiative branding that connects to student's narrative (≤100 chars if possible)",
    )
    elevated_description: Optional[str] = Field(
        None,
        description="Stronger impact framing with method, results, and clear link to future goals (≤150 chars if possible)",
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Concrete ways to deepen impact/leadership that align with student's narrative and future goals",
    )
    alternative_suggestions: List[str] = Field(
        default_factory=list,
        description="Authentic alternative paths if current one is weak, ensuring alignment with future goals",
    )
    validation_or_evidence: List[str] = Field(
        default_factory=list, description="Evidence/data to collect to substantiate claims"
    )
    leverage_points: List[str] = Field(
        default_factory=list,
        description="Partners, platforms, or programs to amplify impact and strengthen narrative coherence",
    )


class DevelopedIdea(BaseModel):
    idea_name: str = Field(..., description="Memorable initiative/idea name that reflects student's narrative")
    impact_focus: str = Field(
        ..., description="Community/beneficiary and problem to solve, clearly aligned with student's future goals"
    )
    unique_method: str = Field(
        ..., description="Unexpected approach aligned to the student's skills, interests, and narrative"
    )
    resources_needed: List[str] = Field(default_factory=list, description="Tools, mentors, partnerships, or budget")
    first_90_days: List[str] = Field(default_factory=list, description="Step-by-step plan for first 90 days")
    milestones: List[str] = Field(
        default_factory=list,
        description="Key deliverables or checkpoints that demonstrate progress toward future goals",
    )
    success_metrics: List[str] = Field(default_factory=list, description="Measurable indicators of progress/impact")
    risks_and_mitigations: List[str] = Field(default_factory=list, description="Top risks and mitigations")


class ExistingActivityRef(BaseModel):
    title: str = Field(..., description="Current title or role")
    organization: Optional[str] = Field(None, description="Org/Initiative name")
    description: Optional[str] = Field(None, description="Brief description if available")


class MissingActivityRef(BaseModel):
    prompt: str = Field(
        ..., description="Short cue describing the gap to ideate on (e.g., 'community service in STEM')"
    )


class CategoryIdeas(BaseModel):
    category: str = Field(..., description="One of the idea categories from the blueprint")
    existing_enhancements: List[ExistingEnhancement] = Field(
        default_factory=list, description="Enhanced framing and improvement paths for existing items"
    )
    developed_missing_ideas: List[DevelopedIdea] = Field(
        default_factory=list, description="Developed ideas for identified gaps"
    )


class ActivityIdeasOutput(BaseModel):
    student_theme: Optional[str] = Field(
        None, description="Optional throughline inferred from the blueprint and profile, connecting to future goals"
    )
    future_goals_summary: Optional[str] = Field(
        None, description="Brief summary of student's stated future goals and intended trajectory"
    )
    categories: List[CategoryIdeas] = Field(
        ..., description="Per-category enhanced and developed ideas, all aligned with narrative and goals"
    )
    top_priorities: List[str] = Field(
        default_factory=list,
        description="3-5 recommended focus items to execute next that strengthen narrative coherence",
    )


class ActivityIdeasInput(BaseModel):
    user_profile: Optional[Dict[str, Any]] = Field(None, description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")
    blueprint_json: Optional[str] = Field(
        None, description="Counts-only Activities Blueprint text; used to enforce per-category totals summing to 10"
    )


def create_activity_ideas_prompt_template() -> ChatPromptTemplate:
    system_prompt = (
        "You are an elite U.S. college admissions strategist.\n"
        "Generate exactly 10 activities distributed across categories per the provided counts-only Activities Blueprint.\n"
        "Use the student's profile and conversation context to make each idea authentic and interview-defensible.\n\n"
        "CRITICAL ALIGNMENT REQUIREMENT:\n"
        "- EVERY activity (both existing enhancements and new ideas) MUST align with the student's narrative and future goals.\n"
        "- Explicitly identify the student's future goals, intended major/career path, and personal narrative from the profile and conversation.\n"
        "- When enhancing existing activities, frame them to show clear progression toward their future goals.\n"
        "- When developing missing activities, ensure they fill gaps that strengthen the narrative arc toward their aspirations.\n"
        "- The connection between each activity and future goals should be explicit and defensible in an interview.\n"
        "- Avoid generic activities that don't tie to the student's specific trajectory.\n\n"
        "INSTRUCTIONS:\n"
        "- The blueprint provides category lines like '- <Category>: Existing: N | Missing: M' and a final total of 10.\n"
        "- For each category, create N 'Existing' ideas (refine/strengthen plausible existing items) and M 'Generated' ideas.\n"
        "- Sum across categories MUST equal 10. Do not add or remove categories beyond those present in the blueprint counts.\n"
        "- Prefer overlooked communities, unexpected methods, measurable results, and clear alignment with the student's future plans.\n"
        "- Keep ideas realistic and defensible; avoid inflated claims.\n"
        "- Ensure narrative coherence: activities should tell a cohesive story that leads to their stated future goals.\n\n"
        "OUTPUT RULES:\n"
        "- Your response MUST be a valid JSON object that can be parsed without errors.\n"
        "- Do NOT include any text before or after the JSON object.\n"
        "- Do NOT use markdown code blocks or backticks.\n"
        "- Ensure all strings are properly escaped and all brackets/braces are balanced.\n"
        "- Populate 'categories' with one entry per category present in the blueprint counts.\n"
        "- Put refined existing items in 'existing_enhancements' and generated items in 'developed_missing_ideas'.\n"
        "- The total number of items across all categories (existing_enhancements + developed_missing_ideas) MUST be 10.\n\n"
        "{format_instructions}\n\n"
        "CONTEXT:\n"
        "{user_profile_context}\n"
        "BLUEPRINT COUNTS (counts-only text):\n"
        "{blueprint_counts}\n"
    )

    user_prompt = (
        "{conversation_context}\n\n"
        "USER QUERY: {user_query}\n"
        "Produce the 10 activities now, honoring the per-category counts. Ensure EVERY activity strongly aligns with the student's narrative and future goals."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )


@tool("create_activity_ideas", args_schema=ActivityIdeasInput, return_direct=False)
def create_activity_ideas(
    user_profile: Optional[Dict[str, Any]],
    recent_messages: List[BaseMessage],
    blueprint_json: Optional[str] = None,
) -> str:
    """Generate exactly 10 activities distributed per counts-only Activities Blueprint, strongly aligned with student's narrative and future goals.

    - Parses counts-only blueprint lines: "- <Category>: Existing: N | Missing: M" plus the final total line.
    - Produces ideas such that the sum across categories equals 10.
    - Uses student's profile and conversation context for authenticity.
    - EVERY activity (existing enhancements and new ideas) MUST align with the student's narrative and future goals.
    - Ensures narrative coherence: activities tell a cohesive story leading to stated future aspirations.
    """

    conversation_context = create_conversation_context(recent_messages[:-1])
    user_profile_context = create_user_context(user_profile)

    # Try to auto-detect blueprint counts text from the latest message if not provided explicitly
    detected_blueprint = blueprint_json or ""
    try:
        last_msg = recent_messages[-1].content if recent_messages else ""
        # Heuristic: if last message looks like JSON, include it verbatim
        if (
            not detected_blueprint
            and last_msg
            and (last_msg.strip().startswith("{") or last_msg.strip().startswith("["))
        ):
            detected_blueprint = last_msg
    except Exception:
        pass

    # Parse counts from the counts-only blueprint text
    def parse_counts(text: str) -> List[Dict[str, Any]]:
        counts: List[Dict[str, Any]] = []
        if not text:
            return counts
        # Example line: "- Category: Existing: 1 | Missing: 2"
        line_pattern = re.compile(r"^\s*-\s*(.+?):\s*Existing:\s*(\d+)\s*\|\s*Missing:\s*(\d+)\s*$")
        for raw_line in text.splitlines():
            m = line_pattern.match(raw_line.strip())
            if m:
                cat = m.group(1).strip()
                existing = int(m.group(2))
                missing = int(m.group(3))
                counts.append({"category": cat, "existing": existing, "missing": missing})
        return counts

    parser = PydanticOutputParser(pydantic_object=ActivityIdeasOutput)
    prompt = create_activity_ideas_prompt_template()

    chain = prompt | llm | parser

    max_retries = 3

    for attempt in range(max_retries):
        try:
            result = chain.invoke(
                {
                    "conversation_context": conversation_context,
                    "user_profile_context": user_profile_context,
                    "user_query": recent_messages[-1].content if recent_messages else "",
                    "blueprint_counts": detected_blueprint,
                    "format_instructions": parser.get_format_instructions(),
                }
            )

            return json.dumps(result.dict(), indent=2)

        except Exception as e:
            return f"Error: {str(e)}"

    return json.dumps({"error": "Maximum retries exceeded"}, indent=2)
