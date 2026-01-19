#this file creates the models (tables) in the database for all the models and further columns for those tables 
from .database import Base  #.database = look for database in same folder; from database import Base - will break
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class Post(Base):
    __tablename__ = "posts"
    
    #column_name = column(Data Type, other params)
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"),nullable=False)
    owner = relationship("User") #relationship b/w Post and User models


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True)