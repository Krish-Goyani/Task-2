from pydantic import BaseModel, EmailStr
from typing import Literal

class User(BaseModel):
    name: str
    email: EmailStr
    password_hash: str  
    role: Literal["admin", "buyer", "seller"]  
    
    
    
