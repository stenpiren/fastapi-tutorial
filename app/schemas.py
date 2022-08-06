from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str        


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# this class is part of schema/pydantic model which defines the structute of a request and response.
# this ensures that when the user wants to create a post, the request will only go through if it has
# a title and content in the body (published here has default value so not a must)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

# this one is used to control the structure of the response we send to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config: # this class is necessary to tell pydantic that sqlalchemy model is ORM and not dictionary
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str    

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #(one direction)