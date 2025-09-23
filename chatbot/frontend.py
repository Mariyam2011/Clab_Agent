import os
import sys
import streamlit as st
import re
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="College Admissions Copilot", page_icon="🎓")
st.title("🎓 College Admissions Copilot")


# Display agent help in sidebar
with st.sidebar:
    st.markdown("**Examples:**")
    st.markdown("`@narrative_angles` - Generate narrative angles for my profile")
    st.markdown("`@future_plan` with focus on engineering")
    st.markdown("`@activity_list` based on my interests")
    st.markdown("`@main_essay_ideas` based on my profile")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])


AVAILABLE_AGENTS = [
    "narrative_angles",
    "future_plan",
    "activity_list",
    "main_essay_ideas",
]

user_input = st.chat_input("Type @ to select an agent, then describe what you need...")

if user_input:
    agent_pattern = r"@(\w+)"
    agent_matches = re.findall(agent_pattern, user_input)

    selected_agent = None

    if agent_matches:
        potential_agent = agent_matches[0]

        if potential_agent in AVAILABLE_AGENTS:
            selected_agent = potential_agent
        else:
            st.error(
                f"Unknown agent '@{potential_agent}'. Available agents: {', '.join([f'@{k}' for k in AVAILABLE_AGENTS.keys()])}"
            )
            st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Process with selected agent
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # Convert history to LangChain messages
                lc_history = []

                for m in st.session_state.messages[-6:]:
                    if m["role"] == "user":
                        lc_history.append(HumanMessage(content=m["content"]))
                    else:
                        lc_history.append(AIMessage(content=m["content"]))

                print(lc_history)  # TODO: remove

                state = {
                    "messages": lc_history + [HumanMessage(content=user_input)],
                    "selected_agent": selected_agent,
                }

                from backend import chatbot_invoke

                new_state = chatbot_invoke(state)

                ai_msg = new_state["messages"][-1].content if new_state.get("messages") else "No response generated."

                output = ai_msg

            except Exception as e:
                output = f"Error: {e}"

            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
