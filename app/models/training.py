from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Training(BaseModel):
    id: str = Field(..., alias="_id")
    trainer_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    status: str

class Availability(BaseModel):
    id: str = Field(..., alias="_id")
    trainer_id: str
    center_id: str
    available_times: List[datetime]
