import os
import sys
import json

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph
from typing import TypedDict, List
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.tool_node import tools_condition
from user_data import DUMMY_USER_DATA
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Allow importing modules from project root (one level up)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import tools to bind to the LLM
from tools import (
    route_tool_call,
    json_to_markdown_llm,
    web_search,
    rewrite_search_query,
)
from complete_strategy_tools import route_tool_call_complete

config = {"recursion_limit": 4}

# Initialize LLM with tool calling
_AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
llm = AzureChatOpenAI(deployment_name=_AZURE_DEPLOYMENT)
tools = [
    route_tool_call,
    route_tool_call_complete,
    json_to_markdown_llm,
    web_search,
    rewrite_search_query,
]
llm_with_tools = llm.bind_tools(tools)

# 1. Define Chat State
class ChatState(TypedDict):
    messages: List  # will hold conversation messages
    tool_option: str
    format_option: str  # "JSON" or "Markdown (LLM)"
    memory: dict  # short-term memory for artifacts
    # Optional toggles for web search query rewriting
    rewrite_queries: bool
    search_context: str | None

"""
2. Define Agent + Tool nodes using LLM tool calling
"""

SYSTEM_INSTRUCTIONS = (
    "You are an elite admissions strategist. "
    "Use the available tools to fulfill the user's request. "
    "Prefer calling the router tools (`route_tool_call` or `route_tool_call_complete`) once per user request. "
    "Always include the user's profile, short-term memory, and recent conversation as tool arguments when applicable. "
    "If tool results are already present in the conversation, synthesize the final answer directly and DO NOT call tools again. "
    "If a tool returns structured JSON, you may return it directly or format using `json_to_markdown_llm` when asked for Markdown."
)

def _build_context_system_message(state: ChatState) -> SystemMessage:
    user_profile = DUMMY_USER_DATA
    memory = dict(state.get("memory", {}))
    try:
        if "rewrite_queries" in state:
            memory["rewrite_queries"] = bool(state.get("rewrite_queries", False))
        if state.get("search_context"):
            memory["search_context"] = state.get("search_context")
    except Exception:
        pass

    conversation_history = [
        {"role": ("user" if isinstance(m, HumanMessage) else "assistant"), "content": m.content}
        for m in state.get("messages", [])[-6:]
    ]

    ctx = {
        "user_profile": user_profile,
        "memory": memory,
        "conversation_history": conversation_history,
        "format_option": state.get("format_option", "JSON"),
        "tool_option": state.get("tool_option", "standard strategy"),
    }
    return SystemMessage(content=f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT(JSON): {json.dumps(ctx)}")

def agent_node(state: ChatState):
    # Build system message with context and any prior tool results (so the LLM can finalize)
    base_sys = _build_context_system_message(state).content
    recent = state["messages"][-12:]
    tool_results = [m.content for m in recent if isinstance(m, ToolMessage)]
    if tool_results:
        try:
            base_sys += "\n\nTOOL_RESULTS:\n" + "\n".join(tool_results[:4])
            base_sys += "\n\nSTRICT: The above tool results are sufficient. Do NOT call any tools again. Produce the final answer now."
        except Exception:
            pass
    system_msg = SystemMessage(content=base_sys)
    # Azure constraint: drop ToolMessage from the visible transcript
    cleaned = [m for m in recent if not isinstance(m, ToolMessage)]
    msgs = [system_msg] + cleaned
    ai = llm_with_tools.invoke(msgs)
    return {"messages": state["messages"] + [ai]}

tools_node = ToolNode(tools)

def should_continue(state: ChatState):
    """Route to tools only if the last assistant message actually requested a tool call.

    Prevents infinite ping-pong when the model replies without tool_calls or when
    prior tool messages exist but have been sanitized from the visible transcript.
    """
    try:
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
            return "tools"
    except Exception:
        pass
    return "end"

# 3. Build the Graph

graph = StateGraph(ChatState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tools_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

chatbot = graph.compile()

# 4. Run the Chatbot
if __name__ == "__main__":
    state = {"messages": [], "tool_option": "standard strategy", "format_option": "JSON", "memory": {}, "rewrite_queries": False, "search_context": None}
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
        try:
            rw_choice = input("Rewrite web queries? 1. No 2. Yes ")
            state["rewrite_queries"] = True if rw_choice.strip() == "2" else False
            if state["rewrite_queries"]:
                ctx = input("Query rewrite context (optional): ")
                state["search_context"] = ctx if ctx.strip() else None
            else:
                state["search_context"] = None
        except Exception:
            state["rewrite_queries"] = False
            state["search_context"] = None
            
        # Add user msg to state (append takes only the message)
        state["messages"].append(HumanMessage(content=user_input))

        # Run one step through the graph (pass config here)
        state = chatbot.invoke(state, config=config)

        print("Bot:", state["messages"][-1].content)
