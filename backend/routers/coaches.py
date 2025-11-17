from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend import schemas, crud, models
from backend.main import get_db

router = APIRouter(
    prefix="/coaches",
    tags=["Coaches"],
)

@router.get("/", response_model=List[schemas.Coach])
def read_coaches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coaches = db.query(models.Coach).offset(skip).limit(limit).all()
    return coaches

@router.get("/{coach_id}", response_model=schemas.Coach)
def read_coach(coach_id: str, db: Session = Depends(get_db)):
    db_coach = crud.get_coach(db, coach_id=coach_id)
    if db_coach is None:
        raise HTTPException(status_code=404, detail="Coach not found")
    return db_coach

@router.get("/{coach_id}/students", response_model=List[schemas.Student])
def read_coach_students(coach_id: str, db: Session = Depends(get_db)):
    students = crud.get_students_by_coach(db, coach_id=coach_id)
    # The crud function returns an empty list if the coach has no students,
    # or if the coach is not found. This is acceptable.
    return students

@router.get("/{coach_id}/submissions", response_model=List[schemas.SubmissionResult])
def read_coach_submissions(coach_id: str, status: Optional[str] = None, db: Session = Depends(get_db)):
    submissions = crud.get_submissions_by_coach(db, coach_id=coach_id, status=status)
    results = []
    for sub in submissions:
        concept = crud.get_concept(db, sub.concept_id)
        manim_content_url = concept.manim_data_path if concept else "https://youtube.com/watch?v=default_video"
        
        manim_json_output = None
        if sub.manim_visualization_json:
            manim_json_output = json.loads(sub.manim_visualization_json)

        results.append(schemas.SubmissionResult(
            submission_id=sub.submission_id,
            student_id=sub.student_id,
            problem_text=sub.problem_text,
            status=sub.status,
            logical_path_text=sub.logical_path_text,
            concept_id=sub.concept_id,
            manim_content_url=manim_content_url,
            audio_explanation_url=sub.audio_explanation_url,
            manim_visualization_json=manim_json_output,
            submitted_at=sub.submitted_at,
        ))
    return results
