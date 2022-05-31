from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    ispublished = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete= "CASCADE"), nullable=False)

    owner = relationship("User")

class Like(Base):
    __tablename__ = "likes"

    post_id =  Column(Integer, ForeignKey("posts.id",ondelete= "CASCADE"),  primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete= "CASCADE"),  primary_key=True)