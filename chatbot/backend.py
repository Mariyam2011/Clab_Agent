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
    # Optional toggles for web search query rewriting
    rewrite_queries: bool
    search_context: str | None

# 2. Define Chat Node
def chat_node(state: ChatState):
    """Chat node that calls the router tool when the user sends a message."""
    user_msg = state["messages"][-1].content  # last user message

    # For now, assume user_profile is known (could also be pulled from memory/db)
    user_profile = DUMMY_USER_DATA
    tool_option = state.get("tool_option", "standard strategy")
    format_option = state.get("format_option", "JSON")
    memory = state.get("memory", {})
    # Sync rewrite settings from state into memory so tools can read them
    try:
        if "rewrite_queries" in state:
            memory["rewrite_queries"] = bool(state.get("rewrite_queries", False))
        if state.get("search_context"):
            memory["search_context"] = state.get("search_context")
    except Exception:
        pass

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
        # If payload is a web_search response, render a concise text
        try:
            if isinstance(response, dict) and response.get("type") == "web_search" and isinstance(payload, dict):
                items = payload.get("results") or []
                meta_header = []
                if payload.get("original_query") or payload.get("final_query"):
                    meta_header.append(f"Original query: {payload.get('original_query','')}")
                    meta_header.append(f"Final query: {payload.get('final_query','')}")
                    meta_header.append(f"Rewrite applied: {payload.get('rewrite_applied', False)}")
                lines = (["\n".join(meta_header)] if meta_header else []) + ["Web search results:"]
                for idx, it in enumerate(items[:5], start=1):
                    title = it.get("title") or f"Result {idx}"
                    url = it.get("url") or ""
                    snippet = it.get("snippet") or ""
                    lines.append(f"{idx}. {title} - {url}\n{snippet}")
                text_out = "\n\n".join(lines) if len(lines) > 1 else str(payload)
                return {"messages": state["messages"] + [AIMessage(content=text_out)], "memory": memory}
        except Exception:
            pass
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
