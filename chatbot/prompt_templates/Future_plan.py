import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_future_plan_prompt_template() -> ChatPromptTemplate:
    prompt = """
    You are acting as a college admissions counselor crafting a future plan statement that will make an application stand out. 
    Think critically: What kind of response would *truly* impress an admissions officer? What feels unique, bold, and out-of-the-box, 
    yet still authentic to the student’s profile and narrative?

    GOAL: Create ONE powerful 100-character future plan line that makes the student’s mission unmistakable.

    FORMULA: [Role/Identity] + [Unique Approach] + [Specific Impact]

    EXCELLENT EXAMPLES (unexpected, specific, memorable):
    - Environmental scientist using tech to empower female farmers
    - Policy leader & artist, challenging gender bias through creative advocacy
    - Computational linguist using AI to decode scripts & empower women globally
    - Sustainability engineer, promoting green technology to combat urban pollution
    - To lead biotech innovations that empower underserved communities

    COUNSELOR’S EXPECTATION:
    - Not vague or cliché (“help people,” “make the world better”).
    - Must fuse different aspects of the student’s identity/skills in a surprising way.
    - Should name a specific community or beneficiary (not just “the world”).
    - Must feel like something ONLY this student could say — rooted in their profile and narrative.

    RULES:
    1. Max 100 characters (including spaces).
    2. Use strong, active verbs (designing, reimagining, challenging, decoding).
    3. Must connect clearly to USER PROFILE and NARRATIVE ANALYSIS.
    4. Output ONLY the single future plan line — no commentary, no extra text.

    USER PROFILE: {user_profile}

    NARRATIVE ANALYSIS: {narrative}

    Generate the future plan line:
    """
    return ChatPromptTemplate.from_template(prompt)

# def create_future_plan_prompt_template() -> ChatPromptTemplate:
#     prompt = """
#     You are an elite U.S. college admissions strategist. 
#     Based on the given USER PROFILE and NARRATIVE ANALYSIS, generate ONE powerful 100-character future plan statement. 

#     FORMULA: [Role/Identity] + [Unique Approach] + [Specific Impact]

#     EXCELLENT EXAMPLES:
#     - Environmental scientist using tech to empower female farmers
#     - Policy leader & artist, challenging gender bias through creative advocacy
#     - Computational linguist using AI to decode scripts & empower women globally
#     - Sustainability engineer, promoting green technology to combat urban pollution
#     - To lead biotech innovations that empower underserved communities

#     RULES:
#     1. Must be MAX 100 characters (including spaces).
#     2. Must feature an unexpected combination of fields/skills.
#     3. Must name a specific beneficiary or community.
#     4. Must use strong, active verbs (avoid generic words like "help" or "make a difference").
#     5. Must clearly connect to the user's profile and narrative.
#     6. Output ONLY the single future plan line — no explanations, no extra text.

#     USER PROFILE: {user_profile}

#     NARRATIVE ANALYSIS: {narrative}

#     Generate the future plan line:
#     """
#     return ChatPromptTemplate.from_template(prompt)


# future_plan_prompt_template = create_future_plan_prompt_template()


