from turtle import title
from typing import AsyncIterable, Optional
from urllib.request import CacheFTPHandler
from fastapi import FastAPI,status
from fastapi.params import Body
from pydantic import BaseModel
from http import HTTPStatus
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Initializes FastAPI
app = FastAPI()
#Database Connection
while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host="database", database="FastAPI" ,user="postgres",password="sdkfhkj234ou23o4ldfsdn", cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("Connection to the database sucessful.")
        break
    except Exception as error:
        print('Failed', error)
        time.sleep(5)

class post(BaseModel):
    title: str
    content: str
    isPublished: bool = True

@app.get("/")
def root():
    return {"message": "Oh yeah"}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts """)
    posts = cur.fetchall()
    return {"Response" :posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    cur.execute("""INSERT INTO posts (title, content, isPublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.isPublished))
    new_post = cur.fetchone()
    conn.commit()
    return {"message":new_post}