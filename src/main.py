from http.client import HTTPException
from operator import mod
from fastapi import FastAPI,status,HTTPException, Depends, Response
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import false
from sqlalchemy.orm import Session
import time
import models
from database import  engine, get_db
from schemas import post

#SQLAlchemy Creates Tables on database
models.Base.metadata.create_all(bind=engine)

#Initializes FastAPI
app = FastAPI()

#Database Connection without using ORM
# while True:
#     try:
#         # Connect to your postgres DB
#         conn = psycopg2.connect(host="database", database="FastAPI" ,user="postgres",password="sdkfhkj234ou23o4ldfsdn", cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         print("Connection to the database sucessful.")
#         break
#     except Exception as error:
#         print('Failed', error)
#         time.sleep(5)

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return {"Response" :posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: post, db: Session = Depends(get_db)):
    # cur.execute("""INSERT INTO posts (title, content, ispublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.ispublished))
    # new_post = cur.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, ispublished=post.ispublished)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Response":new_post}

@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT title,content FROM posts WHERE id=%s """, (str(id)) )
    # post = cur.fetchone() 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"Post Details":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    # deleted_post=cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                            detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_by_id(id:int, updated_post:post, db: Session = Depends(get_db)):
    # cur.execute("""UPDATE posts SET title=%s,content=%s,ispublished=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.ispublished,(str(id))))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"Post Details":post_query.first()}
