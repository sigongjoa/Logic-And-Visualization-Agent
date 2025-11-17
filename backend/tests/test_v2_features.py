import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app, get_db
from backend.models import Base, Student, ConceptsLibrary, Assessment, StudentVectorHistory, Submission
import uuid
from datetime import datetime, UTC
import json

# Setup for in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Helper function to create a student
def create_test_student(db_session, student_id="test_student_v2", student_name="Test Student V2"):
    student = Student(student_id=student_id, student_name=student_name)
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student

# Helper function to create a concept
def create_test_concept(db_session, concept_id="C_V2_TEST", concept_name="V2 Test Concept"):
    concept = ConceptsLibrary(concept_id=concept_id, concept_name=concept_name, curriculum_id="M-ALL")
    db_session.add(concept)
    db_session.commit()
    db_session.refresh(concept)
    return concept

# Test for manim_visualization_json in submission
def test_create_submission_with_manim_json(client, db_session):
    student = create_test_student(db_session)
    concept = create_test_concept(db_session)

    # Mock LLM response to include the concept_id
    # This is a simplified mock, in a real scenario you'd mock the external LLM call
    # For now, we'll rely on the existing mock LLM config if USE_MOCK_LLM is true
    # or ensure the problem_text triggers a known concept.
    
    problem_text = "Solve for x in 2x + 5 = 10 (C_V2_TEST)" # Include concept keyword for mock LLM
    manim_json_data = {"scene": "EquationScene", "objects": [{"type": "Square", "color": "BLUE"}]}

    response = client.post(
        "/submissions/",
        json={
            "student_id": student.student_id,
            "problem_text": problem_text,
            "manim_visualization_json": manim_json_data,
        },
    )
    assert response.status_code == 201
    submission_data = response.json()
    assert submission_data["student_id"] == student.student_id
    assert submission_data["problem_text"] == problem_text
    assert submission_data["status"] == "COMPLETE"
    assert submission_data["manim_visualization_json"] == manim_json_data

    # Verify it's stored in the database
    db_submission = db_session.query(Submission).filter(Submission.submission_id == submission_data["submission_id"]).first()
    assert db_submission is not None
    assert db_submission.manim_visualization_json == json.dumps(manim_json_data)

def test_get_submission_with_manim_json(client, db_session):
    student = create_test_student(db_session, student_id="test_student_get_v2")
    concept = create_test_concept(db_session, concept_id="C_GET_V2_TEST")

    problem_text = "Another problem for retrieval (C_GET_V2_TEST)"
    manim_json_data = {"scene": "GraphScene", "objects": [{"type": "Circle", "color": "RED"}]}
    submission_id = f"sub_{uuid.uuid4().hex[:8]}"

    db_submission = Submission(
        submission_id=submission_id,
        student_id=student.student_id,
        problem_text=problem_text,
        submitted_at=datetime.now(UTC),
        concept_id=concept.concept_id,
        logical_path_text="Logical path for retrieval",
        status="COMPLETE",
        manim_data_path="manim/path/to/video.mp4",
        audio_explanation_url="audio/path/to/audio.wav",
        manim_visualization_json=json.dumps(manim_json_data),
    )
    db_session.add(db_submission)
    db_session.commit()
    db_session.refresh(db_submission)

    response = client.get(f"/submissions/{submission_id}")
    assert response.status_code == 200
    submission_data = response.json()
    assert submission_data["submission_id"] == submission_id
    assert submission_data["manim_visualization_json"] == manim_json_data

# Test for AI analysis fields in assessment
def test_create_assessment_with_ai_fields(client, db_session):
    student = create_test_student(db_session, student_id="test_student_ai_v2")

    assessment_payload = {
        "student_id": student.student_id,
        "assessment_type": "AI_ANALYSIS",
        "source_ref_id": "sub_ai_ref_123",
        "notes": "AI-driven assessment for V2 features",
        "ai_model_version": "MetaRAG-V2.0",
        "ai_reason_code": "CONCEPT_MASTERY_INCREASE",
        "vector_data": {
            "axis1_geo": 70, "axis1_alg": 60, "axis1_ana": 75,
            "axis2_opt": 80, "axis2_piv": 65, "axis2_dia": 70,
            "axis3_con": 85, "axis3_pro": 70, "axis3_ret": 75,
            "axis4_acc": 90, "axis4_gri": 80
        }
    }

    response = client.post(
        "/assessments/",
        json=assessment_payload,
    )
    assert response.status_code == 201
    vector_history_entry = response.json()
    assert vector_history_entry["student_id"] == student.student_id
    
    # Verify the assessment record in the database
    db_assessment = db_session.query(Assessment).filter(Assessment.assessment_id == vector_history_entry["assessment_id"]).first()
    assert db_assessment is not None
    assert db_assessment.assessment_type == "AI_ANALYSIS"
    assert db_assessment.ai_model_version == "MetaRAG-V2.0"
    assert db_assessment.ai_reason_code == "CONCEPT_MASTERY_INCREASE"

def test_create_assessment_without_ai_fields(client, db_session):
    student = create_test_student(db_session, student_id="test_student_no_ai_v2")

    assessment_payload = {
        "student_id": student.student_id,
        "assessment_type": "COACH_MANUAL",
        "notes": "Manual assessment without AI fields",
        "vector_data": {
            "axis1_geo": 50, "axis1_alg": 50, "axis1_ana": 50,
            "axis2_opt": 50, "axis2_piv": 50, "axis2_dia": 50,
            "axis3_con": 50, "axis3_pro": 50, "axis3_ret": 50,
            "axis4_acc": 50, "axis4_gri": 50
        }
    }

    response = client.post(
        "/assessments/",
        json=assessment_payload,
    )
    assert response.status_code == 201
    vector_history_entry = response.json()
    assert vector_history_entry["student_id"] == student.student_id
    
    db_assessment = db_session.query(Assessment).filter(Assessment.assessment_id == vector_history_entry["assessment_id"]).first()
    assert db_assessment is not None
    assert db_assessment.assessment_type == "COACH_MANUAL"
    assert db_assessment.ai_model_version is None
    assert db_assessment.ai_reason_code is None
