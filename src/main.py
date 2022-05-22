from http.client import HTTPException
from fastapi import FastAPI,status,Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
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
    ispublished: bool = True

@app.get("/")
def root():
    return {"message": "That just works!"}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts """)
    posts = cur.fetchall()
    return {"Response" :posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    cur.execute("""INSERT INTO posts (title, content, ispublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.ispublished))
    new_post = cur.fetchone()
    conn.commit()
    return {"Response":new_post}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cur.execute("""SELECT title,content FROM posts WHERE id=%s """, (str(id)) )
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"Post Details":post}