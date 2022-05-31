from fastapi import status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
# import models
from database import  get_db
from schemas import *
from utils import *
from oauth2 import get_current_user

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: like, db: Session =  Depends(get_db), current_user: int = Depends(get_current_user)):
    like_query = db.query(like).filter(like.post_id == like.post_id, like.user_id == current_user.id)
    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user} has already liked post: {like.post_id}")
        new_like = like(post_id = like.post.id , user_id=current_user.id)
        db.add(new_like)
        db.commit()
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No like found")
        
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Unliked the post"}