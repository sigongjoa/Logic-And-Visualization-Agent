from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
from backend import schemas as backend_schemas, crud # Modified line
from backend.models import Base
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

def test_update_llm_feedback():
    db = TestingSessionLocal()
    # 1. Setup: Create an initial LLMLog entry
    initial_feedback_data = backend_schemas.LLMFeedback( # Modified line
        coach_feedback="NEUTRAL",
        reason_code="INITIAL_REVIEW",
        source_submission_id="sub_initial_llm_log"
    )
    initial_llm_log = crud.create_llm_log_feedback(
        db=db,
        feedback=initial_feedback_data,
        source_submission_id="sub_initial_llm_log",
        decision="INITIAL_ANALYSIS",
        model_version="v0.9"
    )
    db.close()

    # 2. Define the update data
    updated_feedback_data = {
        "coach_feedback": "GOOD",
        "reason_code": "SIMPLE_MISTAKE",
    }

    # 3. Call the API endpoint to update
    response = client.patch(f"/llm-logs/feedback/{initial_llm_log.log_id}", json=updated_feedback_data)

    # 4. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["log_id"] == initial_llm_log.log_id
    assert data["coach_feedback"] == updated_feedback_data["coach_feedback"]
    assert data["reason_code"] == updated_feedback_data["reason_code"]

    # 5. Verify the data in the database
    db = TestingSessionLocal()
    updated_llm_log_entry = db.query(models.LLMLog).filter_by(log_id=initial_llm_log.log_id).first()
    assert updated_llm_log_entry is not None
    assert updated_llm_log_entry.coach_feedback == updated_feedback_data["coach_feedback"]
    assert updated_llm_log_entry.reason_code == updated_feedback_data["reason_code"]
    db.close()