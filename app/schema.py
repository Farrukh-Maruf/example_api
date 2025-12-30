from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    title: str
    content: str
    published: bool    ##postbase da bolgani uchun  yozish shart emas
    created_at: datetime
    owner_id: int
    owner: 'UserOut'   # bu yerda UserOut ni string qilib yozamiz, chunki UserOut hali aniqlanmagan, va u pastda joylashgan

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    vote_count: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email:EmailStr
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
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore # 1 - like, 0 - dislike