from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base, StudentVectorHistory

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

def test_create_assessment():
    # 1. Define the test data
    assessment_data = {
        "student_id": "std_testuser",
        "assessment_type": "COACH_MANUAL",
        "notes": "Test assessment from pytest",
        "vector_data": {
            "axis1_geo": 50,
            "axis1_alg": 55,
            "axis1_ana": 60,
            "axis2_opt": 65,
            "axis2_piv": 70,
            "axis2_dia": 75,
            "axis3_con": 80,
            "axis3_pro": 85,
            "axis3_ret": 90,
            "axis4_acc": 95,
            "axis4_gri": 100,
        },
    }

    # 2. Call the API endpoint
    response = client.post("/assessments", json=assessment_data)

    # 3. Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == "std_testuser"
    assert data["axis4_gri"] == 100

    # 4. Verify the data in the database
    db = TestingSessionLocal()
    history_entry = db.query(StudentVectorHistory).filter_by(assessment_id=data["assessment_id"]).first()
    assert history_entry is not None
    assert history_entry.student_id == "std_testuser"
    assert history_entry.axis4_gri == 100
    db.close()
