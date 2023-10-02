from pydantic import BaseModel
from typing import List

#pydantic model for creating a blog post
class BlogCreateBase(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True
        
class BlogCreate(BlogCreateBase):
    class Config():
        orm_mode = True


# Pydantic models for creating a user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
 
    
# Pydantic models for showing a user
class ShowUser(BaseModel):
    name: str
    email: str
    blogs : List[BlogCreate] = []
    class Config():
        orm_mode = True

# Pydantic models for showing a blog post
class ShowBlog(BaseModel):
    title: str
    body: str
    creator_id: ShowUser
    class Config():
        orm_mode = True


# Pydantic models for login
class Login(BaseModel):
    email: str
    password: str
    class Config():
        orm_mode = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config():
        orm_mode = True
        
        
class TokenData(BaseModel):
    email: str = None
    class Config():
        orm_mode = True