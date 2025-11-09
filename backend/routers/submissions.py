from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, crud
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
    db_submission = crud.create_submission(db=db, submission=submission)
    
    # The crud.create_submission now handles Meta-RAG simulation and model updates.
    # It also populates logical_path_text and concept_id in db_submission.
    # We need to retrieve manim_content_url from the concept identified by crud.create_submission.
    
    concept = crud.get_concept(db, db_submission.concept_id)
    manim_content_url = concept.manim_data_path if concept else "https://youtube.com/watch?v=default_video"

    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        concept_id=db_submission.concept_id,
        manim_content_url=manim_content_url,
    )
