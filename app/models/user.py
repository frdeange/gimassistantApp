from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: str
    hashed_password: str
    roles: List[str] = []

    class Config:
        from_attributes = True

class Trainer(User):
    availability: List[str] = []

class Admin(User):
    pass
