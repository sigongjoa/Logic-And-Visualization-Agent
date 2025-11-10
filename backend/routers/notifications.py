from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Literal

from .. import schemas
from ..main import get_db

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)

# Dummy data for demonstration
dummy_notifications = [
    schemas.Notification(
        notification_id="notif_001",
        user_id="user_123",
        type="assignment_graded",
        title="Grade Posted: Data Structures Intro",
        message="Your submission for 'Data Structures Intro' has been graded. Your score is 95/100.",
        created_at=datetime.now() - timedelta(hours=2),
        is_read=False,
        related_id="sub_001"
    ),
    schemas.Notification(
        notification_id="notif_002",
        user_id="user_123",
        type="new_feedback",
        title="New Feedback: Algorithm Design",
        message="You have new feedback from Coach Turing on 'Algorithm Design'.",
        created_at=datetime.now() - timedelta(days=1),
        is_read=False,
        related_id="sub_002"
    ),
    schemas.Notification(
        notification_id="notif_003",
        user_id="user_123",
        type="new_student",
        title="New Student Assigned: Jane Doe",
        message="Jane Doe has been added to your roster.",
        created_at=datetime.now() - timedelta(days=2),
        is_read=True,
        related_id="student_jane"
    ),
    schemas.Notification(
        notification_id="notif_004",
        user_id="user_123",
        type="new_submission",
        title="New Submission: Advanced Algorithms",
        message="John Smith submitted 'Advanced Algorithms'.",
        created_at=datetime.now() - timedelta(days=3),
        is_read=True,
        related_id="sub_003"
    ),
]

@router.get("/", response_model=List[schemas.Notification])
async def get_notifications(db: Session = Depends(get_db)):
    # In a real application, this would fetch notifications from the database
    # filtered by the authenticated user.
    return dummy_notifications

@router.put("/{notification_id}/read")
async def mark_notification_as_read(notification_id: str, db: Session = Depends(get_db)):
    # Placeholder logic: find notification and mark as read
    for notif in dummy_notifications:
        if notif.notification_id == notification_id:
            notif.is_read = True
            return {"message": f"Notification {notification_id} marked as read"}
    raise HTTPException(status_code=404, detail="Notification not found")

@router.put("/mark-all-read")
async def mark_all_notifications_as_read(db: Session = Depends(get_db)):
    # Placeholder logic: mark all notifications for the user as read
    for notif in dummy_notifications:
        notif.is_read = True
    return {"message": "All notifications marked as read"}
