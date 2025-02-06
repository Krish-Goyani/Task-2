from pydantic import BaseModel
from typing import List, Literal
from bson import ObjectId



class Complaint(BaseModel):
    user_id: str
    order_id: str
    product_id: str
    issue: str
    image_url: str = ""
    status: Literal["open", "rejected"]