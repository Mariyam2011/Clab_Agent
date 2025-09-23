"""
Activity list generation tool for college application strategy.
Generates enhanced activities and 3 new signature activities based on user context.
"""

import json
import logging
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, validator
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from tools.utils import create_conversation_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = AzureChatOpenAI(deployment_name="gpt-4o", temperature=0.7, max_tokens=4000)


class Activity(BaseModel):
    """Model for a single activity with validation."""

    current: str = Field(..., description="Current activity description")
    elevated: str = Field(..., description="Enhanced version with deeper impact")
    position: str = Field(..., description="Position title", max_length=50)
    organization: str = Field(..., description="Organization name", max_length=100)
    description: str = Field(..., description="Activity description", max_length=150)

    @validator("position")
    def validate_position_length(cls, v):
        if len(v) > 50:
            return v[:47] + "..."
        return v

    @validator("organization")
    def validate_organization_length(cls, v):
        if len(v) > 100:
            return v[:97] + "..."
        return v

    @validator("description")
    def validate_description_length(cls, v):
        if len(v) > 150:
            return v[:147] + "..."
        return v


class NewActivity(BaseModel):
    """Model for new signature activities."""

    position: str = Field(..., description="Position title", max_length=50)
    organization: str = Field(..., description="Organization name", max_length=100)
    description: str = Field(..., description="Activity description", max_length=150)
    impact_focus: str = Field(..., description="Who this activity targets/helps")
    unique_method: str = Field(..., description="What makes this approach unexpected")

    @validator("position")
    def validate_position_length(cls, v):
        if len(v) > 50:
            return v[:47] + "..."
        return v

    @validator("organization")
    def validate_organization_length(cls, v):
        if len(v) > 100:
            return v[:97] + "..."
        return v

    @validator("description")
    def validate_description_length(cls, v):
        if len(v) > 150:
            return v[:147] + "..."
        return v


class ActivityListOutput(BaseModel):
    """Complete activity list output with validation."""

    enhanced_activities: List[Activity] = Field(..., description="Enhanced versions of existing activities")

    new_signature_activities: List[NewActivity] = Field(
        ..., description="Three new signature activities", min_items=3, max_items=3
    )


def create_activity_list_generator_prompt_template() -> ChatPromptTemplate:
    system_prompt = """You are acting as a U.S. college admissions counselor. 
    Critically think: what kind of activity list would make this student stand out at the world's most selective universities? 
    Activities should feel authentic, unique, and interview-defensible, while highlighting hidden impact and originality.

    TASK: Transform existing activities into standout accomplishments AND invent exactly three new signature activities that are bold, unexpected, and deeply connected to the student's mission.

    STRICT FORMAT REQUIREMENTS:
    - Position: EXACTLY 50 characters or less
    - Organization: EXACTLY 100 characters or less  
    - Description: EXACTLY 150 characters or less
    - Count characters carefully - exceeding limits will cause errors

    CRITICAL AUTHENTICITY WARNING:
    - Enhance by revealing hidden impact, creative methods, and overlooked beneficiaries
    - Do NOT inflate numbers or invent fictional elements. Every claim must be defensible in an interview
    - Admissions officers can immediately detect exaggeration

    FOR ENHANCED ACTIVITIES:
    - Current: What they currently have
    - Elevated: Deeper framing, hidden impact, measurable results
    - Position: Action verb + unique role (≤50 chars)
    - Organization: Memorable org name (≤100 chars)  
    - Description: What + numbers + method + beneficiaries (≤150 chars)

    FOR NEW SIGNATURE ACTIVITIES (exactly 3):
    - Must target an overlooked community
    - Must use an unexpected method
    - Must create measurable change
    - Must include memorable initiative name
    - Position: Leadership role (≤50 chars)
    - Organization: Initiative/org name (≤100 chars)
    - Description: Impact + method + results (≤150 chars)
    - Impact_focus: Who this helps
    - Unique_method: What makes approach unexpected

    COUNSELOR'S EXPECTATION:
    - Every activity demonstrates leadership, creativity, and impact
    - Activities progress logically: involvement → initiative → leadership → scaling
    - Each should make admissions officers think: "Only this student could have done this"

    {format_instructions}
    """

    user_prompt = """Use the following user context to generate the activity list per the instructions above:

    {user_context}

    Remember: 
    - Enhance existing activities by revealing hidden impact
    - Create exactly 3 new signature activities
    - Stay within character limits
    - Make every activity authentic and interview-defensible
    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
    )


class ActivityListInput(BaseModel):
    user_profile: Dict[str, Any] = Field(..., description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")


@tool("format_activity_list", args_schema=ActivityListInput, return_direct=False)
def format_activity_list(user_profile: Dict[str, Any], recent_messages: List[BaseMessage]) -> str:
    """Generate enhanced activities and new signature activities for college applications based on user context."""

    user_context = create_conversation_context(recent_messages)
    user_context += f"\n\nSTUDENT PROFILE & CONTEXT: {json.dumps(user_profile, ensure_ascii=False)}"

    parser = PydanticOutputParser(pydantic_object=ActivityListOutput)

    prompt = create_activity_list_generator_prompt_template()

    chain = prompt | llm | parser

    max_retries = 3

    for attempt in range(max_retries):
        try:
            result = chain.invoke(
                {"user_context": user_context, "format_instructions": parser.get_format_instructions()}
            )

            result_dict = result.dict()

            return json.dumps(result_dict, indent=2)

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")

            pass

    return json.dumps({"error": "Maximum retries exceeded"}, indent=2)
