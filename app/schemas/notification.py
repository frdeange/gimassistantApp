from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class NotificationBase(BaseModel):
    user_id: str
    message: str
    read: bool = False

class NotificationCreate(NotificationBase):
    created_at: Optional[str] = None  # Add created_at field as an optional string

class NotificationUpdate(NotificationBase):
    read: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
