from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True