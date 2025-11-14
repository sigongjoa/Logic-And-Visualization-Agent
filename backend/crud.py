from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, UTC, timedelta
from typing import Optional, List
import uuid
import logging
from . import kakao_sender
import requests
from fastapi import HTTPException
import json
import os
from .fish_speech_adapter import FishSpeechAdapter # Import FishSpeechAdapter

logger = logging.getLogger(__name__)

# Placeholder for external LLM API configuration
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/generate") # Ollama API endpoint
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama2") # Default Ollama model

# Initialize FishSpeechAdapter globally
fish_speech_adapter = FishSpeechAdapter()

# Load LLM simulation configuration
LLM_SIM_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "llm_sim_config.json")
llm_sim_configs = []
try:
    with open(LLM_SIM_CONFIG_PATH, "r", encoding="utf-8") as f:
        llm_sim_configs = json.load(f)
except FileNotFoundError:
    logger.warning(f"LLM simulation config file not found at {LLM_SIM_CONFIG_PATH}. Using default simulations.")
except json.JSONDecodeError:
    logger.error(f"Error decoding LLM simulation config file at {LLM_SIM_CONFIG_PATH}. Using default simulations.")

# Load Manim simulation configuration
MANIM_SIM_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "manim_sim_config.json")
manim_sim_configs = []
try:
    with open(MANIM_SIM_CONFIG_PATH, "r", encoding="utf-8") as f:
        manim_sim_configs = json.load(f)
except FileNotFoundError:
    logger.warning(f"Manim simulation config file not found at {MANIM_SIM_CONFIG_PATH}. Using default simulations.")
except json.JSONDecodeError:
    logger.error(f"Error decoding Manim simulation config file at {MANIM_SIM_CONFIG_PATH}. Using default simulations.")

def call_external_llm_for_analysis(db: Session, problem_text: str) -> dict:
    """
    Calls a local Ollama LLM to analyze the problem text and return
    identified concept, logical path, and 4-axis vector data in JSON format.
    """
    headers = {"Content-Type": "application/json"} # No API key for local Ollama
    
    # Construct a detailed prompt for Ollama to get structured output
    prompt = f"""
You are an expert AI assistant for Project ATLAS, specializing in analyzing math problems and student capabilities.
Your task is to analyze the given math problem and provide a structured JSON output.

Here's what you need to provide:
1.  `concept_id`: Identify the SINGLE MOST RELEVANT concept ID from the provided list of `Available Concept IDs`. It is crucial to select an ID that directly relates to the core mathematical concept required to solve the problem. If the problem involves multiple concepts, choose the most foundational or primary one. If no perfect match, select the closest general concept.
2.  `logical_path_text`: Provide a concise, step-by-step logical explanation or solution path for the problem. This should be clear enough for a student to understand the reasoning.
3.  `vector_data`: Estimate the student's 4-axis capability model scores (0-100) based on the nature of this specific problem. Consider which axes are most challenged or demonstrated by solving this problem.
    -   `axis1_geo`: Geometric reasoning (spatial/shape recognition)
    -   `axis1_alg`: Algebraic manipulation (symbol/equation handling)
    -   `axis1_ana`: Analytical reasoning (function/change inference)
    -   `axis2_opt`: Optimization (finding efficient solutions)
    -   `axis2_piv`: Pivoting (flexibility in switching solution approaches)
    -   `axis2_dia`: Self-diagnosis (ability to identify own errors)
    -   `axis3_con`: Conceptual knowledge (understanding definitions)
    -   `axis3_pro`: Procedural knowledge (applying formulas/steps)
    -   `axis3_ret`: Retrieval speed (speed of recalling facts/methods)
    -   `axis4_acc`: Calculation accuracy (precision in computation)
    -   `axis4_gri`: Difficulty tolerance (persistence with challenging problems)

Math Problem: "{problem_text}"

Available Concept IDs (from ConceptsLibrary):
{', '.join([c.concept_id for c in db.query(models.ConceptsLibrary).all()])}

Your output MUST be a valid JSON object, formatted exactly as shown in the example below. Do NOT include any other text or markdown outside the JSON.

Example JSON Output:
```json
{{
    "concept_id": "C-HCOM-004",
    "logical_path_text": "To solve this quadratic equation, first identify the coefficients a, b, and c. Then, apply the quadratic formula x = [-b ± sqrt(b^2 - 4ac)] / 2a. Finally, simplify the results to find the two possible values for x.",
    "vector_data": {{
        "axis1_geo": 40, "axis1_alg": 85, "axis1_ana": 60,
        "axis2_opt": 70, "axis2_piv": 60, "axis2_dia": 75,
        "axis3_con": 80, "axis3_pro": 85, "axis3_ret": 70,
        "axis4_acc": 90, "axis4_gri": 80
    }}
}}
```
"""

    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json" # Request JSON format from Ollama
    }
    
    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=120) # Increased timeout for LLM
        response.raise_for_status() # Raise an exception for HTTP errors

        ollama_response = response.json()
        
        # Ollama's /api/generate returns a stream of responses, even with stream=False,
        # it might return a single object with 'response' field containing the actual JSON string.
        # Or, if format="json" is fully supported, it might return the JSON directly.
        # We need to handle both cases.
        
        raw_llm_output = ollama_response.get("response", ollama_response)
        
        # Try to parse the response as JSON
        try:
            llm_analysis_data = json.loads(raw_llm_output)
        except json.JSONDecodeError:
            logger.error(f"Ollama response was not valid JSON: {raw_llm_output}")
            raise HTTPException(status_code=500, detail="Ollama did not return valid JSON.")

        llm_concept_id = llm_analysis_data.get("concept_id")
        logical_path_text = llm_analysis_data.get("logical_path_text")
        vector_data = llm_analysis_data.get("vector_data")

        if not llm_concept_id or not logical_path_text or not vector_data:
            logger.error(f"Ollama response missing required fields: {llm_analysis_data}")
            raise HTTPException(status_code=500, detail="Ollama response missing required fields.")

        concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_id == llm_concept_id).first()
        
        if not concept:
            logger.warning(f"Ollama suggested concept_id '{llm_concept_id}' not found in ConceptsLibrary. Attempting fallback.")
            # Fallback: try to find concept based on problem_text keywords if LLM didn't provide a valid one
            if "이차방정식" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "이차방정식").first()
            elif "피타고라스" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "피타고라스의 정리").first()
            elif "소인수분해" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "소인수분해").first()
            elif "일차함수" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "일차함수와 그래프").first()
            elif "삼각비" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "삼각비").first()
            elif "경우의 수" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "경우의 수").first()
            
            if not concept:
                concept = db.query(models.ConceptsLibrary).first() # Get any concept as a last resort

        if not concept:
            raise HTTPException(status_code=500, detail="LLM analysis failed to identify a concept and no fallback found.")

        concept_id = concept.concept_id
        
        # For V1, manim_data_path is directly from ConceptsLibrary
        manim_data_path = concept.manim_data_path if concept.manim_data_path else "https://www.youtube.com/watch?v=default_manim_video"
        
        # Ensure scores are within 0-100
        for axis in vector_data:
            vector_data[axis] = max(0, min(100, vector_data[axis]))

        return {
            "concept_id": concept_id,
            "logical_path_text": logical_path_text,
            "manim_data_path": manim_data_path,
            "vector_data": vector_data
        }

    except requests.exceptions.Timeout:
        logger.error(f"Ollama API request timed out after 120 seconds for problem: {problem_text[:50]}...")
        raise HTTPException(status_code=504, detail="Ollama API request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Ollama API: {e} for problem: {problem_text[:50]}...")
        raise HTTPException(status_code=503, detail=f"Failed to connect to Ollama service: {e}")
    except Exception as e:
        logger.error(f"Error processing Ollama response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Ollama response: {e}")

def process_submission(db: Session, student_id: str, problem_text: str):
    # 1. Call external LLM for analysis
    llm_analysis_result = call_external_llm_for_analysis(db, problem_text)

    concept_id = llm_analysis_result["concept_id"]
    logical_path_text = llm_analysis_result["logical_path_text"]
    manim_data_path = llm_analysis_result["manim_data_path"]
    vector_data = llm_analysis_result["vector_data"]

    submission_id = f"sub_{uuid.uuid4().hex[:8]}" # Define submission_id here

    audio_explanation_url = None
    try:
        # For V1, we synthesize speech and simulate storing it to get a URL
        # In a real scenario, this would involve uploading to cloud storage
        audio_data = fish_speech_adapter.synthesize_speech(logical_path_text)
        # Simulate a URL for the generated audio
        audio_explanation_url = f"https://audio.example.com/{uuid.uuid4().hex}.wav"
        logger.info(f"Simulated audio generation for submission {submission_id}. Audio URL: {audio_explanation_url}")
    except HTTPException as e:
        logger.error(f"Failed to synthesize speech for submission {submission_id}: {e.detail}")
        audio_explanation_url = "https://audio.example.com/error.wav" # Fallback URL
    except Exception as e:
        logger.error(f"An unexpected error occurred during speech synthesis for submission {submission_id}: {e}")
        audio_explanation_url = "https://audio.example.com/error.wav" # Fallback URL

    # 2. Create a new submission record
    db_submission = models.Submission(
        submission_id=submission_id,
        student_id=student_id,
        problem_text=problem_text,
        submitted_at=datetime.now(UTC),
        concept_id=concept_id,
        logical_path_text=logical_path_text,
        status="COMPLETE",
        manim_data_path=manim_data_path,
        audio_explanation_url=audio_explanation_url, # Store the audio URL
    )
    db.add(db_submission)
    db.flush() # Use flush to get submission_id before commit

    # 3. Create an assessment and vector history
    assessment_schema = schemas.AssessmentCreate(
        student_id=student_id,
        assessment_type="llm_analysis",
        source_ref_id=submission_id,
        notes="Generated from LLM analysis of submission",
        vector_data=vector_data,
    )
    db_assessment, db_vector = create_assessment_and_vector(db, assessment_schema)

    # 4. Update or create StudentMastery
    # Calculate new mastery score based on LLM's vector_data for conceptual and procedural knowledge
    # For V1, a simple average of axis3_con and axis3_pro can be used.
    new_mastery_score = int((vector_data["axis3_con"] + vector_data["axis3_pro"]) / 2)
    new_mastery_score = max(0, min(100, new_mastery_score)) # Ensure score is within 0-100

    db_mastery = get_student_mastery(db, student_id, concept_id)
    if db_mastery:
        # Update existing mastery record
        db_mastery.mastery_score = new_mastery_score
        db_mastery.status = "IN_PROGRESS" # Or "MASTERED" if score is high enough
        db_mastery.last_updated = datetime.now(UTC)
        db.add(db_mastery)
    else:
        # Create a new mastery record
        mastery_schema = schemas.StudentMastery(
            student_id=student_id,
            concept_id=concept_id,
            mastery_score=new_mastery_score,
            status="IN_PROGRESS",
        )
        create_student_mastery(db, mastery_schema)

    db.commit()
    db.refresh(db_submission)

    return db_submission, manim_data_path


# Helper function to get a student
def get_student(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

# Helper function to get a coach
def get_coach(db: Session, coach_id: str):
    return db.query(models.Coach).filter(models.Coach.coach_id == coach_id).first()

def get_students_by_coach(db: Session, coach_id: str) -> List[models.Student]:
    coach = get_coach(db, coach_id)
    if coach:
        return coach.students
    return []

# Helper function to get a parent
def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.parent_id == parent_id).first()

# Helper function to get an assessment
def get_assessment(db: Session, assessment_id: str):
    return db.query(models.Assessment).filter(models.Assessment.assessment_id == assessment_id).first()

# Helper function to get a submission
def get_submission(db: Session, submission_id: str):
    return db.query(models.Submission).filter(models.Submission.submission_id == submission_id).first()

def get_submissions_by_coach(db: Session, coach_id: str, status: Optional[str] = None) -> List[models.Submission]:
    coach = get_coach(db, coach_id)
    if not coach:
        return []
    
    student_ids = [student.student_id for student in coach.students]
    if not student_ids:
        return []
        
    query = db.query(models.Submission).filter(models.Submission.student_id.in_(student_ids))
    
    if status:
        query = query.filter(models.Submission.status == status)
        
    return query.order_by(models.Submission.submitted_at.desc()).all()

# Helper function to get a concept
def get_concept(db: Session, concept_id: str):
    return db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_id == concept_id).first()

# Helper function to get a weekly report
def get_report(db: Session, report_id: int):
    return db.query(models.WeeklyReport).filter(models.WeeklyReport.report_id == report_id).first()

# Student Mastery
def create_student_mastery(db: Session, mastery: schemas.StudentMastery):
    db_mastery = models.StudentMastery(
        student_id=mastery.student_id,
        concept_id=mastery.concept_id,
        mastery_score=mastery.mastery_score,
        status=mastery.status,
        last_updated=datetime.now(UTC), # Explicitly set last_updated
    )
    db.add(db_mastery)
    db.commit()
    db.refresh(db_mastery)
    return db_mastery

def get_student_mastery(db: Session, student_id: str, concept_id: str):
    return db.query(models.StudentMastery).filter(
        models.StudentMastery.student_id == student_id,
        models.StudentMastery.concept_id == concept_id,
    ).first()

def update_student_mastery(db: Session, student_id: str, concept_id: str, mastery_score: int, status: str):
    db_mastery = get_student_mastery(db, student_id, concept_id)
    if db_mastery:
        db_mastery.mastery_score = mastery_score
        db_mastery.status = status
        db_mastery.last_updated = datetime.now(UTC)
        db.commit()
        db.refresh(db_mastery)
    return db_mastery

# Student CRUD operations
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(student_id=student.student_id, student_name=student.student_name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Coach CRUD operations
def create_coach(db: Session, coach: schemas.CoachCreate):
    db_coach = models.Coach(coach_id=coach.coach_id, coach_name=coach.coach_name)
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach

# Parent CRUD operations
def create_parent(db: Session, parent: schemas.ParentCreate):
    db_parent = models.Parent(parent_name=parent.parent_name, kakao_user_id=parent.kakao_user_id)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

# Assessment and Vector History
def create_assessment_and_vector(db: Session, assessment: schemas.AssessmentCreate):
    assessment_id = f"asmt_{uuid.uuid4().hex[:8]}"
    db_assessment = models.Assessment(
        assessment_id=assessment_id,
        student_id=assessment.student_id,
        assessment_type=assessment.assessment_type,
        source_ref_id=assessment.source_ref_id,
        notes=assessment.notes,
    )
    db.add(db_assessment)
    db.flush() # Use flush to get assessment_id before commit

    vector_id = f"vec_{uuid.uuid4().hex[:8]}"
    db_vector = models.StudentVectorHistory( # Corrected here
        vector_id=vector_id,
        assessment_id=assessment_id,
        student_id=assessment.student_id,
        axis1_geo=assessment.vector_data["axis1_geo"],
        axis1_alg=assessment.vector_data["axis1_alg"],
        axis1_ana=assessment.vector_data["axis1_ana"],
        axis2_opt=assessment.vector_data["axis2_opt"],
        axis2_piv=assessment.vector_data["axis2_piv"],
        axis2_dia=assessment.vector_data["axis2_dia"],
        axis3_con=assessment.vector_data["axis3_con"],
        axis3_pro=assessment.vector_data["axis3_pro"],
        axis3_ret=assessment.vector_data["axis3_ret"],
        axis4_acc=assessment.vector_data["axis4_acc"],
        axis4_gri=assessment.vector_data["axis4_gri"],
    )
    db.add(db_vector)
    db.commit()
    db.refresh(db_assessment)
    db.refresh(db_vector)
    return db_assessment, db_vector

def get_latest_vector_for_student(db: Session, student_id: str) -> Optional[models.StudentVectorHistory]:
    return db.query(models.StudentVectorHistory).filter( # Corrected here
        models.StudentVectorHistory.student_id == student_id
    ).order_by(models.StudentVectorHistory.created_at.desc()).first()

def get_vector_history_by_student(db: Session, student_id: str) -> List[models.StudentVectorHistory]:
    return db.query(models.StudentVectorHistory).filter( # Corrected here
        models.StudentVectorHistory.student_id == student_id
    ).order_by(models.StudentVectorHistory.created_at.asc()).all()

# Coach Memo
def create_coach_memo(db: Session, memo: schemas.CoachMemoCreate):
    db_memo = models.CoachMemo(
        coach_id=memo.coach_id,
        student_id=memo.student_id,
        memo_text=memo.memo_text,
    )
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

def get_coach_memos(db: Session, student_id: Optional[str] = None, coach_id: Optional[str] = None) -> List[models.CoachMemo]:
    query = db.query(models.CoachMemo)
    if student_id:
        query = query.filter(models.CoachMemo.student_id == student_id)
    if coach_id:
        query = query.filter(models.CoachMemo.coach_id == coach_id)
    return query.order_by(models.CoachMemo.created_at.desc()).all()

# LLM Log and Feedback
def create_llm_log_feedback(
    db: Session,
    feedback: schemas.LLMFeedback,
    source_submission_id: Optional[str],
    decision: str,
    model_version: str,
):
    db_llm_log = models.LLMLog(
        source_submission_id=source_submission_id,
        decision=decision,
        model_version=model_version,
        coach_feedback=feedback.coach_feedback,
        reason_code=feedback.reason_code,
    )
    db.add(db_llm_log)
    db.commit()
    db.refresh(db_llm_log)
    return db_llm_log

def update_llm_log_feedback(
    db: Session,
    log_id: int,
    coach_feedback: str,
    reason_code: Optional[str] = None,
):
    db_llm_log = db.query(models.LLMLog).filter(models.LLMLog.log_id == log_id).first()
    if db_llm_log:
        db_llm_log.coach_feedback = coach_feedback
        db_llm_log.reason_code = reason_code
        db.commit()
        db.refresh(db_llm_log)
    return db_llm_log

# Reports
def get_report_drafts(db: Session) -> List[models.WeeklyReport]:
    return db.query(models.WeeklyReport).filter(models.WeeklyReport.status == "DRAFT").all()

def finalize_report(db: Session, report_id: int, coach_comment: str):
    db_report = get_report(db, report_id)
    if db_report:
        db_report.coach_comment = coach_comment
        db_report.status = "FINALIZED"
        db_report.finalized_at = datetime.now(UTC)
        db.commit()
        db.refresh(db_report)
    return db_report

def send_report(db: Session, report_id: int):
    db_report = get_report(db=db, report_id=report_id)
    if db_report:
        # Get student and parent information
        student = db.query(models.Student).filter(models.Student.student_id == db_report.student_id).first()
        if not student:
            logger.warning(f"Student with ID {db_report.student_id} not found for report {report_id}")
            return None

        parent_association = db.query(models.student_parent_association).filter(
            models.student_parent_association.c.student_id == student.student_id
        ).first()
        if not parent_association:
            logger.warning(f"No parent associated with student {student.student_id} for report {report_id}")
            return None
        
        parent = db.query(models.Parent).filter(models.Parent.parent_id == parent_association.parent_id).first()
        if not parent or not parent.kakao_user_id:
            logger.warning(f"Parent or Kakao user ID not found for student {student.student_id} for report {report_id}")
            return None

        # Construct the message
        message_title = f"주간 학습 리포트 - {student.student_name} ({db_report.period_start.strftime('%Y-%m-%d')} ~ {db_report.period_end.strftime('%Y-%m-%d')})"
        message_body = f"AI 요약:\n{db_report.ai_summary}\n\n코치 코멘트:\n{db_report.coach_comment or '코치 코멘트가 없습니다.'}"
        full_message = f"{message_title}\n\n{message_body}"

        # Simulate sending KakaoTalk message
        kakao_sender.send_kakao_message(parent.kakao_user_id, full_message)

        db_report.status = "SENT"
        db.commit()
        db.refresh(db_report)
    return db_report

# Anki Card CRUD operations
def create_anki_card(
    db: Session,
    student_id: str,
    llm_log_id: int,
    question: str,
    answer: str,
    interval_days: int = 0,
    ease_factor: float = 2.5,
    repetitions: int = 0,
):
    next_review_date = datetime.now(UTC).date() + timedelta(days=1) # Initial next review date
    db_anki_card = models.AnkiCard(
        student_id=student_id,
        llm_log_id=llm_log_id,
        question=question,
        answer=answer,
        next_review_date=next_review_date,
        interval_days=interval_days,
        ease_factor=ease_factor,
        repetitions=repetitions,
    )
    db.add(db_anki_card)
    db.commit()
    db.refresh(db_anki_card)
    return db_anki_card

def update_anki_card_sm2(db: Session, card_id: int, grade: int):
    logger.debug(f"SM2 Update: card_id={card_id}, grade={grade}")
    db_anki_card = db.query(models.AnkiCard).filter(models.AnkiCard.card_id == card_id).first()
    if db_anki_card:
        logger.debug(f"SM2 Update: Before - repetitions={db_anki_card.repetitions}, ease_factor={db_anki_card.ease_factor}, interval_days={db_anki_card.interval_days}, next_review_date={db_anki_card.next_review_date}")
        repetitions, ease_factor, interval_days, next_review_date = calculate_sm2_params(
            db_anki_card.repetitions,
            db_anki_card.ease_factor,
            db_anki_card.interval_days,
            grade,
        )
        db_anki_card.repetitions = repetitions
        db_anki_card.ease_factor = ease_factor
        db_anki_card.interval_days = interval_days
        db_anki_card.next_review_date = next_review_date
        db.commit()
        db.refresh(db_anki_card)
        logger.debug(f"SM2 Update: After - repetitions={db_anki_card.repetitions}, ease_factor={db_anki_card.ease_factor}, interval_days={db_anki_card.interval_days}, next_review_date={db_anki_card.next_review_date}")
    return db_anki_card

def get_anki_cards_by_student(db: Session, student_id: str) -> List[models.AnkiCard]:
    return db.query(models.AnkiCard).filter(models.AnkiCard.student_id == student_id).all()

def get_student_mastery_by_student(db: Session, student_id: str) -> List[models.StudentMastery]:
    return db.query(models.StudentMastery).filter(models.StudentMastery.student_id == student_id).all()

def calculate_sm2_params(
    repetitions: int, ease_factor: float, interval_days: int, grade: int
) -> tuple[int, float, int, datetime.date]: # Changed return type to datetime.date
    """
    Calculates the new SM2 parameters based on the feedback grade.
    Grade should be an integer from 0 to 5.
    0-2: Incorrect response
    3: Correct response, but with difficulty
    4: Correct response, with hesitation
    5: Perfect recall
    """
    logger.debug(f"SM2: Input - repetitions={repetitions}, ease_factor={ease_factor}, interval_days={interval_days}, grade={grade}")

    if grade >= 3:
        # Successful recall
        repetitions += 1
        ease_factor = ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        if ease_factor < 1.3:
            ease_factor = 1.3

        if repetitions == 1:
            interval_days = 1
        elif repetitions == 2:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        
        if interval_days < 1: # Ensure interval is at least 1 day
            interval_days = 1

    else:
        # Failed recall
        repetitions = 0
        interval_days = 1
    
    next_review_date = datetime.now(UTC).date() + timedelta(days=interval_days)
    logger.debug(f"SM2: Output - repetitions={repetitions}, ease_factor={ease_factor}, interval_days={interval_days}, next_review_date={next_review_date}")

    return repetitions, ease_factor, interval_days, next_review_date

def call_external_manim_agent(concept_id: str, logical_path_text: str) -> str:
    """
    Calls an external Manim Agent API to generate a video based on the concept and logical path.
    Returns a URL to the generated Manim video.
    """
    headers = {"X-API-Key": MANIM_AGENT_API_KEY, "Content-Type": "application/json"}
    payload = {
        "concept_id": concept_id,
        "logical_path_text": logical_path_text
    }

    try:
        response = requests.post(MANIM_AGENT_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        manim_response = response.json()
        return manim_response.get("video_url", "https://youtube.com/watch?v=default_manim_video")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling external Manim Agent API: {e}")
        # Fallback to a default video or raise an exception
        return "https://youtube.com/watch?v=error_manim_video"
    except Exception as e:
        logger.error(f"Error processing Manim Agent response: {e}")
        return "https://youtube.com/watch?v=error_manim_video"


