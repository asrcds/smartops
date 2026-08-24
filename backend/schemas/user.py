from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, constr

class UserBase(BaseModel):
    username: constr(min_length=3)
    email: Optional[EmailStr] = None
    password: constr(min_length=6)

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserResponse(UserBase):
    id: int
    role: str
    create_time: datetime

    class Config:
        orm_mode = True
