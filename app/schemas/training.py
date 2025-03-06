from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TrainingBase(BaseModel):
    trainer_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    status: str

class TrainingCreate(TrainingBase):
    pass

class TrainingUpdate(TrainingBase):
    pass

class TrainingResponse(TrainingBase):
    id: str

    class Config:
        from_attributes = True

class AvailabilityBase(BaseModel):
    trainer_id: str
    center_id: str
    available_times: List[datetime]

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityUpdate(AvailabilityBase):
    pass

class AvailabilityResponse(AvailabilityBase):
    id: str

    class Config:
        from_attributes = True
