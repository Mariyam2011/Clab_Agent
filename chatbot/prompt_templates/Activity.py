import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_activity_list_generator_prompt_template() -> ChatPromptTemplate:
    prompt = """
    You are acting as a U.S. college admissions counselor. 
    Critically think: what kind of activity list would make this student stand out at the world’s most selective universities? 
    Activities should feel authentic, unique, and interview-defensible, while highlighting hidden impact and originality.

    USER PROFILE: {user_profile}
    NARRATIVE ANALYSIS: {narrative}
    FUTURE PLAN: {future_plan}

    TASK: Transform existing activities into standout accomplishments AND invent three new signature activities that are bold, unexpected, and deeply connected to the student’s mission.

    FORMAT REQUIREMENTS:
    - Position: [50 characters max]
    - Organization: [100 characters max]
    - Description: [150 characters max]

    CRITICAL AUTHENTICITY WARNING:
    - Enhance by revealing hidden impact, creative methods, and overlooked beneficiaries.
    - Do NOT inflate numbers or invent fictional elements. Every claim must be defensible in an interview.
    - Admissions officers can immediately detect exaggeration.

    EXCELLENCE PATTERNS FROM ACCEPTED STUDENTS:
    - "Led soil conservation in rural villages in Layyah; reforestation near flood prone farmlands; advised 30+ farmers; built alert app"
    - "Designed & developed floating hydroponic system; used sensors; created app to monitor; aided 68 female farmers in rural areas"
    - "Member U19 national team; won 5 gold & 2 silver medals; mentored younger players; selected for exclusive Int'l camp"

    FOR EACH ACTIVITY PROVIDE:
    1. **Enhanced Version of Existing:**
       - Current: [What they currently have]
       - Elevated: [Deeper framing, hidden impact, measurable results]
       - Position: [Action verb + unique role, ≤50 chars]
       - Organization: [Memorable org name, ≤100 chars]
       - Description: [What was done + specific numbers + unique method + who benefited, ≤150 chars]

    2. **Three New Signature Activities:**
       - Must target an overlooked community
       - Must use an unexpected method
       - Must create measurable change
       - Must include a memorable initiative name

    COUNSELOR’S EXPECTATION:
    - Every activity should demonstrate leadership, creativity, and impact.
    - Activities must progress logically (early involvement → initiative → leadership → scaling).
    - Each line should make an admissions officer pause and think: “Only this student could have done this.”

    OUTPUT: Only return the activities in the exact format required, no extra commentary.
    """
    return ChatPromptTemplate.from_template(prompt)

# def create_activity_list_generator_prompt_template() -> ChatPromptTemplate:
#     prompt = """
#     Generate 6–8 authentic, high-impact activities for this student, based on their profile, narrative analysis, and future plan.

#     USER PROFILE: {user_profile}
#     NARRATIVE ANALYSIS: {narrative}
#     FUTURE PLAN: {future_plan}

#     FORMAT (strict):
#     Position (≤50 chars)
#     Organization (≤100 chars)
#     When (grade/year)
#     Hours/Wk, Weeks/Yr
#     Status (Continue/Completed)
#     Key Details: Specific actions, measurable impact, unique method, who benefited (≤200 chars)

#     REQUIREMENTS:
#     - Activities must directly connect to future plan and strengths
#     - Show progression from early involvement to leadership
#     - Include concrete numbers or measurable results
#     - Be authentic and interview-defensible
#     - Mix academic, extracurricular, and community initiatives
#     - Use action verbs and concise language

#     OUTPUT: Only return the list in the exact format above, no explanations.
#     """
#     return ChatPromptTemplate.from_template(prompt)

