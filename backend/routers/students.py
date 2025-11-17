from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud, models
from backend.main import get_db

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

@router.post("/", response_model=schemas.Student, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    return crud.create_student(db=db, student=student)

@router.get("/", response_model=List[schemas.Student])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@router.get("/{student_id}/vector-history", response_model=List[schemas.VectorHistoryEntry])
def get_vector_history(student_id: str, db: Session = Depends(get_db)):
    history = crud.get_vector_history_by_student(db=db, student_id=student_id)
    return history

@router.get("/{student_id}/mastery", response_model=List[schemas.StudentMastery])
def get_student_mastery(student_id: str, db: Session = Depends(get_db)):
    mastery_entries = crud.get_student_mastery_by_student(db=db, student_id=student_id)
    return mastery_entries

@router.get("/{student_id}/reports", response_model=List[schemas.WeeklyReport])
def get_student_reports(student_id: str, db: Session = Depends(get_db)):
    reports = db.query(models.WeeklyReport).filter(models.WeeklyReport.student_id == student_id).all()
    return reports

@router.get("/{student_id}/latest_vector", response_model=schemas.VectorHistoryEntry)
def get_student_latest_vector(student_id: str, db: Session = Depends(get_db)):
    vector = crud.get_latest_vector_for_student(db, student_id)
    if not vector:
        raise HTTPException(status_code=404, detail="Latest vector not found for student")
    return vector

@router.get("/{student_id}/submissions", response_model=List[schemas.SubmissionResult])
def get_student_submissions(student_id: str, db: Session = Depends(get_db)):
    submissions = db.query(models.Submission).filter(models.Submission.student_id == student_id).all()
    return submissions

@router.get("/{student_id}/anki-cards", response_model=List[schemas.AnkiCard])
def get_student_anki_cards(student_id: str, db: Session = Depends(get_db)):
    anki_cards = crud.get_anki_cards_by_student(db, student_id)
    return anki_cards
