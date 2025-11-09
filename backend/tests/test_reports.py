from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
from sqlalchemy import create_engine
from datetime import datetime

# Setup for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Helper function to create a dummy report for testing
def create_dummy_report(db: Session, student_id: str, status: str):
    report = models.WeeklyReport(
        student_id=student_id,
        period_start=datetime(2025, 1, 1),
        period_end=datetime(2025, 1, 7),
        status=status,
        ai_summary="Test summary",
        vector_start_id="vec_start",
        vector_end_id="vec_end",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def test_get_report_drafts():
    # 1. Setup: Create a draft report in the DB
    db = TestingSessionLocal()
    # Clean up previous test data to avoid interference
    db.query(models.WeeklyReport).delete()
    db.commit()
    create_dummy_report(db, "std_report_user", "DRAFT")
    db.close()

    # 2. Call the API endpoint
    response = client.get("/reports/drafts")

    # 3. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["student_id"] == "std_report_user"
    assert data[0]["status"] == "DRAFT"

def test_finalize_report():
    # 1. Setup: Create a draft report
    db = TestingSessionLocal()
    draft_report = create_dummy_report(db, "std_finalize_user", "DRAFT")
    db.close()

    # 2. Call the API endpoint to finalize
    finalize_data = {"coach_comment": "Great progress this week!"}
    response = client.put(f"/reports/{draft_report.report_id}/finalize", json=finalize_data)

    # 3. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FINALIZED"
    assert data["coach_comment"] == "Great progress this week!"

    # 4. Verify the data in the database
    db = TestingSessionLocal()
    finalized_report = db.query(models.WeeklyReport).filter_by(report_id=draft_report.report_id).first()
    assert finalized_report.status == "FINALIZED"
    assert finalized_report.coach_comment == "Great progress this week!"
    assert finalized_report.finalized_at is not None
    db.close()

def test_send_report():
    # 1. Setup: Create a finalized report
    db = TestingSessionLocal()
    finalized_report = create_dummy_report(db, "std_send_user", "FINALIZED")
    db.close()

    # 2. Call the API endpoint to send
    response = client.post(f"/reports/{finalized_report.report_id}/send")

    # 3. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Report sent successfully"

    # 4. Verify the status in the database
    db = TestingSessionLocal()
    sent_report = db.query(models.WeeklyReport).filter_by(report_id=finalized_report.report_id).first()
    assert sent_report.status == "SENT"
    db.close()
