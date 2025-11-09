from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import schemas, crud, models # Added models
from backend.main import get_db

router = APIRouter(
    prefix="/coaches",
    tags=["Coaches"],
)

@router.get("/students", response_model=List[schemas.StudentCreate])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@router.get("/students/{student_id}/reports", response_model=List[schemas.WeeklyReport])
def get_student_reports(student_id: str, db: Session = Depends(get_db)):
    reports = db.query(models.WeeklyReport).filter(models.WeeklyReport.student_id == student_id).all()
    return reports

@router.get("/students/{student_id}/latest_vector", response_model=schemas.VectorHistoryEntry)
def get_student_latest_vector(student_id: str, db: Session = Depends(get_db)):
    vector = crud.get_latest_vector_for_student(db, student_id)
    if not vector:
        raise HTTPException(status_code=404, detail="Latest vector not found for student")
    return vector

@router.get("/students/{student_id}/submissions", response_model=List[schemas.SubmissionResult])
def get_student_submissions(student_id: str, db: Session = Depends(get_db)):
    submissions = db.query(models.Submission).filter(models.Submission.student_id == student_id).all()
    # Convert Submission models to SubmissionResult schemas
    results = []
    for sub in submissions:
        concept = crud.get_concept(db, sub.concept_id)
        manim_content_url = concept.manim_data_path if concept else "https://youtube.com/watch?v=default_video"
        results.append(schemas.SubmissionResult(
            submission_id=sub.submission_id,
            status=sub.status,
            logical_path_text=sub.logical_path_text,
            concept_id=sub.concept_id,
            manim_content_url=manim_content_url
        ))
    return results

@router.get("/students/{student_id}/anki-cards", response_model=List[schemas.AnkiCard])
def get_student_anki_cards(student_id: str, db: Session = Depends(get_db)):
    anki_cards = crud.get_anki_cards_by_student(db, student_id)
    return anki_cards
