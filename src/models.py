from email.policy import default
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    ispublished = Column(Boolean, default=True)
