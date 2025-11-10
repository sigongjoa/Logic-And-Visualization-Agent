from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..main import app

client = TestClient(app)

def test_successful_student_login():
    response = client.post(
        "/auth/login",
        json={"email_or_username": "test", "password": "test", "user_type": "student"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] == "dummy_student_token"

def test_successful_coach_login():
    response = client.post(
        "/auth/login",
        json={"email_or_username": "test", "password": "test", "user_type": "coach"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] == "dummy_coach_token"

def test_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"email_or_username": "wrong", "password": "credentials", "user_type": "student"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password or user type"

def test_invalid_user_type():
    response = client.post(
        "/auth/login",
        json={"email_or_username": "test", "password": "test", "user_type": "admin"}
    )
    assert response.status_code == 422 # Unprocessable Entity due to Pydantic validation
    assert "Input should be 'student' or 'coach'" in response.json()["detail"][0]["msg"]
