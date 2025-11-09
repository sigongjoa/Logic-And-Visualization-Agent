from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from pacer.backend.main import app, get_db
from pacer.backend import models, crud
from pacer.backend.models import Base
from sqlalchemy import create_engine
from datetime import datetime

# Setup the Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_submission():
    # 1. Setup: Create a student, curriculum, and concept
    db = TestingSessionLocal()
    student_id = "std_testuser_submission"
    curriculum_id = "MATH-01"
    concept_id = "C-001"

    # Ensure student exists (or create if not)
    if not db.query(models.Student).filter_by(student_id=student_id).first():
        db.add(models.Student(student_id=student_id, student_name="Test Student"))
        db.commit()

    # Clean up previous test data for StudentMastery
    db.query(models.StudentMastery).filter_by(student_id=student_id, concept_id=concept_id).delete()
    db.commit()

    # Create Curriculum
    if not db.query(models.Curriculum).filter_by(curriculum_id=curriculum_id).first():
        db.add(models.Curriculum(curriculum_id=curriculum_id, curriculum_name="Middle School Math"))
        db.commit()

    # Create Concept
    if not db.query(models.ConceptsLibrary).filter_by(concept_id=concept_id).first():
        db.add(models.ConceptsLibrary(
            concept_id=concept_id,
            curriculum_id=curriculum_id,
            concept_name="Quadratic Formula",
            manim_data_path="http://example.com/manim/C-001"
        ))
        db.commit()
    db.close()

    # 2. Define the test data
    submission_data = {
        "student_id": student_id,
        "problem_text": "What is the derivative of x^2?",
    }

    # 3. Call the API endpoint
    response = client.post("/submissions", json=submission_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "COMPLETE"
    assert "submission_id" in data
    assert data["logical_path_text"] is not None
    assert data["concept_id"] == concept_id # Ensure the mocked concept_id is returned
    assert data["manim_content_url"] is not None

    # 5. Verify the data in the database (Submission and StudentMastery)
    db = TestingSessionLocal()
    submission_entry = db.query(models.Submission).filter_by(submission_id=data["submission_id"]).first()
    assert submission_entry is not None
    assert submission_entry.student_id == student_id
    assert submission_entry.status == "COMPLETE"

    mastery_entry = db.query(models.StudentMastery).filter_by(student_id=student_id, concept_id=concept_id).first()
    assert mastery_entry is not None
    assert mastery_entry.mastery_score == 70 # Assuming a mock mastery score update
    assert mastery_entry.status == "MASTERED" # Assuming a mock status
    assert mastery_entry.last_updated is not None
    db.close()
