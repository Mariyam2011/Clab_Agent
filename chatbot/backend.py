import os
import sys

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph
from typing import TypedDict, List
from langgraph.checkpoint.memory import MemorySaver
from user_data import DUMMY_USER_DATA
from dotenv import load_dotenv

load_dotenv()

# Allow importing modules from project root (one level up)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your router tool
from tools import route_tool_call, json_to_markdown_llm
from complete_strategy_tools import route_tool_call_complete

config = {"configurable": {"thread_id": "1"}}

# 1. Define Chat State
class ChatState(TypedDict):
    messages: List  # will hold conversation messages
    tool_option: str
    format_option: str  # "JSON" or "Markdown (LLM)"
    memory: dict  # short-term memory for artifacts

# 2. Define Chat Node
def chat_node(state: ChatState):
    """Chat node that calls the router tool when the user sends a message."""
    user_msg = state["messages"][-1].content  # last user message

    # For now, assume user_profile is known (could also be pulled from memory/db)
    user_profile = DUMMY_USER_DATA
    tool_option = state.get("tool_option", "standard strategy")
    format_option = state.get("format_option", "JSON")
    memory = state.get("memory", {})

    # Route request → tool execution
    try:
        if tool_option == "complete strategy":
            response = route_tool_call_complete.invoke({
                "user_request": user_msg,
                "user_profile": user_profile
            })
        else:
            response = route_tool_call.invoke({
                "user_request": user_msg,
                "user_profile": user_profile,
                "memory": memory,
                "conversation_history": [
                    {"role": ("user" if isinstance(m, HumanMessage) else "assistant"), "content": m.content}
                    for m in state["messages"][-6:]
                ],
            })

        # Optional LLM-based Markdown formatting
        if format_option == "Markdown (LLM)":
            output = None
            try:
                import json as _json
                # Unwrap memory-aware response shape
                if isinstance(response, dict) and "result" in response:
                    new_memory = response.get("memory") or {}
                    memory.update(new_memory)
                    payload = response.get("result")
                else:
                    payload = response

                if isinstance(payload, (dict, list)):
                    py_obj = payload
                else:
                    try:
                        py_obj = _json.loads(str(payload))
                    except Exception:
                        py_obj = None
                if py_obj is not None:
                    output = json_to_markdown_llm.invoke({
                        "data": py_obj,

                    })
            except Exception:
                output = None
            if output is None:
                output = str(payload)
            new_state = {"messages": state["messages"] + [AIMessage(content=output)], "memory": memory}
            return new_state

        # Raw/JSON path
        if isinstance(response, dict) and "result" in response:
            memory.update(response.get("memory") or {})
            payload = response.get("result")
        else:
            payload = response
        return {"messages": state["messages"] + [AIMessage(content=str(payload))], "memory": memory}
    except Exception as e:
        return {"messages": state["messages"] + [AIMessage(content=f"Error: {e}")], "memory": memory}

# 3. Build the Graph
checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.set_finish_point("chat")

chatbot = graph.compile(checkpointer=checkpointer)

# 4. Run the Chatbot
if __name__ == "__main__":
    state = {"messages": [], "tool_option": "standard strategy", "format_option": "JSON", "memory": {}}
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        tool_choice = input("Select tool: 1. Standard Strategy 2. Complete Strategy ")
        if tool_choice == "2":
            state["tool_option"] = "complete strategy"
        else:
            state["tool_option"] = "standard strategy"
        fmt_choice = input("Select output: 1. JSON 2. Markdown (LLM) ")
        if fmt_choice == "2":
            state["format_option"] = "Markdown (LLM)"
        else:
            state["format_option"] = "JSON"
            
        # Add user msg to state (append takes only the message)
        state["messages"].append(HumanMessage(content=user_input))

        # Run one step through the graph (pass config here)
        state = chatbot.invoke(state, config=config)

        print("Bot:", state["messages"][-1].content)
