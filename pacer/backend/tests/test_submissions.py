from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from pacer.backend.main import app, get_db
from pacer.backend.models import Base, Submission
from sqlalchemy import create_engine

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
    # 1. Define the test data
    submission_data = {
        "student_id": "std_testuser_submission",
        "problem_text": "What is the derivative of x^2?",
    }

    # 2. Call the API endpoint
    response = client.post("/submissions", json=submission_data)

    # 3. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "COMPLETE"
    assert "submission_id" in data
    assert data["logical_path_text"] is not None
    assert data["concept_id"] is not None
    assert data["manim_content_url"] is not None

    # 4. Verify the data in the database
    db = TestingSessionLocal()
    submission_entry = db.query(Submission).filter_by(submission_id=data["submission_id"]).first()
    assert submission_entry is not None
    assert submission_entry.student_id == "std_testuser_submission"
    assert submission_entry.status == "COMPLETE"
    db.close()
