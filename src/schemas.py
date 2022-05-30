from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class PostBase(BaseModel):
    title: str
    content: str
    ispublished: bool = True

class ResponseUserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    owner_id: int 
    created_at: datetime
    owner: ResponseUserCreate

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

