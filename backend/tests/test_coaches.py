import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud, schemas
from sqlalchemy import create_engine
from datetime import datetime, timedelta, timezone

# Setup for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    # Create a new database session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_test_data(db: Session):
    # Clear all relevant tables
    db.query(models.student_coach_relation).delete()
    db.query(models.Student).delete()
    db.query(models.Coach).delete()
    db.query(models.WeeklyReport).delete()
    db.query(models.StudentVectorHistory).delete()
    db.query(models.Submission).delete()
    db.query(models.ConceptsLibrary).delete()
    db.query(models.AnkiCard).delete() # Clear AnkiCard entries
    db.commit()

    # Create a coach
    coach1 = models.Coach(coach_id="coach_test_1", coach_name="Test Coach")
    db.add(coach1)
    db.commit()
    db.refresh(coach1)

    # Create students
    student1 = models.Student(student_id="std_coach_1", student_name="Coach Student 1")
    student2 = models.Student(student_id="std_coach_2", student_name="Coach Student 2")
    db.add_all([student1, student2])
    db.commit()
    db.refresh(student1)
    db.refresh(student2)

    # Associate students with coach
    coach1.students.append(student1)
    coach1.students.append(student2)
    db.commit()

    # Create concepts
    concept1 = models.ConceptsLibrary(concept_id="C_COACH_1", curriculum_id="CUR_1", concept_name="Concept Coach 1", manim_data_path="http://manim.com/coach1")
    concept2 = models.ConceptsLibrary(concept_id="C_COACH_2", curriculum_id="CUR_1", concept_name="Concept Coach 2", manim_data_path="http://manim.com/coach2")
    db.add_all([concept1, concept2])
    db.commit()
    db.refresh(concept1)
    db.refresh(concept2)

    # Create reports
    report1 = models.WeeklyReport(
        student_id=student1.student_id, period_start=datetime.now(timezone.utc) - timedelta(days=14),
        period_end=datetime.now(timezone.utc) - timedelta(days=7), status="FINALIZED",
        ai_summary="Summary 1", vector_start_id="vec_s1_1", vector_end_id="vec_e1_1"
    )
    report2 = models.WeeklyReport(
        student_id=student1.student_id, period_start=datetime.now(timezone.utc) - timedelta(days=7),
        period_end=datetime.now(timezone.utc), status="DRAFT",
        ai_summary="Summary 2", vector_start_id="vec_s1_2", vector_end_id="vec_e1_2"
    )
    db.add_all([report1, report2])
    db.commit()
    db.refresh(report1)
    db.refresh(report2)

    # Create vector history
    vector1_old = models.StudentVectorHistory(
        vector_id="vec_s1_1", assessment_id="asmt_s1_1", student_id=student1.student_id,
        created_at=datetime.now(timezone.utc) - timedelta(days=15),
        axis1_geo=10, axis1_alg=10, axis1_ana=10, axis2_opt=10, axis2_piv=10,
        axis2_dia=10, axis3_con=10, axis3_pro=10, axis3_ret=10, axis4_acc=10, axis4_gri=10
    )
    vector1_latest = models.StudentVectorHistory(
        vector_id="vec_latest_1", assessment_id="asmt_latest_1", student_id=student1.student_id,
        created_at=datetime.now(timezone.utc) - timedelta(days=1),
        axis1_geo=20, axis1_alg=20, axis1_ana=20, axis2_opt=20, axis2_piv=20,
        axis2_dia=20, axis3_con=20, axis3_pro=20, axis3_ret=20, axis4_acc=20, axis4_gri=20
    )
    db.add_all([vector1_old, vector1_latest])
    db.commit()
    db.refresh(vector1_old)
    db.refresh(vector1_latest)

    # Create submissions
    submission1 = models.Submission(
        submission_id="sub_coach_1", student_id=student1.student_id, problem_text="Problem 1",
        status="COMPLETE", logical_path_text="Path 1", concept_id=concept1.concept_id,
        submitted_at=datetime.now(timezone.utc) - timedelta(days=2)
    )
    submission2 = models.Submission(
        submission_id="sub_coach_2", student_id=student1.student_id, problem_text="Problem 2",
        status="PENDING", logical_path_text="Path 2", concept_id=concept2.concept_id,
        submitted_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    db.add_all([submission1, submission2])
    db.commit()
    db.refresh(submission1)
    db.refresh(submission2)

    return {
        "coach1_id": coach1.coach_id,
        "student1_id": student1.student_id,
        "student2_id": student2.student_id,
        "report1_id": report1.report_id,
        "report2_id": report2.report_id,
        "vector1_latest_id": vector1_latest.vector_id,
        "submission1_id": submission1.submission_id,
        "submission2_id": submission2.submission_id,
        "concept1_id": concept1.concept_id,
        "concept2_id": concept2.concept_id,
    }

def test_read_coach(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    response = client.get(f"/coaches/{coach_id}")
    assert response.status_code == 200
    coach_data = response.json()
    assert coach_data["coach_id"] == coach_id
    assert coach_data["coach_name"] == "Test Coach"

def test_read_coach_students(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    response = client.get(f"/coaches/{coach_id}/students")
    assert response.status_code == 200
    students_data = response.json()
    assert len(students_data) == 2
    student_ids = {s["student_id"] for s in students_data}
    assert data_ids["student1_id"] in student_ids
    assert data_ids["student2_id"] in student_ids

def test_read_coach_submissions(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    # Test without status filter
    response = client.get(f"/coaches/{coach_id}/submissions")
    assert response.status_code == 200
    submissions_data = response.json()
    assert len(submissions_data) == 2
    submission_ids = {s["submission_id"] for s in submissions_data}
    assert data_ids["submission1_id"] in submission_ids
    assert data_ids["submission2_id"] in submission_ids

    # Test with status filter
    response = client.get(f"/coaches/{coach_id}/submissions?status=PENDING")
    assert response.status_code == 200
    submissions_data = response.json()
    assert len(submissions_data) == 1
    assert submissions_data[0]["submission_id"] == data_ids["submission2_id"]
    assert submissions_data[0]["status"] == "PENDING"

def test_read_coach(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    response = client.get(f"/coaches/{coach_id}")
    assert response.status_code == 200
    coach_data = response.json()
    assert coach_data["coach_id"] == coach_id
    assert coach_data["coach_name"] == "Test Coach"

def test_read_coach_students(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    response = client.get(f"/coaches/{coach_id}/students")
    assert response.status_code == 200
    students_data = response.json()
    assert len(students_data) == 2
    student_ids = {s["student_id"] for s in students_data}
    assert data_ids["student1_id"] in student_ids
    assert data_ids["student2_id"] in student_ids

def test_read_coach_submissions(db_session: Session):
    data_ids = setup_test_data(db_session)
    coach_id = data_ids["coach1_id"]

    # Test without status filter
    response = client.get(f"/coaches/{coach_id}/submissions")
    assert response.status_code == 200
    submissions_data = response.json()
    assert len(submissions_data) == 2
    submission_ids = {s["submission_id"] for s in submissions_data}
    assert data_ids["submission1_id"] in submission_ids
    assert data_ids["submission2_id"] in submission_ids

    # Test with status filter
    response = client.get(f"/coaches/{coach_id}/submissions?status=PENDING")
    assert response.status_code == 200
    submissions_data = response.json()
    assert len(submissions_data) == 1
    assert submissions_data[0]["submission_id"] == data_ids["submission2_id"]
    assert submissions_data[0]["status"] == "PENDING"
