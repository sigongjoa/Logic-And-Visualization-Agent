from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
from sqlalchemy import create_engine
from datetime import datetime, timedelta, timezone # Added timezone
import pytest
from backend.scripts.generate_weekly_reports import generate_weekly_reports

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
        period_start=datetime(2025, 1, 1, tzinfo=timezone.utc), # Use timezone-aware datetime
        period_end=datetime(2025, 1, 7, tzinfo=timezone.utc),   # Use timezone-aware datetime
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
    # 1. Setup: Create a finalized report, a student, and a parent
    db = TestingSessionLocal()
    # Ensure student exists
    if not db.query(models.Student).filter_by(student_id="std_send_user").first():
        db.add(models.Student(student_id="std_send_user", student_name="Test Send User"))
        db.commit()
    
    # Ensure parent exists and is associated
    parent_id = 1 # Assuming parent_id is auto-incremented, or use a fixed ID
    if not db.query(models.Parent).filter_by(parent_id=parent_id).first():
        db.add(models.Parent(parent_id=parent_id, parent_name="Test Parent", kakao_user_id="kakao_test_user"))
        db.commit()
    
    # Associate student and parent
    if not db.query(models.student_parent_association).filter_by(student_id="std_send_user", parent_id=parent_id).first():
        db.execute(models.student_parent_association.insert().values(student_id="std_send_user", parent_id=parent_id))
        db.commit()

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

@pytest.mark.asyncio
async def test_generate_weekly_reports():
    # 1. Create a student (if not already exists)
    db = TestingSessionLocal()
    student_id = "test_student_report"
    if not db.query(models.Student).filter_by(student_id=student_id).first():
        db.add(models.Student(student_id=student_id, student_name="Test Report Student"))
        db.commit()

    # Ensure parent exists and is associated
    parent_id = 1 # Use a fixed ID for testing
    if not db.query(models.Parent).filter_by(parent_id=parent_id).first():
        db.add(models.Parent(parent_id=parent_id, parent_name="Test Report Parent", kakao_user_id="kakao_test_report_user"))
        db.commit()
    
    # Associate student and parent
    if not db.query(models.student_parent_association).filter_by(student_id=student_id, parent_id=parent_id).first():
        db.execute(models.student_parent_association.insert().values(student_id=student_id, parent_id=parent_id))
        db.commit()

    # 2. Create some vector history, submissions, and mastery updates for the student
    # Clean up previous data
    db.query(models.StudentVectorHistory).filter_by(student_id=student_id).delete()
    db.query(models.Submission).filter_by(student_id=student_id).delete()
    db.query(models.StudentMastery).filter_by(student_id=student_id).delete()
    db.commit()

    today = datetime.now(timezone.utc) # Updated to timezone-aware datetime
    one_week_ago = today - timedelta(days=7)

    # Create vector history
    db.add(models.StudentVectorHistory(
        vector_id="vec_report_1", assessment_id="asmt_report_1", student_id=student_id,
        created_at=one_week_ago + timedelta(days=1), # Start of week
        axis1_geo=50, axis1_alg=50, axis1_ana=50, axis2_opt=50, axis2_piv=50,
        axis2_dia=50, axis3_con=50, axis3_pro=50, axis3_ret=50, axis4_acc=50, axis4_gri=50
    ))
    db.add(models.StudentVectorHistory(
        vector_id="vec_report_2", assessment_id="asmt_report_2", student_id=student_id,
        created_at=today - timedelta(days=3),
        axis1_geo=55, axis1_alg=55, axis1_ana=55, axis2_opt=55, axis2_piv=55,
        axis2_dia=55, axis3_con=55, axis3_pro=55, axis3_ret=55, axis4_acc=55, axis4_gri=55
    ))
    db.add(models.StudentVectorHistory(
        vector_id="vec_report_3", assessment_id="asmt_report_3", student_id=student_id,
        created_at=today - timedelta(minutes=1), # End of week (just before report generation)
        axis1_geo=60, axis1_alg=60, axis1_ana=60, axis2_opt=60, axis2_piv=60,
        axis2_dia=60, axis3_con=60, axis3_pro=60, axis3_ret=60, axis4_acc=60, axis4_gri=60
    ))

    # Create a concept for submissions and mastery
    concept_id_math = "C_MATH_TEST"
    if not db.query(models.ConceptsLibrary).filter_by(concept_id=concept_id_math).first():
        db.add(models.ConceptsLibrary(
            concept_id=concept_id_math, curriculum_id="M-ALL", concept_name="Math Test Concept", manim_data_path="http://example.com/manim/math_test"
        ))
    
    # Create some submissions
    db.add(models.Submission(
        submission_id="sub_report_1", student_id=student_id, problem_text="Report Problem 1",
        submitted_at=today - timedelta(days=5), status="COMPLETE",
        logical_path_text="Logical path for problem 1", concept_id=concept_id_math
    ))
    db.add(models.Submission(
        submission_id="sub_report_2", student_id=student_id, problem_text="Report Problem 2",
        submitted_at=today - timedelta(days=2), status="PENDING",
        logical_path_text="Logical path for problem 2", concept_id=concept_id_math
    ))

    # Create some mastery updates
    db.add(models.StudentMastery(
        student_id=student_id, concept_id=concept_id_math, mastery_score=75, status="IN_PROGRESS",
        last_updated=today - timedelta(days=4)
    ))
    db.commit()

    # 3. Run the report generation script
    await generate_weekly_reports(db=db)

    # 4. Retrieve the newly created report
    reports = db.query(models.WeeklyReport).filter_by(student_id=student_id).all()
    assert len(reports) == 1
    new_report = reports[0]

    # 5. Send the report
    crud.send_report(db, new_report.report_id)

    # 6. Assertions
    # Verify that the report status is SENT after sending
    sent_report = db.query(models.WeeklyReport).filter_by(report_id=new_report.report_id).first()
    assert sent_report.status == "SENT"
    assert sent_report.vector_start_id == "vec_report_1"
    assert sent_report.vector_end_id == "vec_report_3"

    # Assert specific content in the AI summary (updated for Korean and qualitative summary)
    student_name = db.query(models.Student).filter_by(student_id=student_id).first().student_name
    assert f"주간 학습 리포트 - {student_name}" in sent_report.ai_summary
    assert "4축 모델 변화" in sent_report.ai_summary
    assert "이번 주 연산 정확성(axis4_acc)은 60점으로, 지난 주 대비 10점 향상되었습니다." in sent_report.ai_summary
    assert "난이도 내성(axis4_gri)은 60점으로, 지난 주 대비 10점 향상되었습니다." in sent_report.ai_summary
    assert "이번 주 학습 활동" in sent_report.ai_summary
    assert "총 2개의 문제를 제출했습니다. 그 중 1개를 완료했습니다." in sent_report.ai_summary
    assert "미완료 문제: Report Problem 2" in sent_report.ai_summary
    assert "개념 숙련도 변화" in sent_report.ai_summary
    assert "숙련도가 향상된 개념: C_MATH_TEST" in sent_report.ai_summary
    assert "전반적으로 연산 정확성과 난이도 내성 모두 긍정적인 변화를 보였습니다. 꾸준한 학습 태도가 돋보입니다." in sent_report.ai_summary
    db.close()