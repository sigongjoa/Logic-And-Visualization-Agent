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
        manim_content_url=manim_content_url,
    )