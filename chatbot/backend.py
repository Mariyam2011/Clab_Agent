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
from tools import route_tool_call, json_to_markdown 
from complete_strategy_tools import route_tool_call_complete

config = {"configurable": {"thread_id": "1"}}

# 1. Define Chat State
class ChatState(TypedDict):
    messages: List  # will hold conversation messages
    tool_option: str

# 2. Define Chat Node
def chat_node(state: ChatState):
    """Chat node that calls the router tool when the user sends a message."""
    user_msg = state["messages"][-1].content  # last user message

    # For now, assume user_profile is known (could also be pulled from memory/db)
    user_profile = DUMMY_USER_DATA
    tool_option = state.get("tool_option", "standard strategy")

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
            "user_profile": user_profile
        })
        return {"messages": state["messages"] + [AIMessage(content=str(response))]}
    except Exception as e:
        return {"messages": state["messages"] + [AIMessage(content=f"Error: {e}")]}

# 3. Build the Graph
checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.set_finish_point("chat")

chatbot = graph.compile(checkpointer=checkpointer)

# 4. Run the Chatbot
if __name__ == "__main__":
    state = {"messages": [], "tool_option": "standard strategy"}
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        tool_choice = input("Select tool: 1. Standard Strategy 2. Complete Strategy ")
        if tool_choice == "2":
            state["tool_option"] = "complete strategy"
        else:
            state["tool_option"] = "standard strategy"
            
        # Add user msg to state (append takes only the message)
        state["messages"].append(HumanMessage(content=user_input))

        # Run one step through the graph (pass config here)
        state = chatbot.invoke(state, config=config)

        print("Bot:", state["messages"][-1].content)
