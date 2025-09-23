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
    generate_narrative_angles,
    generate_future_plan,
    generate_activity_list,
    generate_main_essay_ideas,
)

config = {"recursion_limit": 4}


llm = AzureChatOpenAI(deployment_name="gpt-4o")


class ChatState(TypedDict):
    messages: List
    selected_agent: str | None


AGENT_TOOLS = {
    "narrative_angles": generate_narrative_angles,
    "future_plan": generate_future_plan,
    "activity_list": generate_activity_list,
    "main_essay_ideas": generate_main_essay_ideas,
}

SYSTEM_INSTRUCTIONS = (
    "You are an elite admissions strategist. "
    "Help students with college application strategy, essay writing, and academic planning. "
    "Provide helpful, detailed, and personalized responses based on the student's profile. "
    "Be encouraging and specific in your advice."
)


# For simple LLM calls
def _build_context_system_message(user_profile: Dict[str, Any]) -> SystemMessage:
    return SystemMessage(
        content=f"{SYSTEM_INSTRUCTIONS}\n\nSTUDENT PROFILE & CONTEXT: {json.dumps(user_profile, ensure_ascii=False)}"
    )


def invoke_agent_tool(agent_name: str, recent_messages: List[BaseMessage], user_profile: Dict[str, Any]) -> str:
    if agent_name not in AGENT_TOOLS:
        return f"Error: Unknown agent '{agent_name}'. Available agents: {list(AGENT_TOOLS.keys())}"

    try:
        tool_function = AGENT_TOOLS[agent_name]

        result = tool_function.invoke({"user_profile": user_profile, "recent_messages": recent_messages})

        if isinstance(result, dict):
            return json.dumps(result, indent=2, ensure_ascii=False)
        else:
            return str(result)

    except Exception as e:
        return f"Error calling {agent_name}: {str(e)}"


def chatbot_invoke(state: ChatState) -> ChatState:
    user_profile = DUMMY_USER_DATA
    recent_messages = state["messages"][-6:]

    selected_agent = state.get("selected_agent")

    if selected_agent and selected_agent in AGENT_TOOLS:
        response_content = invoke_agent_tool(selected_agent, recent_messages, user_profile)

        ai_message = AIMessage(content=response_content)
    else:
        system_msg = _build_context_system_message(user_profile)

        messages = [system_msg] + recent_messages

        ai_message = llm.invoke(messages)

    return {
        "messages": state["messages"] + [ai_message],
        "selected_agent": selected_agent,
    }


if __name__ == "__main__":
    state = {
        "messages": [],
        "selected_agent": None,
    }

    print("College Admissions Copilot - CLI Mode")
    print("Available agents: @narrative_angles, @future_plan, @activity_list, @main_essay_ideas")
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
