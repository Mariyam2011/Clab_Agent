import json
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

from .create_activities_blueprint import create_activities_blueprint
from .create_activity_ideas import create_activity_ideas
from .format_activity_list import format_activity_list


class CreateActivityListInput(BaseModel):
    user_profile: Optional[Dict[str, Any]] = Field(None, description="Complete user profile")
    recent_messages: List[BaseMessage] = Field(..., description="Recent conversation messages")
    include_intermediate: bool = Field(
        False, description="Include intermediate blueprint and ideas in the final output"
    )


@tool("create_activity_list", args_schema=CreateActivityListInput, return_direct=False)
def create_activity_list(
    user_profile: Optional[Dict[str, Any]],
    recent_messages: List[BaseMessage],
    include_intermediate: bool = True,
) -> str:
    """Run sequential workflow: activities_blueprint -> activity_ideas -> format_activity_list.
    Returns a consolidated JSON object including all stages when include_intermediate=True;
    otherwise returns only the final formatted activities JSON.
    """

    result: Dict[str, Any] = {}

    # Step 1: Create Activities Blueprint
    try:
        blueprint_text = create_activities_blueprint.invoke(
            {"user_profile": user_profile, "recent_messages": recent_messages}
        )
        blueprint_json = json.loads(blueprint_text)
        if include_intermediate:
            result["activities_blueprint"] = blueprint_json
    except Exception as e:
        return json.dumps({"error": f"Blueprint error: {str(e)}"}, indent=2)

    # Step 2: Create Activity Ideas (grounded by blueprint)
    try:
        ideas_text = create_activity_ideas.invoke(
            {
                "user_profile": user_profile,
                "recent_messages": recent_messages,
                "blueprint_json": blueprint_text,
            }
        )
        ideas_json = json.loads(ideas_text)
        if include_intermediate:
            result["activity_ideas"] = ideas_json
    except Exception as e:
        return json.dumps({"error": f"Ideas error: {str(e)}"}, indent=2)

    # Step 3: Format Activity List (grounded by blueprint + ideas)
    try:
        formatted_text = format_activity_list.invoke(
            {
                "user_profile": user_profile,
                "recent_messages": recent_messages,
                "blueprint_json": blueprint_text,
                "ideas_json": ideas_text,
                "as_text": False,
            }
        )
        formatted_json = json.loads(formatted_text)
        if include_intermediate:
            result["formatted_activity_list"] = formatted_json
        else:
            return formatted_text
    except Exception as e:
        return json.dumps({"error": f"Formatting error: {str(e)}"}, indent=2)

    return json.dumps(result, indent=2)
