
from fastapi import FastAPI,status,HTTPException, Depends, Response, APIRouter
from typing import List
from sqlalchemy.orm import Session
import models
from database import  get_db
from schemas import *
from utils import *
from oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
#Returns all posts
@router.get("/", response_model=List[ResponsePost])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts

#Returns specefic post
@router.get("/{id}", response_model=ResponsePost)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT title,content FROM posts WHERE id=%s """, (str(id)) )
    # post = cur.fetchone() 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

#Creates Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_posts(post: CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    # cur.execute("""INSERT INTO posts (title, content, ispublished) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.ispublished))
    # new_post = cur.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, ispublished=post.ispublished)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Updates specefic post and returns updated value
@router.put("/{id}", response_model=ResponsePost)
def update_by_id(id:int, updated_post:CreatePost, db: Session = Depends(get_db)):
    # cur.execute("""UPDATE posts SET title=%s,content=%s,ispublished=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.ispublished,(str(id))))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

#Delete Specefic Post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
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
