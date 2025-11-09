from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import schemas, crud
from backend.main import get_db

router = APIRouter(
    prefix="/coach-memos",
    tags=["Coaching"],
)

@router.post("/", response_model=schemas.CoachMemoResponse, status_code=201)
def create_coach_memo(
    memo: schemas.CoachMemoCreate, db: Session = Depends(get_db)
):
    db_memo = crud.create_coach_memo(db=db, memo=memo)
    return db_memo
