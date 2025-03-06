from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from app.services.notification_service import NotificationService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])
notification_service = NotificationService()

@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, current_user: User = Depends(get_current_user)):
    if current_user.id != notification.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return notification_service.create_notification(notification)

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(current_user: User = Depends(get_current_user)):
    return notification_service.get_notifications(current_user.id)

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: str, notification: NotificationUpdate, current_user: User = Depends(get_current_user)):
    existing_notification = notification_service.get_notification(notification_id)
    if current_user.id != existing_notification.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return notification_service.update_notification(notification_id, notification)

@router.delete("/{notification_id}")
def delete_notification(notification_id: str, current_user: User = Depends(get_current_user)):
    existing_notification = notification_service.get_notification(notification_id)
    if current_user.id != existing_notification.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    notification_service.delete_notification(notification_id)
    return {"message": "Notification deleted"}
