import os
import sys
import json
from typing import TypedDict, List, Dict, Any

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from user_data import DUMMY_USER_DATA

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

from tools import (
    suggest_narrative_angles,
    create_future_plan,
    create_activity_list,
    generate_main_essay_ideas,
)

from tools.convert_to_markdown import json_to_markdown_llm

config = {"recursion_limit": 4}


llm = AzureChatOpenAI(deployment_name="gpt-4o")


class ChatState(TypedDict):
    messages: List
    selected_agent: str | None
    fetch_user_data: bool
    convert_to_markdown: bool
    use_web_search: bool


AGENT_TOOLS = {
    "suggest_narrative_angles": suggest_narrative_angles,
    "create_future_plan": create_future_plan,
    "create_activity_list": create_activity_list,
    "generate_main_essay_ideas": generate_main_essay_ideas,
}

SYSTEM_INSTRUCTIONS = (
    "You are an elite admissions strategist. "
    "Help students with college application strategy, essay writing, and academic planning. "
    "Provide helpful, detailed, and general responses. "
    "Be encouraging and specific in your advice."
)


# For simple LLM calls
def _build_context_system_message(user_profile: Dict[str, Any] | None) -> SystemMessage:
    if user_profile:
        return SystemMessage(
            content=f"{SYSTEM_INSTRUCTIONS}\n\nSTUDENT PROFILE & CONTEXT: {json.dumps(user_profile, ensure_ascii=False)}"
        )
    else:
        return SystemMessage(content=SYSTEM_INSTRUCTIONS)


def invoke_agent_tool(
    agent_name: str,
    recent_messages: List[BaseMessage],
    user_profile: Dict[str, Any] | None,
    convert_to_markdown: bool = False,
) -> str:
    if agent_name not in AGENT_TOOLS:
        return f"Error: Unknown agent '{agent_name}'. Available agents: {list(AGENT_TOOLS.keys())}"

    try:
        tool_function = AGENT_TOOLS[agent_name]

        result = tool_function.invoke({"user_profile": user_profile, "recent_messages": recent_messages})

        if isinstance(result, dict):
            result_str = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result_str = str(result)

        if convert_to_markdown:
            try:
                result_str = json_to_markdown_llm.invoke({"data": result})
            except Exception as e:
                result_str = f"{result_str}\n\n*Note: Markdown conversion failed: {str(e)}*"

        return result_str

    except Exception as e:
        return f"Error calling {agent_name}: {str(e)}"


def chatbot_invoke(state: ChatState) -> ChatState:
    fetch_user_data = state.get("fetch_user_data", False)
    convert_to_markdown = state.get("convert_to_markdown", True)
    use_web_search = state.get("use_web_search", False)

    user_profile = DUMMY_USER_DATA if fetch_user_data else None

    recent_messages = state["messages"]

    selected_agent = state.get("selected_agent")

    if selected_agent and selected_agent in AGENT_TOOLS:
        response_content = invoke_agent_tool(selected_agent, recent_messages, user_profile, convert_to_markdown)

        ai_message = AIMessage(content=response_content)
    else:
        system_msg = _build_context_system_message(user_profile)

        messages = [system_msg] + recent_messages

        ai_message = llm.invoke(messages)

    return {
        "messages": state["messages"] + [ai_message],
        "selected_agent": selected_agent,
        "fetch_user_data": fetch_user_data,
        "convert_to_markdown": convert_to_markdown,
    }


if __name__ == "__main__":
    state = {
        "messages": [],
        "selected_agent": None,
        "fetch_user_data": True,
    }

    print("College Admissions Copilot - CLI Mode")
    print("Type 'exit' or 'quit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        selected_agent = None

        if user_input.startswith("@"):
            parts = user_input.split(" ", 1)
            agent_name = parts[0][1:]

            if agent_name in AGENT_TOOLS:
                selected_agent = agent_name

        state["messages"].append(HumanMessage(content=user_input))
        state["selected_agent"] = selected_agent

        state = chatbot_invoke(state)

        print("Bot:", state["messages"][-1].content)
        print()
