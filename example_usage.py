"""
Example usage of the Workflow Orchestrator

This script demonstrates how to use the workflow orchestrator to generate
a complete college application strategy with proper error handling and validation.
"""

import json
import logging

from workflow_orchestrator import WorkflowOrchestrator, generate_application_strategy

# Configure logging to see the workflow progress
logging.basicConfig(level=logging.INFO)

# Sample student profile (you can replace this with your actual data)
DUMMY_USER_DATA = {
    "name": "Sarah Johnson",
    "gender": "Female",
    "birth_country": "United States",
    "cultural_background": [
        "American",
        "first-generation college student",
        "rural upbringing",
        "STEM-focused",
        "environmental advocate",
    ],
    "academic": {
        "gpa": "3.95",
        "school_type": "Public High School",
        "test_scores": {"SAT": "1450", "ACT": "32"},
    },
    "activities": [
        {
            "position": "President",
            "category": "Academic",
            "description": "Led environmental science club, organized community clean-up events, coordinated with local government on sustainability initiatives",
        },
        {
            "position": "Team Captain",
            "category": "Athletics",
            "description": "Varsity soccer team captain, led team to state championship, organized team community service projects",
        },
        {
            "position": "Volunteer",
            "category": "Community Service",
            "description": "Tutored underprivileged students in math and science, developed curriculum for after-school program",
        },
        {
            "position": "Research Assistant",
            "category": "Research",
            "description": "Assisted professor in environmental impact study, analyzed data on renewable energy adoption in rural communities",
        },
    ],
    "future_plans": [
        "Study environmental engineering",
        "Work on renewable energy solutions",
        "Masters degree",
        "Start a non-profit focused on rural sustainability",
    ],
}


def example_1_simple_usage():
    """Example 1: Simple usage with the convenience function"""
    print("=== Example 1: Simple Usage ===")
    
    # Use the convenience function
    result = generate_application_strategy(DUMMY_USER_DATA)
    
    # Check if successful
    if result["status"] == "completed":
        print("✅ Workflow completed successfully!")
        print(f"Total execution time: {result['total_execution_time']:.2f} seconds")
        
        # Access individual results
        narratives = result["results"]["narrative_angles"]
        future_plan = result["results"]["future_plan"]
        activities = result["results"]["activity_list"]
        main_essay_ideas = result["results"]["main_essay_ideas"]
        
        print(f"\n📝 Generated {len(narratives['narrative_angles'])} narrative angles")
        print(f"🎯 Future plan: {future_plan}")
        print(f"📋 Activity list generated")
        print(f"✍️ Generated {len(main_essay_ideas['main_essay_ideas'])} main essay ideas")
        
        # Show execution details
        print("\n📊 Execution Details:")
        for step, details in result["execution_details"].items():
            print(f"  {step}: {details['status']} ({details['execution_time']:.2f}s)")
            
    else:
        print("❌ Workflow failed!")
        print(f"Error: {result['error']}")
        if 'step' in result:
            print(f"Failed at step: {result['step']}")
        if 'details' in result:
            print(f"Details: {result['details']}")

