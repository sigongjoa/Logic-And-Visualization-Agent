from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from backend.main import app, get_db
from backend import models
from sqlalchemy import create_engine

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

def test_get_vector_history():
    # 1. Setup: Create a student and some vector history
    db = TestingSessionLocal()
    student_id = "std_history_user"
    # Clean up previous test data
    db.query(models.StudentVectorHistory).filter_by(student_id=student_id).delete()
    db.commit()

    history1 = models.StudentVectorHistory(
        vector_id="vec_1", assessment_id="asmt_1", student_id=student_id,
        axis1_geo=10, axis1_alg=10, axis1_ana=10, axis2_opt=10, axis2_piv=10,
        axis2_dia=10, axis3_con=10, axis3_pro=10, axis3_ret=10, axis4_acc=10, axis4_gri=10
    )
    history2 = models.StudentVectorHistory(
        vector_id="vec_2", assessment_id="asmt_2", student_id=student_id,
        axis1_geo=20, axis1_alg=20, axis1_ana=20, axis2_opt=20, axis2_piv=20,
        axis2_dia=20, axis3_con=20, axis3_pro=20, axis3_ret=20, axis4_acc=20, axis4_gri=20
    )
    db.add_all([history1, history2])
    db.commit()
    db.close()

    # 2. Call the API endpoint
    response = client.get(f"/students/{student_id}/vector-history")

    # 3. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["student_id"] == student_id
    assert data[0]["axis1_geo"] == 10
    assert data[1]["axis1_geo"] == 20
