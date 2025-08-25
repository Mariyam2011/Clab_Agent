import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_main_essay_ideas_prompt_template() -> ChatPromptTemplate:
    """
    Creates a concise, high-impact prompt template for generating main essay story ideas
    aligned with the student's future plan and activities.
    """
    system_prompt = """You are an elite U.S. college admissions essay strategist. 
    Your job: craft 3–5 unique, theme-driven main essay concepts that admissions officers will remember. 
    They must be authentic, deeply personal, and highlight growth, impact, and future potential.

    **Requirements for Each Concept:**
    1. Center on a core theme/value that reflects the student's authentic self.
    2. Include a vivid, specific anecdote (show, don’t tell).
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

    user_prompt = """Generate 3–5 compelling main essay story ideas for this student.

    USER PROFILE: {user_profile}
    NARRATIVE ANALYSIS: {narrative}
    FUTURE PLAN: {future_plan}
    ACTIVITY RESULT: {activity_result}

    TASK:
    - Align with future plan and activities
    - Showcase growth, impact, and authenticity
    - Reveal different facets of the student
    - Complete narrative arc (beginning, middle, end)
    - Be unique, interview-defensible, and memorable

    Output ONLY the valid JSON object.
    """
    return ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", user_prompt)]
    )

# def create_main_essay_ideas_prompt_template() -> ChatPromptTemplate:
#     system_prompt = """You are an expert US college admissions counselor with deep knowledge of what makes a personal statement stand out at selective universities. 

#     TASK: Based on the student's future plan and activities, generate 3–5 compelling and unique MAIN ESSAY STORY CONCEPTS for the Common App (or similar application) essay.

#     Each concept must:
#     1. Be theme-driven (centered around a personal value, passion, or defining trait).
#     2. Showcase the student's personal growth, resilience, or transformation.
#     3. Include a specific, vivid anecdote that "shows, not tells" the trait or lesson.
#     4. Use a hook-worthy opening idea to grab attention immediately.
#     5. Reflect authenticity — true to the student's voice and experience.
#     6. Subtly connect to the student's future goals and potential contributions to a university community.
#     7. Avoid clichés, generic sports/grades/travel essays unless told from a surprising and fresh angle.
#     8. End with a forward-looking insight or connection to the person they are becoming.
#     9. Ensure the story focuses on depth over breadth — one main narrative or theme per concept.

#     OUTPUT:You must output ONLY a valid JSON object in the following structure:
#     {{
#         "main_essay_ideas": [
#             {{
#                 "title": "Title/Theme",
#                 "hook": "One-sentence hook idea",
#                 "anecdote": "Core anecdote (2–3 sentences)",
#                 "growth": "Personal growth & insight",
#                 "connection": "Connection to future goals"
#             }},
#             ...
#         ]
#     }}
#     Output ONLY the valid JSON object, nothing else. Remember: no line breaks within string values
#     """

#     user_prompt = """INPUTS:

#     USER PROFILE: {user_profile}

#     NARRATIVE ANALYSIS: {narrative}
#     FUTURE PLAN: {future_plan}
#     ACTIVITY RESULT: {activity_result}"""

#     return ChatPromptTemplate.from_messages(
#         [("system", system_prompt), ("user", user_prompt)]
#     )

