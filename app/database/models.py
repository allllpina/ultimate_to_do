from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: str
    category: int
    duration: int
    date_of_deadline: datetime
    date_of_creation: Optional[datetime] = datetime.now()
    description_length: int
    priority: int

    class Config:
        orm_mode = True