from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: str  # Use id directly instead of alias _id
    user_id: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))

    class Config:
        from_attributes = True
