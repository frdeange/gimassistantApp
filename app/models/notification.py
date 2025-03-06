from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
