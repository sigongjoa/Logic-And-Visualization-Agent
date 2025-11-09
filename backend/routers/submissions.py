from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, crud
from backend.main import get_db
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

    # Step 1: Call Meta-RAG to analyze the problem (V1 Simulation)
    # This simulates steps 17 & 18 in the sequence diagram
    found_concept = crud.search_concept_by_keyword(db, submission.problem_text)

    if not found_concept:
        raise HTTPException(status_code=404, detail="No relevant concept found for the submission.")

    # Step 2: Get visualization data (V1 Simulation)
    # This simulates steps 19 & 20
    concept_id = found_concept.concept_id
    logical_path_text = f"This problem appears to be related to the concept: '{found_concept.concept_name}'. Based on our analysis, here is a step-by-step guide."
    manim_content_url = found_concept.manim_data_path or "https://youtube.com/watch?v=default_video"

    # Step 3: Store the submission (Step 21)
    db_submission = crud.create_submission(
        db=db,
        submission=submission,
    )
    db_submission.logical_path_text = logical_path_text
    db_submission.concept_id = concept_id
    db.commit()
    db.refresh(db_submission)

    # Step 4: Perform 4+1 Axis Model Update (Steps 24, 25, 26)
    
    # 4a: Update Curriculum Axis (Student Mastery)
    # For V1, we'll use a mock score, e.g., the student demonstrated 70% mastery
    crud.update_student_mastery(
        db=db,
        student_id=submission.student_id,
        concept_id=concept_id,
        mastery_score=70,
        status="IN_PROGRESS",
    )

    # 4b: Perform a micro-update on the 4-Axis Model (Student Vector)
    # As an example, let's say the analysis detected a calculation mistake,
    # slightly lowering the 'axis4_acc' score.
    
    # First, get the latest vector for the student
    latest_vector = crud.get_latest_vector_for_student(db, submission.student_id)
    
    if latest_vector:
        new_vector_data = {
            "axis1_geo": latest_vector.axis1_geo,
            "axis1_alg": latest_vector.axis1_alg,
            "axis1_ana": latest_vector.axis1_ana,
            "axis2_opt": latest_vector.axis2_opt,
            "axis2_piv": latest_vector.axis2_piv,
            "axis2_dia": latest_vector.axis2_dia,
            "axis3_con": latest_vector.axis3_con,
            "axis3_pro": latest_vector.axis3_pro,
            "axis3_ret": latest_vector.axis3_ret,
            "axis4_acc": max(0, latest_vector.axis4_acc - 5), # Decrease accuracy
            "axis4_gri": latest_vector.axis4_gri,
        }
    else:
        # If no vector exists, create a default one
        new_vector_data = {
            "axis1_geo": 50, "axis1_alg": 50, "axis1_ana": 50,
            "axis2_opt": 50, "axis2_piv": 50, "axis2_dia": 50,
            "axis3_con": 50, "axis3_pro": 50, "axis3_ret": 50,
            "axis4_acc": 45, "axis4_gri": 50,
        }

    assessment_create = schemas.AssessmentCreate(
        student_id=submission.student_id,
        assessment_type="AI_ANALYSIS",
        source_ref_id=db_submission.submission_id, # Use the newly created submission_id
        notes="AI-driven micro-update based on submission analysis. Detected potential calculation error.",
        vector_data=new_vector_data
    )
    
    crud.create_assessment_and_vector(
        db=db,
        assessment=assessment_create,
    )

    # Step 5: Return the result to the student (Step 22)
    return schemas.SubmissionResult(
        submission_id=db_submission.submission_id,
        status=db_submission.status,
        logical_path_text=db_submission.logical_path_text,
        concept_id=db_submission.concept_id,
        manim_content_url=manim_content_url,
    )
