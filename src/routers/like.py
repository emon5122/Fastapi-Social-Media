from fastapi import status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import  get_db
import schemas
import models
from utils import *
from oauth2 import get_current_user

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(likes: schemas.Like, db: Session =  Depends(get_db), current_user: int = Depends(get_current_user)):
    like_query = db.query(models.Like).filter(models.Like.post_id == likes.post_idd, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if (likes.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user} has already liked post: {schemas.like.post_id}")
        new_like = models.Like(post_id = likes.post.id , user_id=current_user.id)
        db.add(new_like)
        db.commit()
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No like found")
        
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Unliked the post"}