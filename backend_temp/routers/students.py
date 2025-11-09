from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud
from backend.main import get_db

router = APIRouter(
    prefix="/students",
    tags=["4-Axis Model"],
)

@router.get("/{student_id}/vector-history", response_model=List[schemas.VectorHistoryEntry])
def get_vector_history(student_id: str, db: Session = Depends(get_db)):
    history = crud.get_vector_history_by_student(db=db, student_id=student_id)
    return history
