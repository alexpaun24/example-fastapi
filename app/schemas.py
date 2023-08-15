from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class VoteChoices(IntEnum):
    upvote = 1
    downvote = 0

class User(BaseModel):
    email: EmailStr
    password: str    


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    dir: VoteChoices
    
    class Config:
        from_attributes = True
