"""
Workflow Orchestrator for College Application Strategy Generation

This module provides a robust workflow orchestrator that ensures tools are called
in the correct order with proper error handling, data validation, and logging.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, Field, ValidationError

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from prompt_templates.narratives import create_narrative_angles_prompt_template
from prompt_templates.Future_plan import create_future_plan_prompt_template
from prompt_templates.Activity import create_activity_list_generator_prompt_template
from prompt_templates.Main_essay import create_main_essay_ideas_prompt_template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowStep(Enum):
    """Enumeration of workflow steps for tracking progress"""
    NARRATIVE_ANGLES = "narrative_angles"
    FUTURE_PLAN = "future_plan"
    ACTIVITY_LIST = "activity_list"
    MAIN_ESSAY_IDEAS = "main_essay_ideas"


class WorkflowStatus(Enum):
    """Enumeration of workflow statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATED = "validated"


@dataclass
class WorkflowResult:
    """Container for workflow step results"""
    step: WorkflowStep
    status: WorkflowStatus
    data: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None
    validation_errors: Optional[List[str]] = None


class StudentProfileValidator(BaseModel):
    """Pydantic model for validating student profile data"""
    name: str = Field(..., description="Student's full name")
    gender: str = Field(..., description="Student's gender")
    birth_country: str = Field(..., description="Student's birth country")
    cultural_background: List[str] = Field(..., description="Cultural background elements")
    academic: Dict[str, Any] = Field(..., description="Academic information")
    activities: List[Dict[str, Any]] = Field(..., description="Student activities")
    future_plans: List[str] = Field(..., description="Future plans")

    class Config:
        extra = "allow"  # Allow additional fields


class NarrativeAnglesValidator(BaseModel):
    """Pydantic model for validating narrative angles output"""
    narrative_angles: List[Dict[str, Any]] = Field(..., description="List of narrative angles")

    @classmethod
    def validate_narrative_angle(cls, angle: Dict[str, Any]) -> List[str]:
        """Validate individual narrative angle structure"""
        errors = []
        required_fields = ["title", "positioning", "essay_concept", "anchor_scene", 
                          "unexpected_twist", "signature_initiative", "natural_major_fit"]
        
        for field in required_fields:
            if field not in angle:
                errors.append(f"Missing required field: {field}")
        
        if "signature_initiative" in angle:
            initiative = angle["signature_initiative"]
            if not isinstance(initiative, dict):
                errors.append("signature_initiative must be a dictionary")
            elif "name" not in initiative or "description" not in initiative:
                errors.append("signature_initiative must contain 'name' and 'description'")
        
        return errors


class MainEssayIdeasValidator(BaseModel):
    """Pydantic model for validating main essay ideas output"""
    main_essay_ideas: List[Dict[str, Any]] = Field(..., description="List of main essay ideas")

    @classmethod
    def validate_essay_idea(cls, idea: Dict[str, Any]) -> List[str]:
        """Validate individual essay idea structure"""
        errors = []
        required_fields = ["title", "theme", "hook", "challenge", "journey", 
                          "growth", "impact", "future_connection", "key_activities", 
                          "unique_angle", "authenticity_factors"]
        
        for field in required_fields:
            if field not in idea:
                errors.append(f"Missing required field: {field}")
        
        return errors


class WorkflowOrchestrator:
    """
    Main orchestrator class that manages the complete workflow execution
    with proper error handling, validation, and logging.
    """
    
    def __init__(self, llm: Optional[AzureChatOpenAI] = None):
        """
        Initialize the workflow orchestrator.
        
        Args:
            llm: LangChain LLM instance. If None, creates a new AzureChatOpenAI instance.
        """
        self.llm = llm or AzureChatOpenAI(deployment_name="gpt-4o")
        self.results: Dict[WorkflowStep, WorkflowResult] = {}
        self.execution_log: List[Dict[str, Any]] = []
        
        # Initialize prompt templates
        self.narrative_prompt = create_narrative_angles_prompt_template()
        self.future_plan_prompt = create_future_plan_prompt_template()
        self.activity_prompt = create_activity_list_generator_prompt_template()
        self.main_essay_prompt = create_main_essay_ideas_prompt_template()
        
        logger.info("WorkflowOrchestrator initialized successfully")
    
    def validate_student_profile(self, student_profile: Dict[str, Any]) -> List[str]:
        """
        Validate student profile data structure.
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        try:
            StudentProfileValidator(**student_profile)
            return []
        except ValidationError as e:
            errors = [f"Validation error: {err['msg']} at field {err['loc']}" 
                     for err in e.errors()]
            logger.error(f"Student profile validation failed: {errors}")
            return errors
    
    def execute_with_retry(self, func, *args, max_retries: int = 3, **kwargs) -> Any:
        """
        Execute a function with retry logic and error handling.
        
        Args:
            func: Function to execute
            *args: Function arguments
            max_retries: Maximum number of retry attempts
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or error information
        """
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(f"Function {func.__name__} executed successfully in {execution_time:.2f}s")
                return result, execution_time, None
                
            except Exception as e:
                error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
                logger.warning(error_msg)
                
                if attempt == max_retries - 1:
                    logger.error(f"All retry attempts failed for {func.__name__}")
                    return None, 0, str(e)
                
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None, 0, "Max retries exceeded"
    
    def generate_narrative_angles(self, student_profile: Dict[str, Any]) -> WorkflowResult:
        """
        Generate narrative angles with validation and error handling.
        
        Args:
            student_profile: Validated student profile
            
        Returns:
            WorkflowResult containing the result
        """
        logger.info("Starting narrative angles generation")
        
        def _generate_narratives():
            chain = self.narrative_prompt | self.llm | StrOutputParser()
            raw_result = chain.invoke({"student_profile": json.dumps(student_profile)})
            
            # Try to parse JSON
            try:
                parsed_result = json.loads(raw_result)
                return parsed_result
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {e}")
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except:
                        pass
                raise ValueError(f"Invalid JSON response: {raw_result[:200]}...")
        
        result, execution_time, error = self.execute_with_retry(_generate_narratives)
        
        if error:
            return WorkflowResult(
                step=WorkflowStep.NARRATIVE_ANGLES,
                status=WorkflowStatus.FAILED,
                data=None,
                error=error,
                execution_time=execution_time
            )
        
        # Validate the result
        validation_errors = []
        try:
            validator = NarrativeAnglesValidator(**result)
            for angle in validator.narrative_angles:
                angle_errors = NarrativeAnglesValidator.validate_narrative_angle(angle)
                validation_errors.extend(angle_errors)
        except ValidationError as e:
            validation_errors.append(f"Structure validation failed: {e}")
        
        status = WorkflowStatus.VALIDATED if not validation_errors else WorkflowStatus.FAILED
        
        workflow_result = WorkflowResult(
            step=WorkflowStep.NARRATIVE_ANGLES,
            status=status,
            data=result,
            error=None,
            execution_time=execution_time,
            validation_errors=validation_errors
        )
        
        self.results[WorkflowStep.NARRATIVE_ANGLES] = workflow_result
        logger.info(f"Narrative angles generation completed with status: {status}")
        
        return workflow_result
    
    def generate_future_plan(self, student_profile: Dict[str, Any], 
                           narrative_result: WorkflowResult) -> WorkflowResult:
        """
        Generate future plan with validation and error handling.
        
        Args:
            student_profile: Student profile
            narrative_result: Previous narrative angles result
            
        Returns:
            WorkflowResult containing the result
        """
        logger.info("Starting future plan generation")
        
        if narrative_result.status != WorkflowStatus.VALIDATED:
            return WorkflowResult(
                step=WorkflowStep.FUTURE_PLAN,
                status=WorkflowStatus.FAILED,
                data=None,
                error="Cannot generate future plan without valid narrative angles"
            )
        
        # Use the first narrative angle
        narrative_angle = narrative_result.data["narrative_angles"][0]
        
        def _generate_future_plan():
            chain = self.future_plan_prompt | self.llm | StrOutputParser()
            return chain.invoke({
                "user_profile": json.dumps(student_profile),
                "narrative": narrative_angle
            })
        
        result, execution_time, error = self.execute_with_retry(_generate_future_plan)
        
        if error:
            return WorkflowResult(
                step=WorkflowStep.FUTURE_PLAN,
                status=WorkflowStatus.FAILED,
                data=None,
                error=error,
                execution_time=execution_time
            )
        
        # Validate future plan (should be a string under 100 characters)
        validation_errors = []
        if not isinstance(result, str):
            validation_errors.append("Future plan must be a string")
        elif len(result) > 100:
            validation_errors.append(f"Future plan exceeds 100 characters: {len(result)}")
        elif not result.strip():
            validation_errors.append("Future plan cannot be empty")
        
        status = WorkflowStatus.VALIDATED if not validation_errors else WorkflowStatus.FAILED
        
        workflow_result = WorkflowResult(
            step=WorkflowStep.FUTURE_PLAN,
            status=status,
            data=result,
            error=None,
            execution_time=execution_time,
            validation_errors=validation_errors
        )
        
        self.results[WorkflowStep.FUTURE_PLAN] = workflow_result
        logger.info(f"Future plan generation completed with status: {status}")
        
        return workflow_result
    
    def generate_activity_list(self, student_profile: Dict[str, Any],
                             narrative_result: WorkflowResult,
                             future_plan_result: WorkflowResult) -> WorkflowResult:
        """
        Generate activity list with validation and error handling.
        
        Args:
            student_profile: Student profile
            narrative_result: Narrative angles result
            future_plan_result: Future plan result
            
        Returns:
            WorkflowResult containing the result
        """
        logger.info("Starting activity list generation")
        
        if narrative_result.status != WorkflowStatus.VALIDATED:
            return WorkflowResult(
                step=WorkflowStep.ACTIVITY_LIST,
                status=WorkflowStatus.FAILED,
                data=None,
                error="Cannot generate activity list without valid narrative angles"
            )
        
        if future_plan_result.status != WorkflowStatus.VALIDATED:
            return WorkflowResult(
                step=WorkflowStep.ACTIVITY_LIST,
                status=WorkflowStatus.FAILED,
                data=None,
                error="Cannot generate activity list without valid future plan"
            )
        
        narrative_angle = narrative_result.data["narrative_angles"][0]
        future_plan = future_plan_result.data
        
        def _generate_activity_list():
            chain = self.activity_prompt | self.llm | StrOutputParser()
            return chain.invoke({
                "user_profile": json.dumps(student_profile),
                "narrative": narrative_angle,
                "future_plan": future_plan
            })
        
        result, execution_time, error = self.execute_with_retry(_generate_activity_list)
        
        if error:
            return WorkflowResult(
                step=WorkflowStep.ACTIVITY_LIST,
                status=WorkflowStatus.FAILED,
                data=None,
                error=error,
                execution_time=execution_time
            )
        
        # Basic validation for activity list
        validation_errors = []
        if not isinstance(result, str):
            validation_errors.append("Activity list must be a string")
        elif not result.strip():
            validation_errors.append("Activity list cannot be empty")
        
        status = WorkflowStatus.VALIDATED if not validation_errors else WorkflowStatus.FAILED
        
        workflow_result = WorkflowResult(
            step=WorkflowStep.ACTIVITY_LIST,
            status=status,
            data=result,
            error=None,
            execution_time=execution_time,
            validation_errors=validation_errors
        )
        
        self.results[WorkflowStep.ACTIVITY_LIST] = workflow_result
        logger.info(f"Activity list generation completed with status: {status}")
        
        return workflow_result
    
    def generate_main_essay_ideas(self, student_profile: Dict[str, Any],
                                narrative_result: WorkflowResult,
                                future_plan_result: WorkflowResult,
                                activity_result: WorkflowResult) -> WorkflowResult:
        """
        Generate main essay ideas with validation and error handling.
        
        Args:
            student_profile: Student profile
            narrative_result: Narrative angles result
            future_plan_result: Future plan result
            activity_result: Activity list result
            
        Returns:
            WorkflowResult containing the result
        """
        logger.info("Starting main essay ideas generation")
        
        # Validate all previous steps
        for step, result in [(WorkflowStep.NARRATIVE_ANGLES, narrative_result),
                            (WorkflowStep.FUTURE_PLAN, future_plan_result),
                            (WorkflowStep.ACTIVITY_LIST, activity_result)]:
            if result.status != WorkflowStatus.VALIDATED:
                return WorkflowResult(
                    step=WorkflowStep.MAIN_ESSAY_IDEAS,
                    status=WorkflowStatus.FAILED,
                    data=None,
                    error=f"Cannot generate main essay ideas without valid {step.value}"
                )
        
        narrative_angle = narrative_result.data["narrative_angles"][0]
        future_plan = future_plan_result.data
        activity_list = activity_result.data
        
        def _generate_main_essay_ideas():
            chain = self.main_essay_prompt | self.llm | StrOutputParser()
            raw_result = chain.invoke({
                "user_profile": json.dumps(student_profile),
                "narrative": narrative_angle,
                "future_plan": future_plan,
                "activity_result": activity_list
            })
            
            # Try to parse JSON
            try:
                parsed_result = json.loads(raw_result)
                return parsed_result
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed: {e}")
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except:
                        pass
                raise ValueError(f"Invalid JSON response: {raw_result[:200]}...")
        
        result, execution_time, error = self.execute_with_retry(_generate_main_essay_ideas)
        
        if error:
            return WorkflowResult(
                step=WorkflowStep.MAIN_ESSAY_IDEAS,
                status=WorkflowStatus.FAILED,
                data=None,
                error=error,
                execution_time=execution_time
            )
        
        # Validate the result
        validation_errors = []
        try:
            validator = MainEssayIdeasValidator(**result)
            for idea in validator.main_essay_ideas:
                idea_errors = MainEssayIdeasValidator.validate_essay_idea(idea)
                validation_errors.extend(idea_errors)
        except ValidationError as e:
            validation_errors.append(f"Structure validation failed: {e}")
        
        status = WorkflowStatus.VALIDATED if not validation_errors else WorkflowStatus.FAILED
        
        workflow_result = WorkflowResult(
            step=WorkflowStep.MAIN_ESSAY_IDEAS,
            status=status,
            data=result,
            error=None,
            execution_time=execution_time,
            validation_errors=validation_errors
        )
        
        self.results[WorkflowStep.MAIN_ESSAY_IDEAS] = workflow_result
        logger.info(f"Main essay ideas generation completed with status: {status}")
        
        return workflow_result
    
    def execute_complete_workflow(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete workflow in the correct order with full error handling.
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            Dictionary containing all results and workflow status
        """
        logger.info("Starting complete workflow execution")
        start_time = time.time()
        
        # Step 1: Validate student profile
        profile_errors = self.validate_student_profile(student_profile)
        if profile_errors:
            return {
                "status": "failed",
                "error": "Student profile validation failed",
                "validation_errors": profile_errors,
                "results": {}
            }
        
        # Step 2: Generate narrative angles
        narrative_result = self.generate_narrative_angles(student_profile)
        if narrative_result.status != WorkflowStatus.VALIDATED:
            return {
                "status": "failed",
                "error": "Narrative angles generation failed",
                "step": "narrative_angles",
                "details": narrative_result.error,
                "results": self.results
            }
        
        # Step 3: Generate future plan
        future_plan_result = self.generate_future_plan(student_profile, narrative_result)
        if future_plan_result.status != WorkflowStatus.VALIDATED:
            return {
                "status": "failed",
                "error": "Future plan generation failed",
                "step": "future_plan",
                "details": future_plan_result.error,
                "results": self.results
            }
        
        # Step 4: Generate activity list
        activity_result = self.generate_activity_list(student_profile, narrative_result, future_plan_result)
        if activity_result.status != WorkflowStatus.VALIDATED:
            return {
                "status": "failed",
                "error": "Activity list generation failed",
                "step": "activity_list",
                "details": activity_result.error,
                "results": self.results
            }
        
        # Step 5: Generate main essay ideas
        main_essay_result = self.generate_main_essay_ideas(student_profile, narrative_result, 
                                                          future_plan_result, activity_result)
        if main_essay_result.status != WorkflowStatus.VALIDATED:
            return {
                "status": "failed",
                "error": "Main essay ideas generation failed",
                "step": "main_essay_ideas",
                "details": main_essay_result.error,
                "results": self.results
            }
        
        total_time = time.time() - start_time
        
        # Compile final results
        final_results = {
            "status": "completed",
            "total_execution_time": total_time,
            "results": {
                "narrative_angles": narrative_result.data,
                "future_plan": future_plan_result.data,
                "activity_list": activity_result.data,
                "main_essay_ideas": main_essay_result.data
            },
            "execution_details": {
                step.value: {
                    "status": result.status.value,
                    "execution_time": result.execution_time,
                    "validation_errors": result.validation_errors
                }
                for step, result in self.results.items()
            }
        }
        
        logger.info(f"Complete workflow executed successfully in {total_time:.2f}s")
        return final_results
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the workflow execution.
        
        Returns:
            Dictionary containing workflow summary
        """
        total_time = sum(result.execution_time or 0 for result in self.results.values())
        successful_steps = sum(1 for result in self.results.values() 
                             if result.status == WorkflowStatus.VALIDATED)
        failed_steps = sum(1 for result in self.results.values() 
                          if result.status == WorkflowStatus.FAILED)
        
        return {
            "total_steps": len(self.results),
            "successful_steps": successful_steps,
            "failed_steps": failed_steps,
            "total_execution_time": total_time,
            "step_details": {
                step.value: {
                    "status": result.status.value,
                    "execution_time": result.execution_time,
                    "has_errors": bool(result.error or result.validation_errors)
                }
                for step, result in self.results.items()
            }
        }


# Convenience function for easy usage
def generate_application_strategy(student_profile: Dict[str, Any], 
                                llm: Optional[AzureChatOpenAI] = None) -> Dict[str, Any]:
    """
    Convenience function to generate complete application strategy.
    
    Args:
        student_profile: Student profile dictionary
        llm: Optional LLM instance
        
    Returns:
        Complete application strategy results
    """
    orchestrator = WorkflowOrchestrator(llm)
    return orchestrator.execute_complete_workflow(student_profile)
