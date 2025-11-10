from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
from sqlalchemy import create_engine
from datetime import datetime, timedelta, timezone
import pytest

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
    db.query(models.AnkiCard).delete()
    db.commit()

    # Create students
    student1 = models.Student(student_id="std_test_1", student_name="Test Student 1")
    student2 = models.Student(student_id="std_test_2", student_name="Test Student 2")
    db.add_all([student1, student2])
    db.commit()

    # Create concepts
    concept1 = models.ConceptsLibrary(concept_id="C_TEST_1", curriculum_id="CUR_1", concept_name="Concept Test 1", manim_data_path="http://manim.com/test1")
    db.add(concept1)
    db.commit()

    # Create reports
    report1 = models.WeeklyReport(
        student_id=student1.student_id, period_start=datetime.now(timezone.utc) - timedelta(days=14),
        period_end=datetime.now(timezone.utc) - timedelta(days=7), status="FINALIZED",
        ai_summary="Summary 1", vector_start_id="vec_s1_1", vector_end_id="vec_e1_1"
    )
    db.add(report1)
    db.commit()

    # Create vector history
    vector1_latest = models.StudentVectorHistory(
        vector_id="vec_latest_1", assessment_id="asmt_latest_1", student_id=student1.student_id,
        created_at=datetime.now(timezone.utc) - timedelta(days=1),
        axis1_geo=20, axis1_alg=20, axis1_ana=20, axis2_opt=20, axis2_piv=20,
        axis2_dia=20, axis3_con=20, axis3_pro=20, axis3_ret=20, axis4_acc=20, axis4_gri=20
    )
    db.add(vector1_latest)
    db.commit()

    # Create submissions
    submission1 = models.Submission(
        submission_id="sub_test_1", student_id=student1.student_id, problem_text="Problem 1",
        status="COMPLETE", logical_path_text="Path 1", concept_id=concept1.concept_id,
        submitted_at=datetime.now(timezone.utc) - timedelta(days=2)
    )
    db.add(submission1)
    db.commit()

    # Create Anki cards
    anki_card1 = models.AnkiCard(
        student_id=student1.student_id, llm_log_id=1, question="Anki Question 1",
        answer="Anki Answer 1", next_review_date=datetime.now(timezone.utc) + timedelta(days=1)
    )
    db.add(anki_card1)
    db.commit()

    return {
        "student1_id": student1.student_id,
        "student2_id": student2.student_id,
        "report1_id": report1.report_id,
        "vector1_latest_id": vector1_latest.vector_id,
        "submission1_id": submission1.submission_id,
        "concept1_id": concept1.concept_id,
        "anki_card1_id": anki_card1.card_id,
    }

def test_get_all_students(db_session: Session):
    setup_test_data(db_session)
    response = client.get("/students/")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_get_student_reports(db_session: Session):
    data_ids = setup_test_data(db_session)
    response = client.get(f"/students/{data_ids['student1_id']}/reports")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['report_id'] == data_ids['report1_id']

def test_get_student_latest_vector(db_session: Session):
    data_ids = setup_test_data(db_session)
    response = client.get(f"/students/{data_ids['student1_id']}/latest_vector")
    assert response.status_code == 200
    assert response.json()['vector_id'] == data_ids['vector1_latest_id']

def test_get_student_submissions(db_session: Session):
    data_ids = setup_test_data(db_session)
    response = client.get(f"/students/{data_ids['student1_id']}/submissions")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['submission_id'] == data_ids['submission1_id']

def test_get_student_anki_cards(db_session: Session):
    data_ids = setup_test_data(db_session)
    response = client.get(f"/students/{data_ids['student1_id']}/anki-cards")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['card_id'] == data_ids['anki_card1_id']

def test_get_vector_history(db_session: Session):
    data_ids = setup_test_data(db_session)
    response = client.get(f"/students/{data_ids['student1_id']}/vector-history")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_student_mastery(db_session: Session):
    # Setup
    student_id = "std_mastery_user"
    concept_id = "C_MASTER_1"
    crud.create_student(db_session, crud.schemas.StudentCreate(student_id=student_id, student_name="Mastery Student"))
    crud.create_student_mastery(db_session, crud.schemas.StudentMastery(student_id=student_id, concept_id=concept_id, mastery_score=80, status="MASTERED"))

    response = client.get(f"/students/{student_id}/mastery")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['mastery_score'] == 80
