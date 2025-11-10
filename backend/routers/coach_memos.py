from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from backend import schemas, crud
from backend.main import get_db

router = APIRouter(
    prefix="/coach-memos",
    tags=["Coaching"],
)

@router.get("/", response_model=List[schemas.CoachMemoResponse])
def read_coach_memos(
    student_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    memos = crud.get_coach_memos(db=db, student_id=student_id, coach_id=coach_id)
    return memos

@router.post("/", response_model=schemas.CoachMemoResponse, status_code=201)
def create_coach_memo(
    memo: schemas.CoachMemoCreate, db: Session = Depends(get_db)
):
    db_memo = crud.create_coach_memo(db=db, memo=memo)
    return db_memo
