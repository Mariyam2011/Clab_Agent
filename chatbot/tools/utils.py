from typing import List
from langchain_core.messages import BaseMessage


def create_conversation_context(recent_messages: List[BaseMessage]) -> str:
    conversation_context = ""

    if recent_messages:
        conversation_context = "\n\nRECENT CONVERSATION CONTEXT:\n"

        for msg in recent_messages[-6:]:
            role = "User" if hasattr(msg, "type") and msg.type == "human" else "Assistant"

            conversation_context += f"{role}: {msg.content}\n"

    return conversation_context
