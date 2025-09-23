import os
import sys
import streamlit as st

from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

load_dotenv()


from langchain_core.messages import HumanMessage, AIMessage  # noqa: E402


st.set_page_config(page_title="Admissions Strategy Chatbot", page_icon="🎓")
st.title("Admissions Strategy Chatbot")

# Sidebar profile editor
st.sidebar.header("User Profile (JSON)")

# profile_text = st.sidebar.text_area(
#     "Edit profile JSON",
#     json.dumps(DEFAULT_PROFILE, indent=2, ensure_ascii=False),
#     height=420,
# )

tool_option = st.selectbox("Select tool:", ["Standard Strategy", "Complete Strategy"])

format_option = st.selectbox("Output formatting:", ["JSON", "Markdown (LLM)"])

force_web_search = st.sidebar.checkbox(
    "Force Web Search",
    value=False,
    help="Append a hint to trigger web search explicitly.",
)

rewrite_queries = st.sidebar.checkbox(
    "Rewrite query before web search",
    value=False,
    help="Use LLM to improve search queries.",
)

search_context = st.sidebar.text_input(
    "Query rewrite context (optional)", value="college admissions"
)

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
if user_input := st.chat_input(
    "Ask for narrative, future plan, activities, essay or complete strategy"
):
    # Append user message
    outgoing_text = user_input + (
        " search"
        if force_web_search and not user_input.lower().endswith("search")
        else ""
    )
    st.session_state.messages.append({"role": "user", "content": outgoing_text})
    with st.chat_message("user"):
        st.markdown(outgoing_text)

    # Parse profile JSON
    # try:
    #     user_profile = json.loads(profile_text)
    # except Exception as e:
    #     error_msg = f"Invalid profile JSON: {e}"
    #     st.session_state.messages.append({"role": "assistant", "content": error_msg})
    #     with st.chat_message("assistant"):
    #         st.error(error_msg)
    #     st.stop()

    # Persist rewrite settings into in-memory state for downstream tools
    st.session_state.memory["rewrite_queries"] = rewrite_queries
    if search_context:
        st.session_state.memory["search_context"] = search_context
    else:
        st.session_state.memory.pop("search_context", None)

    # Build state and call agent graph
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Convert history to LangChain messages
                lc_history = []
                for m in st.session_state.messages[-6:]:
                    if m["role"] == "user":
                        lc_history.append(HumanMessage(content=m["content"]))
                    else:
                        lc_history.append(AIMessage(content=m["content"]))

                # Build agent state
                state = {
                    "messages": lc_history + [HumanMessage(content=outgoing_text)],
                    "tool_option": "complete strategy"
                    if tool_option == "Complete Strategy"
                    else "standard strategy",
                    "format_option": format_option,
                    "memory": dict(st.session_state.memory),
                    "rewrite_queries": bool(rewrite_queries),
                    "search_context": search_context if search_context else None,
                }

                # Invoke one step
                from backend import chatbot, config  # Add import

                new_state = chatbot.invoke(
                    state, config=config
                )  # Fixed: actually call the chatbot

                # Extract assistant reply
                ai_msg = (
                    new_state["messages"][-1].content
                    if new_state.get("messages")
                    else "No response generated."  # Better error message
                )
                st.session_state.memory.update(new_state.get("memory", {}))
                output = ai_msg
            except Exception as e:
                output = f"Error: {e}"

            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})

            # Optionally render web context if tools populate it in memory
            web_ctx = st.session_state.memory.get("web_context")
            if web_ctx:
                with st.expander("Web sources used"):
                    for idx, item in enumerate(web_ctx, start=1):
                        title = item.get("title") or f"Result {idx}"
                        url = item.get("url") or ""
                        snippet = item.get("snippet") or ""
                        st.markdown(f"**{idx}. [{title}]({url})**\n\n{snippet}")
                meta = st.session_state.memory.get("web_meta") or {}
                if meta:
                    st.info(
                        f"Original query: {meta.get('original_query', '')}\n\n"
                        f"Final query: {meta.get('final_query', '')}\n\n"
                        f"Rewrite applied: {meta.get('rewrite_applied', False)}"
                    )
