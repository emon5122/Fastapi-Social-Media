from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import *
from schemas import UserLogin
from models import *
from utils import verify
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
