from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, crud, models
from backend.main import get_db
import uuid

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)

@router.post("/", response_model=schemas.SubmissionResult, status_code=201)
def create_submission(
    submission: schemas.SubmissionCreate, db: Session = Depends(get_db)
):
    db_submission, manim_content_url = crud.process_submission(
        db=db,
        student_id=submission.student_id,
        problem_text=submission.problem_text,
    )

    if not db_submission:
        raise HTTPException(status_code=400, detail="Submission could not be created.")

    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        concept_id=db_submission.concept_id,
        manim_content_url=db_submission.manim_data_path,
        audio_explanation_url=db_submission.audio_explanation_url, # Include audio URL
        submitted_at=db_submission.submitted_at,
    )

@router.get("/{submission_id}", response_model=schemas.SubmissionResult)
def get_submission_by_id(submission_id: str, db: Session = Depends(get_db)):
    db_submission = crud.get_submission(db, submission_id=submission_id)
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        problem_text=db_submission.problem_text,
        concept_id=db_submission.concept_id,
        manim_content_url=db_submission.manim_data_path,
        audio_explanation_url=db_submission.audio_explanation_url, # Include audio URL
        submitted_at=db_submission.submitted_at,
    )

@router.post("/{submission_id}/review", response_model=schemas.SubmissionReviewResponse)
def review_submission(
    submission_id: str,
    review: schemas.SubmissionReviewCreate,
    db: Session = Depends(get_db),
):
    # This will be implemented in the next step
    db_review = crud.add_coach_review_to_submission(
        db=db, submission_id=submission_id, review=review
    )
    if not db_review:
        raise HTTPException(status_code=404, detail="Submission not found or review could not be added.")
    return db_review