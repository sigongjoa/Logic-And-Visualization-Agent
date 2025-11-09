from sqlalchemy.orm import Session
from . import models, schemas

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
