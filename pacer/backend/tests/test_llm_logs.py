from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from pacer.backend.main import app, get_db
from pacer.backend import models, crud
from pacer.backend.models import Base
from sqlalchemy import create_engine
from datetime import datetime

# Setup for the test database
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

def test_create_llm_feedback():
    # 1. Setup: Create a dummy submission (if needed, as source_submission_id is nullable)
    db = TestingSessionLocal()
    submission_id = "sub_llm_test"
    if not db.query(models.Submission).filter_by(submission_id=submission_id).first():
        db.add(models.Submission(
            submission_id=submission_id,
            student_id="std_llm_test",
            problem_text="Test problem",
            status="COMPLETE"
        ))
        db.commit()
    db.close()

    # 2. Define the test data
    feedback_data = {
        "log_id": 1, # This will be auto-incremented in DB, but schema expects it
        "coach_feedback": "GOOD",
        "reason_code": "SIMPLE_MISTAKE",
        "source_submission_id": submission_id, # Optional, but good to test
    }

    # 3. Call the API endpoint
    response = client.post("/llm-logs/feedback", json=feedback_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["coach_feedback"] == feedback_data["coach_feedback"]
    assert data["reason_code"] == feedback_data["reason_code"]
    assert data["source_submission_id"] == feedback_data["source_submission_id"]
    assert "log_id" in data
    assert "created_at" in data

    # 5. Verify the data in the database
    db = TestingSessionLocal()
    llm_log_entry = db.query(models.LLMLog).filter_by(log_id=data["log_id"]).first()
    assert llm_log_entry is not None
    assert llm_log_entry.coach_feedback == feedback_data["coach_feedback"]
    assert llm_log_entry.reason_code == feedback_data["reason_code"]
    db.close()
