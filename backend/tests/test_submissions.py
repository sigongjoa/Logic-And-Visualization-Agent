from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models, crud
from backend.models import Base
from sqlalchemy import create_engine
from datetime import datetime, timedelta, UTC # Added UTC
from unittest.mock import patch # Added patch

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

@patch('backend.crud.requests.post')
def test_create_submission(mock_post):
    # Configure the mock to return a specific response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "concept_id": "C_이차함수",
        "logical_path_text": "LLM analysis: The problem '이차함수와 그래프' is about quadratic functions. Key steps involve identifying the vertex, roots, and graph properties.",
        "vector_data": {
            "axis1_geo": 50, "axis1_alg": 65, "axis1_ana": 50,
            "axis2_opt": 55, "axis2_piv": 50, "axis2_dia": 50,
            "axis3_con": 60, "axis3_pro": 55, "axis3_ret": 50,
            "axis4_acc": 60, "axis4_gri": 50,
        }
    }

    # 1. Setup: Create a student, curriculum, and concept
    db = TestingSessionLocal()
    # Clear ConceptsLibrary to ensure a clean state
    db.query(models.ConceptsLibrary).delete()
    db.commit()

    student_id = "std_testuser_submission"
    curriculum_id = "MATH-01"
    concept_id = "C_이차함수" # Use the correct concept_id from knowledge graph

    # Ensure student exists (or create if not)
    if not db.query(models.Student).filter_by(student_id=student_id).first():
        db.add(models.Student(student_id=student_id, student_name="Test Student"))
        db.commit()

    # Clean up previous test data for StudentMastery
    db.query(models.StudentMastery).filter_by(student_id=student_id, concept_id=concept_id).delete()
    db.commit()

    # Create Curriculum
    if not db.query(models.Curriculum).filter_by(curriculum_id=curriculum_id).first():
        db.add(models.Curriculum(curriculum_id=curriculum_id, curriculum_name="Middle School Math"))
        db.commit()

    # Create Concept
    if not db.query(models.ConceptsLibrary).filter_by(concept_id=concept_id).first():
        db.add(models.ConceptsLibrary(
            concept_id=concept_id,
            curriculum_id="M-ALL",
            concept_name="이차함수와 그래프",
            manim_data_path="http://example.com/manim/C_이차함수"
        ))
        db.commit()
    db.close()

    # 2. Define the test data
    submission_data = {
        "student_id": student_id,
        "problem_text": "이차함수와 그래프",
    }

    # 3. Call the API endpoint
    response = client.post("/submissions", json=submission_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert "submission_id" in data
    assert data["logical_path_text"] == "LLM analysis: The problem '이차함수와 그래프' is about quadratic functions. Key steps involve identifying the vertex, roots, and graph properties."
    assert data["concept_id"] == "C_이차함수" # Assert the correct concept_id based on the problem text
    assert data["manim_content_url"] == "http://example.com/manim/C_이차함수"

    # 5. Verify the data in the database (Submission and StudentMastery)
    db = TestingSessionLocal()
    submission_entry = db.query(models.Submission).filter_by(submission_id=data["submission_id"]).first()
    assert submission_entry is not None
    assert submission_entry.student_id == student_id
    assert submission_entry.status == "PENDING"

    mastery_entry = db.query(models.StudentMastery).filter_by(student_id=student_id, concept_id="C_이차함수").first()
    assert mastery_entry is not None
    assert mastery_entry.mastery_score == 70 # Assuming a mock mastery score update
    assert mastery_entry.status == "IN_PROGRESS" # Status should be IN_PROGRESS
    assert mastery_entry.last_updated is not None

    # Verify LLMLog entry
    llm_log_entry = db.query(models.LLMLog).filter_by(source_submission_id=data["submission_id"]).first()
    assert llm_log_entry is not None
    assert llm_log_entry.decision == "ANALYSIS_COMPLETE"
    assert llm_log_entry.model_version == "V1_LLM_INTEGRATION" # Updated model version

    # Verify AnkiCard entry
    anki_card_entry = db.query(models.AnkiCard).filter_by(student_id=student_id, llm_log_id=llm_log_entry.log_id).first()
    assert anki_card_entry is not None
    assert anki_card_entry.question.startswith("What is the key concept related to '이차함수와 그래프'?")
    assert anki_card_entry.answer.startswith("The problem is primarily about 'C_이차함수'")
    assert anki_card_entry.next_review_date is not None
    db.close()

@patch('backend.crud.requests.post')
def test_create_submission_and_update_vector(mock_post):
    # Configure the mock to return a specific response for the second test
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "concept_id": "C_피타고라스",
        "logical_path_text": "LLM analysis: The problem '피타고라스의 정리' applies the Pythagorean theorem. Focus on identifying right triangles and side lengths.",
        "vector_data": {
            "axis1_geo": 65, "axis1_alg": 50, "axis1_ana": 50,
            "axis2_opt": 50, "axis2_piv": 55, "axis2_dia": 50,
            "axis3_con": 55, "axis3_pro": 60, "axis3_ret": 50,
            "axis4_acc": 50, "axis4_gri": 60,
        }
    }

    # 1. Setup: Create a student, curriculum, and concept
    db = TestingSessionLocal()
    # Clear ConceptsLibrary to ensure a clean state
    db.query(models.ConceptsLibrary).delete()
    db.commit()

    student_id = "std_testuser_vector"
    concept_id = "C_피타고라스" # Use the correct concept_id from knowledge graph

    # Ensure student exists (or create if not)
    if not db.query(models.Student).filter_by(student_id=student_id).first():
        db.add(models.Student(student_id=student_id, student_name="Test Vector Student"))
        db.commit()

    # Create an initial vector for the student
    initial_vector = models.StudentVectorHistory(
        vector_id="vec_initial_2",
        assessment_id="asmt_initial_2",
        student_id=student_id,
        created_at=datetime.now(UTC) - timedelta(days=10), # Set to an older date
        axis1_geo=60, axis1_alg=60, axis1_ana=60,
        axis2_opt=60, axis2_piv=60, axis2_dia=60,
        axis3_con=60, axis3_pro=60, axis3_ret=60,
        axis4_acc=60, axis4_gri=60,
    )
    # Clean up previous vector history
    db.query(models.StudentVectorHistory).filter_by(student_id=student_id).delete()
    db.add(initial_vector)
    db.commit()

    # Create Concept
    if not db.query(models.ConceptsLibrary).filter_by(concept_id=concept_id).first():
        db.add(models.ConceptsLibrary(
            concept_id=concept_id,
            curriculum_id="M-ALL",
            concept_name="피타고라스의 정리",
            manim_data_path="http://example.com/manim/C_피타고라스"
        ))
        db.commit()
    db.close()

    # 2. Define the test data
    submission_data = {
        "student_id": student_id,
        "problem_text": "피타고라스의 정리",
    }

    # 3. Call the API endpoint
    response = client.post("/submissions", json=submission_data)

    # 4. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["concept_id"] == "C_피타고라스"
    assert data["logical_path_text"] == "LLM analysis: The problem '피타고라스의 정리' applies the Pythagorean theorem. Focus on identifying right triangles and side lengths."


    # 5. Verify the vector was updated
    db.close() # Close the session used for setup
    db = TestingSessionLocal() # Open a new session to ensure latest data
    new_vector = db.query(models.StudentVectorHistory).filter(
        models.StudentVectorHistory.student_id == student_id
    ).order_by(models.StudentVectorHistory.created_at.desc()).first()

    assert new_vector is not None
    assert new_vector.vector_id != "vec_initial_2"
    assert new_vector.axis1_geo == 65 # Updated expected value
    assert new_vector.axis3_pro == 60 # Updated expected value
    assert new_vector.axis4_acc == 50 # Updated expected value

    # Verify LLMLog entry
    llm_log_entry = db.query(models.LLMLog).filter_by(source_submission_id=data["submission_id"]).first()
    assert llm_log_entry is not None
    assert llm_log_entry.decision == "ANALYSIS_COMPLETE"
    assert llm_log_entry.model_version == "V1_LLM_INTEGRATION" # Updated model version

    # Verify AnkiCard entry
    anki_card_entry = db.query(models.AnkiCard).filter_by(student_id=student_id, llm_log_id=llm_log_entry.log_id).first()
    assert anki_card_entry is not None
    assert anki_card_entry.question.startswith("What is the key concept related to '피타고라스의 정리'?")
    assert anki_card_entry.answer.startswith("The problem is primarily about 'C_피타고라스'")
    assert anki_card_entry.next_review_date is not None
    db.close()
