from fastapi import APIRouter, Depends, HTTPException
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

    # V1 Meta-RAG simulation: Search for a concept keyword in the problem text.
    # This is a very basic implementation.
    # A more advanced version would parse the text more intelligently.
    found_concept = crud.search_concept_by_keyword(db, submission.problem_text)

    if not found_concept:
        # If no concept is found, we can't proceed with the V1 logic.
        # In a real scenario, we might have a fallback or error state.
        # For now, we'll raise an error.
        raise HTTPException(status_code=404, detail="No relevant concept found for the submission.")

    concept_id = found_concept.concept_id
    logical_path_text = f"This problem appears to be related to the concept: '{found_concept.concept_name}'."
    manim_content_url = found_concept.manim_data_path or "https://youtube.com/watch?v=default_video"

    db_submission = crud.create_submission(
        db=db,
        submission=submission,
        submission_id=submission_id,
        logical_path_text=logical_path_text,
        concept_id=concept_id,
    )

    # Update StudentMastery based on the submission
    # For V1, we'll mock the mastery score and status update
    mock_mastery_score = 70
    mock_mastery_status = "MASTERED"
    crud.update_student_mastery(
        db=db,
        student_id=submission.student_id,
        concept_id=concept_id,
        mastery_score=mock_mastery_score,
        status=mock_mastery_status,
    )

    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        concept_id=db_submission.concept_id,
        manim_content_url=manim_content_url,
    )
