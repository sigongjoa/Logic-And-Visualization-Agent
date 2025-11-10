from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Literal

from .. import schemas
from ..main import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

# Dummy user data for demonstration
dummy_user_student = schemas.UserMe(
    user_id="user_123",
    username="student_user",
    email="student@example.com",
    user_type="student"
)

dummy_user_coach = schemas.UserMe(
    user_id="coach_456",
    username="coach_user",
    email="coach@example.com",
    user_type="coach"
)

# Dummy notification settings
dummy_notification_settings = schemas.UserNotificationUpdate(
    new_assignments=True,
    feedback_from_coach=True,
    platform_updates=False
)

@router.get("/me", response_model=schemas.UserMe)
async def get_current_user_profile(db: Session = Depends(get_db)):
    # In a real app, this would get the authenticated user's ID
    # and fetch their profile from the database.
    # For now, we'll return a dummy user based on a hypothetical user type.
    # This needs to be integrated with actual authentication later.
    current_user_type = "student" # This would come from the auth token
    if current_user_type == "student":
        return dummy_user_student
    elif current_user_type == "coach":
        return dummy_user_coach
    raise HTTPException(status_code=401, detail="Not authenticated")

@router.put("/me", response_model=schemas.UserMe)
async def update_current_user_profile(user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    # Placeholder for updating user profile
    current_user_type = "student" # This would come from the auth token
    if current_user_type == "student":
        if user_update.username:
            dummy_user_student.username = user_update.username
        if user_update.email:
            dummy_user_student.email = user_update.email
        return dummy_user_student
    elif current_user_type == "coach":
        if user_update.username:
            dummy_user_coach.username = user_update.username
        if user_update.email:
            dummy_user_coach.email = user_update.email
        return dummy_user_coach
    raise HTTPException(status_code=401, detail="Not authenticated")

@router.put("/me/password")
async def update_current_user_password(password_update: schemas.UserPasswordUpdate, db: Session = Depends(get_db)):
    # Placeholder for password update logic
    if password_update.new_password != password_update.confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    # In a real app, verify current_password, hash new_password, and update in DB
    print(f"Password for user updated. New password: {password_update.new_password}")
    return {"message": "Password updated successfully"}

@router.put("/me/notifications", response_model=schemas.UserNotificationUpdate)
async def update_current_user_notifications(notification_update: schemas.UserNotificationUpdate, db: Session = Depends(get_db)):
    # Placeholder for updating notification preferences
    dummy_notification_settings.new_assignments = notification_update.new_assignments
    dummy_notification_settings.feedback_from_coach = notification_update.feedback_from_coach
    dummy_notification_settings.platform_updates = notification_update.platform_updates
    return dummy_notification_settings

@router.delete("/me")
async def deactivate_current_user_account(db: Session = Depends(get_db)):
    # Placeholder for account deactivation logic
    print("User account deactivated.")
    return {"message": "Account deactivated successfully"}
