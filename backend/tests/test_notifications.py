from fastapi.testclient import TestClient
from ..main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_get_notifications():
    response = client.get("/notifications/")
    assert response.status_code == 200
    notifications = response.json()
    assert isinstance(notifications, list)
    assert len(notifications) > 0
    assert "notification_id" in notifications[0]
    assert "title" in notifications[0]
    assert "is_read" in notifications[0]

def test_mark_notification_as_read():
    # First, get notifications to find an unread one
    get_response = client.get("/notifications/")
    notifications = get_response.json()
    
    unread_notification_id = None
    for notif in notifications:
        if not notif["is_read"]:
            unread_notification_id = notif["notification_id"]
            break
    
    if unread_notification_id:
        response = client.put(f"/notifications/{unread_notification_id}/read")
        assert response.status_code == 200
        assert response.json()["message"] == f"Notification {unread_notification_id} marked as read"
        
        # Verify it's marked as read (re-fetch notifications)
        get_response_after_read = client.get("/notifications/")
        updated_notifications = get_response_after_read.json()
        for notif in updated_notifications:
            if notif["notification_id"] == unread_notification_id:
                assert notif["is_read"] == True
                break
    else:
        # If all dummy notifications are already read, this test might pass without marking anything
        # For robust testing, ensure dummy data has unread notifications
        pass

def test_mark_all_notifications_as_read():
    response = client.put("/notifications/mark-all-read")
    assert response.status_code == 200
    assert response.json()["message"] == "All notifications marked as read"
    
    # Verify all are marked as read
    get_response = client.get("/notifications/")
    notifications = get_response.json()
    for notif in notifications:
        assert notif["is_read"] == True

def test_mark_nonexistent_notification_as_read():
    response = client.put("/notifications/nonexistent_id/read")
    assert response.status_code == 404
    assert response.json()["detail"] == "Notification not found"
