"""
Tools module for the college application chatbot.
Provides organized tools for narrative generation, web search, routing, and formatting.
"""

# Import all tools to make them available when importing from tools
from .narrative_tools import (
    generate_narrative_angles,
    generate_future_plan,
    generate_activity_list,
    generate_main_essay_ideas,
)

from .web_tools import (
    web_search,
    rewrite_search_query,
    perform_web_search,
    should_use_web,
)

from .routing_tools import (
    route_tool_call,
)

from .formatting_tools import (
    json_to_markdown_llm,
)

from .utilities import (
    strip_fences_and_labels,
    coerce_json_best_effort,
)

# List of all available tools for easy access
__all__ = [
    # Narrative tools
    "generate_narrative_angles",
    "generate_future_plan",
    "generate_activity_list",
    "generate_main_essay_ideas",
    # Web tools
    "web_search",
    "rewrite_search_query",
    "perform_web_search",
    "should_use_web",
    # Routing tools
    "route_tool_call",
    # Formatting tools
    "json_to_markdown_llm",
    # Utilities
    "strip_fences_and_labels",
    "coerce_json_best_effort",
]
