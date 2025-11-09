from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pacer.backend import schemas, crud
from pacer.backend.main import get_db
import uuid

router = APIRouter(
    prefix="/assessments",
    tags=["4-Axis Model"],
)

@router.post("/", response_model=schemas.VectorHistoryEntry, status_code=201)
def create_assessment(
    assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)
):
    # Generate unique IDs for assessment and vector
    assessment_id = f"asmt_{uuid.uuid4()}"
    vector_id = f"vec_{uuid.uuid4()}"

    # Call the CRUD function to create the DB entries
    db_vector_history = crud.create_assessment_and_vector(
        db=db,
        assessment=assessment,
        assessment_id=assessment_id,
        vector_id=vector_id,
    )
    return db_vector_history
