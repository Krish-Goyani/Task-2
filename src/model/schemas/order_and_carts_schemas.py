from pydantic import BaseModel
from typing import List, Literal
from bson import ObjectId

class CartItem(BaseModel):
    user_id: ObjectId
    product_id: ObjectId
    quantity: int
    
    

class OrderItem(BaseModel): # ---> structure
    product_id: ObjectId
    quantity: int
    price: float

class Order(BaseModel): # ---> Schema
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: Literal["pending", "shipped", "delivered", "cancelled"]