from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class NotificationBase(BaseModel):
    user_id: str
    message: str
    read: bool = False

class NotificationCreate(NotificationBase):
    created_at: Optional[datetime] = None

    @field_validator('created_at', mode='before')
    def set_created_at(cls, v):
        return v or datetime.now(timezone.utc)

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})  # Convierte datetime a string

class NotificationUpdate(NotificationBase):
    read: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})  # Convierte datetime a string 
