from tarfile import LinkFallbackError
import email_validator
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


#inherating from PostBase

class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr


    #converting pydantic model to dict
    class Config:
        orm_mode = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase): # controlling the output data 
    id : int # optional for viewing 
    created_at: datetime 
    owner_id: int
    owner: UserOut

    #converting pydantic model to dict
    class Config:
        orm_mode = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    Post: Post
    likes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    name: str

class Vote(BaseModel):
    post_id: int
    dir: bool