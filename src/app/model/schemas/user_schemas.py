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
    
    
    {'_id': ObjectId('67a4372572e5a3fefc38d9e0'), 'name': 'string', 'email': 'new@example.com', 'password_hash': '$2b$12$FCX/BcUKDxZnYK33v4gvJOvW8T6Q2t8S7WvjZkaD3dKhcQ9fUfowa', 'role': 'buyer', 
     'created_at': '2025-02-06T04:14:29.242735', 'updated_at': '2025-02-06T04:14:29.242741'}
class UserOut(BaseModel):
    _id : str
    name : str
    email : EmailStr
    role :  Literal["admin", "buyer", "seller"]
class TokenSchema(BaseModel):
    access_token: str
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None