from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime
from typing import Optional




class UserOut(BaseModel):
    # model_config = ConfigDict(from_attributes=True) #advanced and newer version of the class config ..
    id:int
    email:EmailStr
    created_at: datetime
    class Config:   # older version from Pydantic V1
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass 



# response model 
class Post(PostBase): 
    id: int
    created_at: datetime
    owner_id : int 
    owner : UserOut
    # title: str
    # content: str
    # published: bool no need all are inherited

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr #imported from pydantic needs email-validator library 
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[int] = None

class Vote(BaseModel):
    post_id : int
    direction : int #conint(le=1)  # 1 for upvote and 0 for downvote 
    # conint is used to set constraint on int like here le =1 -> less than equal to 1

