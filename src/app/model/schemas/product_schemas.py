from pydantic import BaseModel
from typing import List
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
