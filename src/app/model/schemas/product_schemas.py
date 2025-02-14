from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Product(BaseModel):
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str] | None = None
    thumbnail: str | None = None
    seller_id: str

class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    rating: Optional[float]
    brand: Optional[str]
    images: Optional[List[str]]
    thumbnail: Optional[str]

class ProductLLM(BaseModel):
    title: str 
    description: str 
    category: str 
    price: float 
    rating: float
    brand: str 
    images: list[str] 
    thumbnail: str 
