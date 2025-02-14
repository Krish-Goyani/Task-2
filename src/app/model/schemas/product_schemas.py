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
    title: str = Field(description="The product title")
    description: str = Field(description="The product description")
    category: str = Field(description="The product category")
    price: float = Field(description="The product price (float)")
    rating: float = Field(description="The product rating (float)")
    brand: str = Field(description="The product brand")
    images: list[str] = Field(description="A list of image URLs (as JSON array)")
    thumbnail: str = Field(description="The product thumbnail URL")
