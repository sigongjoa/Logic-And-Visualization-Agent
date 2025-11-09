from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import schemas, crud
from backend.main import get_db
import uuid

router = APIRouter(
    prefix="/assessments",
    tags=["4-Axis Model"],
)

@router.post("/", response_model=schemas.VectorHistoryEntry, status_code=201)
def create_assessment(
    assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)
):
    # Call the CRUD function to create the DB entries
    db_assessment, db_vector_history = crud.create_assessment_and_vector(
        db=db,
        assessment=assessment,
    )
    return db_vector_history
