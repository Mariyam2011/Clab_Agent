"""
Utility functions for tools module.
Contains helper functions for JSON processing, string manipulation, and common operations.
"""

import ast
import json
from typing import Any


def strip_fences_and_labels(s: str) -> str:
    """Strip code fences and language labels from strings."""
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


def coerce_json_best_effort(raw: Any) -> Any:
    """Attempt to parse JSON from various string formats with fallbacks."""
    if not isinstance(raw, str):
        return raw
    s = strip_fences_and_labels(raw)
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(s[start : end + 1])
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        return None
