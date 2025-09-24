from typing import List, Optional, Dict, Any
import json
from langchain_core.messages import BaseMessage


def create_conversation_context(recent_messages: List[BaseMessage]) -> str:
    conversation_context = ""

    if recent_messages and len(recent_messages) > 0:
        conversation_context = "RECENT CONVERSATION CONTEXT:\n"

        for msg in recent_messages:
            role = "User" if hasattr(msg, "type") and msg.type == "human" else "Assistant"

            conversation_context += f"{role}: {msg.content}\n"

        conversation_context += (
            "\n\nEXTRACT ANY IMPORTANT INFORMATION FROM THE CONVERSATION THAT IS RELEVANT TO THE CURRENT TASK.\n\n"
        )

    return conversation_context


def create_user_context(user_profile: Optional[Dict[str, Any]]) -> str:
    user_profile_context = ""

    if user_profile is not None:
        user_profile_context = f"\nSTUDENT PROFILE & CONTEXT: {json.dumps(user_profile, ensure_ascii=False)}"

    return user_profile_context


def _strip_fences_and_labels(s: str) -> str:
    s = s.strip()

    if s.startswith("```"):
        s = s[3:]

        first_newline = s.find("\n")

        if first_newline != -1:
            s = s[first_newline + 1 :]

        if s.rstrip().endswith("```"):
            s = s.rstrip()[:-3]

    if s.lower().startswith("json "):
        s = s[5:]

    return s.strip()
