from pydantic import BaseModel

class post(BaseModel):
    title: str
    content: str
    ispublished: bool = True
