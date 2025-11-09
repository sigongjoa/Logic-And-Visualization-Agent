from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pacer.backend import schemas, crud
from pacer.backend.main import get_db
import uuid

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)

@router.post("/", response_model=schemas.SubmissionResult, status_code=201)
def create_submission(
    submission: schemas.SubmissionCreate, db: Session = Depends(get_db)
):
    submission_id = f"sub_{uuid.uuid4()}"

    # In a real V1 scenario, this would call the Meta-RAG engine.
    # For now, we'll mock the response as per the V1 "뼈대(skeleton)" strategy.
    logical_path_text = "This is a mock logical path from Meta-RAG."
    concept_id = "C-001" # Mock concept ID
    manim_content_url = "https://youtube.com/watch?v=mock_video"

    db_submission = crud.create_submission(
        db=db,
        submission=submission,
        submission_id=submission_id,
        logical_path_text=logical_path_text,
        concept_id=concept_id,
    )

    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        concept_id=db_submission.concept_id,
        manim_content_url=manim_content_url, # This comes from a lookup, mocked here
    )
