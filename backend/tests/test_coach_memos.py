from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
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

def test_create_coach_memo():
    # 1. Setup: Create a dummy coach and student
    db = TestingSessionLocal()
    coach_id = "coach_test"
    student_id = "std_test_memo"

    if not db.query(models.Coach).filter_by(coach_id=coach_id).first():
        db.add(models.Coach(coach_id=coach_id, coach_name="Test Coach"))
        db.commit()
    if not db.query(models.Student).filter_by(student_id=student_id).first():
        db.add(models.Student(student_id=student_id, student_name="Test Student Memo"))
        db.commit()
    db.close()

    # 2. Define the test data
    memo_data = {
        "coach_id": coach_id,
        "student_id": student_id,
        "memo_text": "Student showed great improvement in pivot thinking today.",
    }

    # 3. Call the API endpoint
    response = client.post("/coach-memos/", json=memo_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["coach_id"] == coach_id
    assert data["student_id"] == student_id
    assert data["memo_text"] == memo_data["memo_text"]
    assert "memo_id" in data
    assert "created_at" in data

    # 5. Verify the data in the database
    db = TestingSessionLocal()
    memo_entry = db.query(models.CoachMemo).filter_by(memo_id=data["memo_id"]).first()
    assert memo_entry is not None
    assert memo_entry.coach_id == coach_id
    assert memo_entry.student_id == student_id
    assert memo_entry.memo_text == memo_data["memo_text"]
    db.close()

def test_read_coach_memos():
    db = TestingSessionLocal()
    # Setup: Clear old memos and create new data
    db.query(models.CoachMemo).delete()
    db.commit()

    coach_id1 = "coach_memo_1"
    coach_id2 = "coach_memo_2"
    student_id1 = "std_memo_1"
    student_id2 = "std_memo_2"

    # Create coaches and students if they don't exist
    if not db.query(models.Coach).filter_by(coach_id=coach_id1).first():
        db.add(models.Coach(coach_id=coach_id1, coach_name="Memo Coach 1"))
    if not db.query(models.Coach).filter_by(coach_id=coach_id2).first():
        db.add(models.Coach(coach_id=coach_id2, coach_name="Memo Coach 2"))
    if not db.query(models.Student).filter_by(student_id=student_id1).first():
        db.add(models.Student(student_id=student_id1, student_name="Memo Student 1"))
    if not db.query(models.Student).filter_by(student_id=student_id2).first():
        db.add(models.Student(student_id=student_id2, student_name="Memo Student 2"))
    db.commit()

    # Create memos
    memo1 = models.CoachMemo(coach_id=coach_id1, student_id=student_id1, memo_text="Memo 1")
    memo2 = models.CoachMemo(coach_id=coach_id1, student_id=student_id2, memo_text="Memo 2")
    memo3 = models.CoachMemo(coach_id=coach_id2, student_id=student_id1, memo_text="Memo 3")
    db.add_all([memo1, memo2, memo3])
    db.commit()
    db.close()

    # Test fetching all memos
    response = client.get("/coach-memos/")
    assert response.status_code == 200
    assert len(response.json()) >= 3

    # Test fetching memos for a specific student
    response = client.get(f"/coach-memos/?student_id={student_id1}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(d["memo_text"] == "Memo 1" for d in data)
    assert any(d["memo_text"] == "Memo 3" for d in data)

    # Test fetching memos for a specific coach
    response = client.get(f"/coach-memos/?coach_id={coach_id1}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(d["memo_text"] == "Memo 1" for d in data)
    assert any(d["memo_text"] == "Memo 2" for d in data)
