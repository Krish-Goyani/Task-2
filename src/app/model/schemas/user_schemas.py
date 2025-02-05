from pydantic import BaseModel, EmailStr
from typing import Literal
from bson import ObjectId

class User(BaseModel):
    name: str
    email: EmailStr
    password_hash: str  
    role: Literal["admin", "buyer", "seller"]  

class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str  
    role: Literal["admin", "buyer", "seller"]  
    
    
class TokenSchema(BaseModel):
    access_token: str
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None