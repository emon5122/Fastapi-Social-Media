from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    ispublished: bool = True

class CreatePost(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True