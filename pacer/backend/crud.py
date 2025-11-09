from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, UTC

def create_assessment_and_vector(db: Session, assessment: schemas.AssessmentCreate, assessment_id: str, vector_id: str):
    # 1. Create the Assessment object
    db_assessment = models.Assessment(
        assessment_id=assessment_id,
        student_id=assessment.student_id,
        assessment_type=assessment.assessment_type,
        source_ref_id=assessment.source_ref_id,
        notes=assessment.notes,
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)

    # 2. Create the StudentVectorHistory object
    db_vector_history = models.StudentVectorHistory(
        vector_id=vector_id,
        assessment_id=assessment_id,
        student_id=assessment.student_id,
        **assessment.vector_data,
    )
    db.add(db_vector_history)
    db.commit()
    db.refresh(db_vector_history)

    return db_vector_history

def create_submission(db: Session, submission: schemas.SubmissionCreate, submission_id: str, logical_path_text: str, concept_id: str):
    db_submission = models.Submission(
        submission_id=submission_id,
        student_id=submission.student_id,
        problem_text=submission.problem_text,
        status="COMPLETE",  # Set status to COMPLETE as per mock logic
        logical_path_text=logical_path_text,
        concept_id=concept_id,
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_report_drafts(db: Session):
    return db.query(models.WeeklyReport).filter(models.WeeklyReport.status == "DRAFT").all()

def get_report(db: Session, report_id: int):
    return db.query(models.WeeklyReport).filter(models.WeeklyReport.report_id == report_id).first()

def finalize_report(db: Session, report_id: int, comment: str):
    db_report = get_report(db=db, report_id=report_id)
    if db_report:
        db_report.status = "FINALIZED"
        db_report.coach_comment = comment
        db_report.finalized_at = datetime.now(UTC)
        db.commit()
        db.refresh(db_report)
    return db_report

def send_report(db: Session, report_id: int):
    db_report = get_report(db=db, report_id=report_id)
    if db_report:
        db_report.status = "SENT"
        db.commit()
        db.refresh(db_report)
    return db_report

def get_vector_history_by_student(db: Session, student_id: str):
    return db.query(models.StudentVectorHistory).filter(models.StudentVectorHistory.student_id == student_id).all()

def update_student_mastery(db: Session, student_id: str, concept_id: str, mastery_score: int, status: str):
    db_mastery = db.query(models.StudentMastery).filter_by(
        student_id=student_id, concept_id=concept_id
    ).first()

    if db_mastery:
        db_mastery.mastery_score = mastery_score
        db_mastery.status = status
        db_mastery.last_updated = datetime.now(UTC)
    else:
        db_mastery = models.StudentMastery(
            student_id=student_id,
            concept_id=concept_id,
            mastery_score=mastery_score,
            status=status,
            last_updated=datetime.now(UTC),
        )
        db.add(db_mastery)
    db.commit()
    db.refresh(db_mastery)
    return db_mastery

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
