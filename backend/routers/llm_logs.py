from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import schemas, crud
from backend.main import get_db

router = APIRouter(
    prefix="/llm-logs",
    tags=["MLOps"],
)

@router.post("/feedback", response_model=schemas.LLMLogResponse, status_code=201)
def create_llm_feedback(
    feedback: schemas.LLMFeedback, db: Session = Depends(get_db)
):
    # For V1, we'll mock the decision and model_version
    mock_decision = "APPROVE_ANKI"
    mock_model_version = "v1.0"

    db_llm_log = crud.create_llm_log_feedback(
        db=db,
        feedback=feedback,
        source_submission_id=feedback.source_submission_id, # Use actual source_submission_id from feedback
        decision=mock_decision,
        model_version=mock_model_version,
    )
    return db_llm_log

@router.patch("/feedback/{log_id}", response_model=schemas.LLMLogResponse)
def update_llm_feedback(
    log_id: int, feedback: schemas.LLMFeedback, db: Session = Depends(get_db)
):
    db_llm_log = crud.update_llm_log_feedback(
        db=db,
        log_id=log_id,
        coach_feedback=feedback.coach_feedback,
        reason_code=feedback.reason_code,
    )
    return db_llm_log
