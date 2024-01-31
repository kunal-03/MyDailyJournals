from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JournalBase(BaseModel):
    title: str
    content: str
    published: bool = True

class JournalCreate(JournalBase):
    pass

class Journal(JournalBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    