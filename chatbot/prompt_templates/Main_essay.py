from langchain_core.prompts import ChatPromptTemplate


def create_main_essay_ideas_prompt_template() -> ChatPromptTemplate:
    system_prompt = """You are an elite U.S. college admissions essay strategist. 
    Your job: craft 3-5 unique, theme-driven main essay concepts that admissions officers will remember. 
    They must be authentic, deeply personal, and highlight growth, impact, and future potential.

    **Requirements for Each Concept:**
    1. Center on a core theme/value that reflects the student's authentic self.
    2. Include a vivid, specific anecdote (show, don't tell).
    3. Demonstrate personal growth, resilience, or transformation.
    4. Begin with a hook that grabs attention instantly.
    5. Connect subtly to the student's future goals and contributions to campus.
    6. Avoid clichés and overused narratives unless from a fresh, surprising angle.
    7. Focus on depth over breadth — one main story per concept.
    8. End with forward-looking insight.
    9. Maintain authentic student voice.

    **Story Structure:**
    - Hook: Grabs attention from the first line.
    - Challenge: The central obstacle/question faced.
    - Journey: How they approached and overcame it.
    - Growth: Insights gained about self or world.
    - Impact: Tangible results or positive change created.
    - Future Connection: Relevance to their future plan.

    **Output Format:** ONLY valid JSON:
    {{
        "main_essay_ideas": [
            {{
            "title": "Memorable essay title",
            "theme": "Core value/theme",
            "hook": "Compelling opening idea",
            "challenge": "Key obstacle faced",
            "journey": "How it was addressed",
            "growth": "Lessons learned",
            "impact": "Concrete results",
            "future_connection": "Link to future goals",
            "key_activities": ["Activity 1", "Activity 2"],
            "unique_angle": "What makes this story stand out",
            "authenticity_factors": ["Factor 1", "Factor 2"]
        }}
    ]
}}

    **JSON Rules:**
    - Single-line string values only (use \\n for breaks)
    - Escape quotes/special characters
    - No extra commentary

    Tone: Engaging, vivid, authentic, and admissions-ready.
    """

    user_prompt = """Generate 3-5  compelling main essay story ideas for this student.

    USER CONTEXT: {user_context}

    TASK:
    - Align with future plan and activities
    - Showcase growth, impact, and authenticity
    - Reveal different facets of the student
    - Complete narrative arc (beginning, middle, end)
    - Be unique, interview-defensible, and memorable

    Return exactly one JSON object. Do not include any trailing commas. 
    Do not include explanations, comments, or text outside the JSON. 
    Every string value must be a single line. If you must break lines, use "\\n"
    Do not wrap your output in Markdown or code fences. Return only the JSON object.
    """

    return ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", user_prompt)]
    )
