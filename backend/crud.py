from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, UTC, timedelta # Added timedelta
from typing import Optional, List
import uuid
import logging
from . import kakao_sender # Import the kakao_sender
import requests # Added requests
from fastapi import HTTPException # Moved import to top

logger = logging.getLogger(__name__)

# Placeholder for external LLM API configuration
LLM_API_URL = "http://localhost:8001/llm-analysis" # Example URL
LLM_API_KEY = "your_llm_api_key" # Replace with actual API key or environment variable

# Placeholder for external Manim Agent API configuration
MANIM_AGENT_API_URL = "http://localhost:8002/manim-generate" # Example URL
MANIM_AGENT_API_KEY = "your_manim_api_key" # Replace with actual API key or environment variable

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
        # In a real scenario, you would make an actual HTTP request here.
        # For now, we'll simulate the Manim Agent's response.
        # response = requests.post(MANIM_AGENT_API_URL, headers=headers, json=payload)
        # response.raise_for_status() # Raise an exception for HTTP errors
        # manim_response = response.json()
        # return manim_response.get("video_url", "https://youtube.com/watch?v=default_manim_video")

        # Simulated Manim Agent response
        if "이차함수" in concept_id:
            return "https://youtube.com/watch?v=quadratic_function_manim"
        elif "피타고라스" in concept_id:
            return "https://youtube.com/watch?v=pythagorean_theorem_manim"
        else:
            return "https://youtube.com/watch?v=default_manim_video"

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling external Manim Agent API: {e}")
        # Fallback to a default video or raise an exception
        return "https://youtube.com/watch?v=error_manim_video"
    except Exception as e:
        logger.error(f"Error processing Manim Agent response: {e}")
        return "https://youtube.com/watch?v=error_manim_video"

# Helper function to get a student
def get_student(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

# Helper function to get a coach
def get_coach(db: Session, coach_id: str):
    return db.query(models.Coach).filter(models.Coach.coach_id == coach_id).first()

# Helper function to get a parent
def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.parent_id == parent_id).first()

# Helper function to get an assessment
def get_assessment(db: Session, assessment_id: str):
    return db.query(models.Assessment).filter(models.Assessment.assessment_id == assessment_id).first()

# Helper function to get a submission
def get_submission(db: Session, submission_id: str):
    return db.query(models.Submission).filter(models.Submission.submission_id == submission_id).first()

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
    next_review_date: datetime,
    interval_days: int = 0,
    ease_factor: float = 2.5,
    repetitions: int = 0,
):
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

# Submissions
def create_submission(db: Session, submission: schemas.SubmissionCreate):
    submission_id = f"sub_{uuid.uuid4().hex[:8]}"
    db_submission = models.Submission(
        submission_id=submission_id,
        student_id=submission.student_id,
        problem_text=submission.problem_text,
        status="PENDING", # Initial status
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    # Call external LLM for analysis
    llm_analysis_result = call_external_llm_for_analysis(db, submission.problem_text)
    
    concept_id = llm_analysis_result["concept_id"]
    logical_path_text = llm_analysis_result["logical_path_text"]
    manim_data_path = llm_analysis_result["manim_data_path"]
    ai_vector_data = llm_analysis_result["vector_data"]

    # Assign logical_path_text and concept_id to db_submission
    db_submission.logical_path_text = logical_path_text
    db_submission.concept_id = concept_id
    db.commit() # Commit the changes to db_submission
    db.refresh(db_submission) # Refresh db_submission to reflect committed changes

    # Update StudentMastery based on the submission
    mastery_entry = get_student_mastery(db, submission.student_id, concept_id)
    if mastery_entry:
        # Update existing entry
        update_student_mastery(db, submission.student_id, concept_id, 70, "IN_PROGRESS")
    else:
        # Create new entry
        create_student_mastery(db, schemas.StudentMastery(
            student_id=submission.student_id,
            concept_id=concept_id,
            mastery_score=70, # Placeholder score
            status="IN_PROGRESS" # Placeholder status
        ))

    # Create a new vector history entry based on the submission
    assessment_schema = schemas.AssessmentCreate(
        student_id=submission.student_id,
        assessment_type="AI_ANALYSIS",
        source_ref_id=submission_id,
        notes=f"Vector generated from submission {submission_id}",
        vector_data=ai_vector_data # Use AI data from LLM analysis
    )
    db_assessment, db_vector = create_assessment_and_vector(db, assessment_schema)

    # Create LLMLog entry
    llm_log_feedback_schema = schemas.LLMFeedback(
        coach_feedback="", # No coach feedback at this stage
        reason_code=None,
    )
    db_llm_log = create_llm_log_feedback(
        db=db,
        feedback=llm_log_feedback_schema,
        source_submission_id=submission_id,
        decision="ANALYSIS_COMPLETE",
        model_version="V1_LLM_INTEGRATION", # Updated model version
    )

    # Create AnkiCard entry (V1 Simulation)
    anki_question = f"What is the key concept related to '{submission.problem_text}'?"
    anki_answer = f"The problem is primarily about '{concept_id}' and its logical path is: {logical_path_text}"
    
    # For V1, set next_review_date to tomorrow
    next_review_date = datetime.now(UTC) + timedelta(days=1)

    create_anki_card(
        db=db,
        student_id=submission.student_id,
        llm_log_id=db_llm_log.log_id,
        question=anki_question,
        answer=anki_answer,
        next_review_date=next_review_date,
    )

    return db_submission

def call_external_llm_for_analysis(db: Session, problem_text: str) -> dict:
    """
    Calls an external LLM API to analyze the problem text and return
    identified concept, logical path, and 4-axis vector data.
    """
    headers = {"X-API-Key": LLM_API_KEY, "Content-Type": "application/json"}
    payload = {"problem_text": problem_text}
    
    try:
        # In a real scenario, you would make an actual HTTP request here.
        # For now, we'll simulate the LLM's response.
        # response = requests.post(LLM_API_URL, headers=headers, json=payload)
        # response.raise_for_status() # Raise an exception for HTTP errors
        # llm_response = response.json()

        # Simulated LLM response for V1
        llm_response = {}
        if "이차함수" in problem_text:
            llm_response = {
                "concept_id": "C_이차함수",
                "logical_path_text": f"LLM analysis: The problem '{problem_text}' is about quadratic functions. Key steps involve identifying the vertex, roots, and graph properties.",
                "vector_data": {
                    "axis1_geo": 50, "axis1_alg": 65, "axis1_ana": 50,
                    "axis2_opt": 55, "axis2_piv": 50, "axis2_dia": 50,
                    "axis3_con": 60, "axis3_pro": 55, "axis3_ret": 50,
                    "axis4_acc": 60, "axis4_gri": 50,
                }
            }
        elif "피타고라스" in problem_text:
            llm_response = {
                "concept_id": "C_피타고라스",
                "logical_path_text": f"LLM analysis: The problem '{problem_text}' applies the Pythagorean theorem. Focus on identifying right triangles and side lengths.",
                "vector_data": {
                    "axis1_geo": 65, "axis1_alg": 50, "axis1_ana": 50,
                    "axis2_opt": 50, "axis2_piv": 55, "axis2_dia": 50,
                    "axis3_con": 55, "axis3_pro": 60, "axis3_ret": 50,
                    "axis4_acc": 50, "axis4_gri": 60,
                }
            }
        else:
            llm_response = {
                "concept_id": "C_기본개념", # Default concept
                "logical_path_text": f"LLM analysis: The problem '{problem_text}' involves basic mathematical concepts. Review fundamental principles.",
                "vector_data": {
                    "axis1_geo": 55, "axis1_alg": 55, "axis1_ana": 55,
                    "axis2_opt": 55, "axis2_piv": 55, "axis2_dia": 55,
                    "axis3_con": 55, "axis3_pro": 55, "axis3_ret": 55,
                    "axis4_acc": 55, "axis4_gri": 55,
                }
            }


        # In a real scenario, you would parse the LLM's response
        # to extract concept_id, logical_path_text, and vector_data.
        
        # Placeholder for LLM-identified concept (if LLM provides it)
        llm_concept_id = llm_response.get("concept_id")
        
        concept = None
        if llm_concept_id:
            concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_id == llm_concept_id).first()
        
        if not concept:
            # Fallback: try to find concept based on problem_text keywords if LLM didn't provide a valid one
            # This is similar to the old search_concept_by_keyword logic
            if "이차함수" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "이차함수").first()
            elif "피타고라스" in problem_text:
                concept = db.query(models.ConceptsLibrary).filter(models.ConceptsLibrary.concept_name == "피타고라스").first()
            # Add more keyword-based fallbacks or a default concept
            if not concept:
                # Default concept if nothing else matches
                concept = db.query(models.ConceptsLibrary).first() # Get any concept for now

        if not concept:
            raise HTTPException(status_code=500, detail="LLM analysis failed to identify a concept and no fallback found.")

        concept_id = concept.concept_id
        concept_name = concept.concept_name # Safely get concept_name
        logical_path_text = llm_response.get("logical_path_text", 
                                             f"LLM generated logical path for '{problem_text}' related to '{concept_name}'.")
        # Call external Manim Agent to get the video path
        manim_data_path = call_external_manim_agent(concept_id, logical_path_text)
        # Simulate 4-axis vector data from LLM response
        vector_data = llm_response.get("vector_data", {
            "axis1_geo": 55, "axis1_alg": 55, "axis1_ana": 55,
            "axis2_opt": 55, "axis2_piv": 55, "axis2_dia": 55,
            "axis3_con": 55, "axis3_pro": 55, "axis3_ret": 55,
            "axis4_acc": 55, "axis4_gri": 55,
        })
        
        # Ensure scores are within 0-100
        for axis in vector_data:
            vector_data[axis] = max(0, min(100, vector_data[axis]))

        return {
            "concept_id": concept_id,
            "logical_path_text": logical_path_text,
            "manim_data_path": manim_data_path,
            "vector_data": vector_data
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling external LLM API: {e}")
        raise HTTPException(status_code=503, detail=f"Failed to connect to LLM service: {e}")
    except Exception as e:
        logger.error(f"Error processing LLM response: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing LLM response: {e}")

# Submissions
def create_submission(db: Session, submission: schemas.SubmissionCreate):
    submission_id = f"sub_{uuid.uuid4().hex[:8]}"
    db_submission = models.Submission(
        submission_id=submission_id,
        student_id=submission.student_id,
        problem_text=submission.problem_text,
        status="PENDING", # Initial status
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    # Call external LLM for analysis
    llm_analysis_result = call_external_llm_for_analysis(db, submission.problem_text)
    
    concept_id = llm_analysis_result["concept_id"]
    logical_path_text = llm_analysis_result["logical_path_text"]
    manim_data_path = llm_analysis_result["manim_data_path"]
    ai_vector_data = llm_analysis_result["vector_data"]

    # Assign logical_path_text and concept_id to db_submission
    db_submission.logical_path_text = logical_path_text
    db_submission.concept_id = concept_id
    db.commit() # Commit the changes to db_submission
    db.refresh(db_submission) # Refresh db_submission to reflect committed changes

    # Update StudentMastery based on the submission
    mastery_entry = get_student_mastery(db, submission.student_id, concept_id)
    if mastery_entry:
        # Update existing entry
        update_student_mastery(db, submission.student_id, concept_id, 70, "IN_PROGRESS")
    else:
        # Create new entry
        create_student_mastery(db, schemas.StudentMastery(
            student_id=submission.student_id,
            concept_id=concept_id,
            mastery_score=70, # Placeholder score
            status="IN_PROGRESS" # Placeholder status
        ))

    # Create a new vector history entry based on the submission
    assessment_schema = schemas.AssessmentCreate(
        student_id=submission.student_id,
        assessment_type="AI_ANALYSIS",
        source_ref_id=submission_id,
        notes=f"Vector generated from submission {submission_id}",
        vector_data=ai_vector_data # Use AI data from LLM analysis
    )
    db_assessment, db_vector = create_assessment_and_vector(db, assessment_schema)

    # Create LLMLog entry
    llm_log_feedback_schema = schemas.LLMFeedback(
        coach_feedback="", # No coach feedback at this stage
        reason_code=None,
    )
    db_llm_log = create_llm_log_feedback(
        db=db,
        feedback=llm_log_feedback_schema,
        source_submission_id=submission_id,
        decision="ANALYSIS_COMPLETE",
        model_version="V1_LLM_INTEGRATION", # Updated model version
    )

    # Create AnkiCard entry (V1 Simulation)
    anki_question = f"What is the key concept related to '{submission.problem_text}'?"
    anki_answer = f"The problem is primarily about '{concept_id}' and its logical path is: {logical_path_text}"
    
    # For V1, set next_review_date to tomorrow
    next_review_date = datetime.now(UTC) + timedelta(days=1)

    create_anki_card(
        db=db,
        student_id=submission.student_id,
        llm_log_id=db_llm_log.log_id,
        question=anki_question,
        answer=anki_answer,
        next_review_date=next_review_date,
    )

    return db_submission
