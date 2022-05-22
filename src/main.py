from turtle import title
from typing import AsyncIterable
from fastapi import FastAPI,status
from fastapi.params import Body
from pydantic import BaseModel
from http import HTTPStatus

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    isPublished: bool = True

@app.get("/")
async def root():
    return {"message": "Oh yeah"}

@app.post("/", status_code=status.HTTP_201_CREATED)
def createpost(rec_post: post):
    rec_post.dict()
    return {"message":rec_post}