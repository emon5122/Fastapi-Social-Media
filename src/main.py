from fastapi import FastAPI,status,HTTPException, Depends, Response
from fastapi.params import Body
import models
from database import  engine, get_db
from routers import post,user


#SQLAlchemy Creates Tables on database
models.Base.metadata.create_all(bind=engine)

#Initializes FastAPI
app = FastAPI()

#Routers
app.include_router(post.router)
app.include_router(user.router)