from fastapi.testclient import TestClient
from ..main import app
from ..routers.users import dummy_user_student, dummy_user_coach, dummy_notification_settings

client = TestClient(app)

def test_get_current_user_profile_student():
    # Assuming the router's get_current_user_profile returns dummy_user_student by default
    response = client.get("/users/me")
    assert response.status_code == 200
    user_profile = response.json()
    assert user_profile["user_id"] == dummy_user_student.user_id
    assert user_profile["username"] == dummy_user_student.username
    assert user_profile["email"] == dummy_user_student.email
    assert user_profile["user_type"] == dummy_user_student.user_type

def test_update_current_user_profile():
    update_data = {"username": "updated_student", "email": "updated_student@example.com"}
    response = client.put("/users/me", json=update_data)
    assert response.status_code == 200
    updated_profile = response.json()
    assert updated_profile["username"] == update_data["username"]
    assert updated_profile["email"] == update_data["email"]
    # Verify the dummy data is actually updated (due to direct import)
    assert dummy_user_student.username == update_data["username"]
    assert dummy_user_student.email == update_data["email"]

def test_update_current_user_password_success():
    password_data = {
        "current_password": "old_password", # Dummy, not checked in router
        "new_password": "new_secure_password",
        "confirm_new_password": "new_secure_password"
    }
    response = client.put("/users/me/password", json=password_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

def test_update_current_user_password_mismatch():
    password_data = {
        "current_password": "old_password",
        "new_password": "new_secure_password",
        "confirm_new_password": "mismatched_password"
    }
    response = client.put("/users/me/password", json=password_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "New passwords do not match"

def test_update_current_user_notifications():
    notification_data = {
        "new_assignments": False,
        "feedback_from_coach": True,
        "platform_updates": True
    }
    response = client.put("/users/me/notifications", json=notification_data)
    assert response.status_code == 200
    updated_notifications = response.json()
    assert updated_notifications["new_assignments"] == notification_data["new_assignments"]
    assert updated_notifications["feedback_from_coach"] == notification_data["feedback_from_coach"]
    assert updated_notifications["platform_updates"] == notification_data["platform_updates"]
    # Verify the dummy data is actually updated
    assert dummy_notification_settings.new_assignments == notification_data["new_assignments"]
    assert dummy_notification_settings.feedback_from_coach == notification_data["feedback_from_coach"]
    assert dummy_notification_settings.platform_updates == notification_data["platform_updates"]

def test_deactivate_current_user_account():
    response = client.delete("/users/me")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deactivated successfully"
