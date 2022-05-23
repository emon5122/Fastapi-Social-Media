from fastapi import FastAPI,status,HTTPException, Depends, Response, APIRouter
from typing import List
from sqlalchemy.orm import Session
import models
from database import  get_db
from schemas import *
from utils import *

router = APIRouter()
#Create User
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=ResponseUserCreate)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}',response_model=ResponseUserCreate)
def get_User(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found")
    
    return user