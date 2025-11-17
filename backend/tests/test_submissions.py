from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend.models import Base, Student, Submission, StudentMastery, StudentVectorHistory, ConceptsLibrary, Curriculum
from backend import crud, schemas
import pytest
import os
import json # Added this line

# Setup the Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Populate initial data for testing
        curriculums = [
            {"curriculum_id": "M-ALL", "curriculum_name": "중등 수학: 공통 기초"},
            {"curriculum_id": "H-COMMON", "curriculum_name": "고등 수학 (상), (하)"},
        ]
        for curr_data in curriculums:
            if not db.query(Curriculum).filter_by(curriculum_id=curr_data["curriculum_id"]).first():
                db.add(Curriculum(**curr_data))
        
        concepts = [
            {"concept_id": "C-MALL-001", "curriculum_id": "M-ALL", "concept_name": "소인수분해", "manim_data_path": "https://youtube.com/watch?v=manim_video_for_prime_factorization"},
            {"concept_id": "C-HCOM-004", "curriculum_id": "H-COMMON", "concept_name": "이차방정식", "manim_data_path": "https://youtube.com/watch?v=manim_video_for_quadratic_equation"},
            {"concept_id": "C-MALL-013", "curriculum_id": "M-ALL", "concept_name": "피타고라스의 정리", "manim_data_path": "https://youtube.com/watch?v=manim_video_for_pythagorean_theorem"},
        ]
        for concept_data in concepts:
            if not db.query(ConceptsLibrary).filter_by(concept_id=concept_data["concept_id"]).first():
                db.add(ConceptsLibrary(**concept_data))
        db.commit()

        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

import unittest.mock

def test_create_submission(db_session: Session):
    # 1. Create a dummy student
    student_id = "std_test_submission"
    student_name = "Test Student"
    crud.create_student(db_session, schemas.StudentCreate(student_id=student_id, student_name=student_name))

    # 2. Define the test submission data
    submission_data = {
        "student_id": student_id,
        "problem_text": "x^2 - 4x + 3 = 0의 해를 구하시오. (이차방정식 문제)",
    }

    # 3. Call the API endpoint
    response = client.post("/submissions", json=submission_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert "submission_id" in data
    assert data["status"] == "COMPLETE"
    assert isinstance(data["logical_path_text"], str) and len(data["logical_path_text"]) > 0
    assert data["concept_id"] == "C-HCOM-004" # Based on simulated LLM response for "이차방정식"
    assert data["manim_content_url"] == "https://youtube.com/watch?v=manim_video_for_quadratic_equation" # From ConceptsLibrary
    assert "audio_explanation_url" in data
    assert data["audio_explanation_url"].startswith("https://audio.example.com/")
    assert data["audio_explanation_url"].endswith(".wav")

    # 5. Verify the data in the database
    db = db_session
    
    # Verify Submission
    db_submission = db.query(Submission).filter_by(submission_id=data["submission_id"]).first()
    assert db_submission is not None
    assert db_submission.student_id == student_id
    assert db_submission.problem_text == submission_data["problem_text"]
    assert db_submission.status == "COMPLETE"
    assert db_submission.concept_id == "C-HCOM-004"
    assert db_submission.manim_data_path == "https://youtube.com/watch?v=manim_video_for_quadratic_equation"
    assert db_submission.audio_explanation_url.startswith("https://audio.example.com/")
    assert db_submission.audio_explanation_url.endswith(".wav")

    # Verify StudentMastery
    db_mastery = db.query(StudentMastery).filter_by(student_id=student_id, concept_id="C-HCOM-004").first()
    assert db_mastery is not None
    # The exact score depends on the real LLM output, so we check for a reasonable range
    assert 0 <= db_mastery.mastery_score <= 100
    assert db_mastery.status == "IN_PROGRESS"

    # Verify StudentVectorHistory
    db_vector_history = db.query(StudentVectorHistory).filter_by(student_id=student_id).order_by(StudentVectorHistory.created_at.desc()).first()
    assert db_vector_history is not None
    assert db_vector_history.assessment_id is not None
    # The exact score depends on the real LLM output, so we check for a reasonable range
    assert 0 <= db_vector_history.axis1_alg <= 100

def test_get_submission_by_id(db_session: Session):
    # Create a dummy student
    student_id = "std_test_get_submission"
    student_name = "Test Student Get Submission"
    crud.create_student(db_session, schemas.StudentCreate(student_id=student_id, student_name=student_name))

    # Create a submission
    submission_data = {
        "student_id": student_id,
        "problem_text": "x^2 - 4x + 3 = 0의 해를 구하시오. (이차방정식 문제)",
    }
    response_post = client.post("/submissions", json=submission_data)
    assert response_post.status_code == 201
    created_submission_id = response_post.json()["submission_id"]

    # Test fetching the submission by ID
    response_get = client.get(f"/submissions/{created_submission_id}")
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["submission_id"] == created_submission_id
    assert data_get["status"] == "COMPLETE"
    assert isinstance(data_get["logical_path_text"], str) and len(data_get["logical_path_text"]) > 0
    assert isinstance(data_get["concept_id"], str) and len(data_get["concept_id"]) > 0
    assert isinstance(data_get["manim_content_url"], str) and data_get["manim_content_url"].startswith("https://")
    assert "audio_explanation_url" in data_get
    assert data_get["audio_explanation_url"].startswith("https://audio.example.com/")
    assert data_get["audio_explanation_url"].endswith(".wav")

    # Test fetching a non-existent submission
    response_not_found = client.get("/submissions/non_existent_id")
    assert response_not_found.status_code == 404
    assert response_not_found.json()["detail"] == "Submission not found"