from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, UTC
from typing import Optional, List
import uuid
import logging
from . import kakao_sender # Import the kakao_sender

logger = logging.getLogger(__name__)

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

    # Determine concept_id based on problem_text (simulated LLM analysis)
    concept = search_concept_by_keyword(db, submission.problem_text)
    concept_id = concept.concept_id if concept else None

    if concept_id:
        # Check if StudentMastery entry exists
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
    # For now, using dummy vector data. In a real scenario, this would come from LLM analysis.
    dummy_vector_data = {
        "axis1_geo": 50, "axis1_alg": 50, "axis1_ana": 50,
        "axis2_opt": 50, "axis2_piv": 50, "axis2_dia": 50,
        "axis3_con": 50, "axis3_pro": 50, "axis3_ret": 50,
        "axis4_acc": 55, "axis4_gri": 50, # Changed axis4_acc to 55
    }
    assessment_schema = schemas.AssessmentCreate(
        student_id=submission.student_id,
        assessment_type="AI_ANALYSIS",
        source_ref_id=submission_id,
        notes=f"Vector generated from submission {submission_id}",
        vector_data=dummy_vector_data
    )
    create_assessment_and_vector(db, assessment_schema)

    return db_submission

def update_submission_status(db: Session, submission_id: str, status: str):
    db_submission = get_submission(db, submission_id)
    if db_submission:
        db_submission.status = status
        db.commit()
        db.refresh(db_submission)
    return db_submission

def search_concept_by_keyword(db: Session, keyword: str):
    # This is a very basic simulation. In a real scenario, this would involve
    # more sophisticated text search or an actual RAG system.
    return db.query(models.ConceptsLibrary).filter(
        models.ConceptsLibrary.concept_name.ilike(f"%{keyword}%")
    ).first()

# Curriculum and Concepts
def create_curriculum(db: Session, curriculum: schemas.Curriculum):
    db_curriculum = models.Curriculum(
        curriculum_id=curriculum.curriculum_id,
        curriculum_name=curriculum.curriculum_name,
        description=curriculum.description,
    )
    db.add(db_curriculum)
    db.commit()
    db.refresh(db_curriculum)
    return db_curriculum

def create_concept(db: Session, concept: schemas.Concept):
    db_concept = models.ConceptsLibrary(
        concept_id=concept.concept_id,
        curriculum_id=concept.curriculum_id,
        concept_name=concept.concept_name,
        description=concept.description,
    )
    db.add(db_concept)
    db.commit()
    db.refresh(db_concept)
    return db_concept

def create_concept_relation(db: Session, relation: schemas.ConceptRelation):
    db_relation = models.ConceptRelation(
        from_concept_id=relation.from_concept_id,
        to_concept_id=relation.to_concept_id,
        relation_type=relation.relation_type,
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

# Student Mastery
def create_student_mastery(db: Session, mastery: schemas.StudentMastery):
    db_mastery = models.StudentMastery(
        student_id=mastery.student_id,
        concept_id=mastery.concept_id,
        mastery_score=mastery.mastery_score,
        status=mastery.status,
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
