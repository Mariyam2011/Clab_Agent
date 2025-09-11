import os
import sys
import json
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

# Allow importing from project root (one level up from /chatbot)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import router, formatters, and default profile
from tools import route_tool_call, json_to_markdown_llm
from complete_strategy_tools import route_tool_call_complete

try:
    from user_data import DUMMY_USER_DATA as DEFAULT_PROFILE
except Exception:
    # Provide a minimal fallback profile so the app runs even if user_data is missing
    DEFAULT_PROFILE = {
        "name": "Student",
        "academic": {},
        "activities": [],
        "future_plans": [],
    }

st.set_page_config(page_title="Admissions Strategy Chatbot", page_icon="🎓")
st.title("Admissions Strategy Chatbot")

# Sidebar profile editor
st.sidebar.header("User Profile (JSON)")
profile_text = st.sidebar.text_area(
    "Edit profile JSON",
    json.dumps(DEFAULT_PROFILE, indent=2, ensure_ascii=False),
    height=420,
)
tool_option = st.selectbox("Select tool:", ["Standard Strategy", "Complete Strategy"])
format_option = st.selectbox("Output formatting:", ["JSON", "Markdown (LLM)"])

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"|"assistant", "content": str}
if "memory" not in st.session_state:
    st.session_state.memory = {}

# Render history
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Ask for narrative, future plan, activities, essay or complete strategy"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Parse profile JSON
    try:
        user_profile = json.loads(profile_text)
    except Exception as e:
        error_msg = f"Invalid profile JSON: {e}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)
        st.stop()
    
    # Call router tool
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if tool_option == "Complete Strategy":
                    response = route_tool_call_complete.invoke({
                        "user_request": user_input,
                        "user_profile": user_profile,
                    })
                else:
                    response = route_tool_call.invoke({
                        "user_request": user_input,
                        "user_profile": user_profile,
                        "memory": st.session_state.memory,
                        "conversation_history": st.session_state.messages[-6:],
                    })

                # Decide how to render output
                # Unwrap memory-aware response
                new_memory = None
                payload = response
                if isinstance(response, dict) and "result" in response:
                    new_memory = response.get("memory") or {}
                    payload = response.get("result")

                if new_memory:
                    st.session_state.memory.update(new_memory)

                if format_option == "Raw/JSON":
                    output = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2)
                else:
                    # Try to coerce to JSON-like Python object
                    py_obj = None
                    if isinstance(payload, (dict, list)):
                        py_obj = payload
                    elif isinstance(payload, str):
                        try:
                            py_obj = json.loads(payload)
                        except Exception:
                            py_obj = None

                    if py_obj is not None:
                        try:
                            if format_option == "Markdown (LLM)":
                                output = json_to_markdown_llm.invoke({
                                    "data": py_obj,
                                })
                            else:
                                output = json_to_markdown_llm.invoke({"data": py_obj})
                        except Exception:
                            output = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2)
                    else:
                        # Fall back to raw rendering if we cannot parse JSON
                        output = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2)
            except Exception as e:
                output = f"Error: {e}"

            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})