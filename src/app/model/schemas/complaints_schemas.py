from pydantic import BaseModel
from typing import List, Literal
from bson import ObjectId



class Complaint(BaseModel):
    user_id: ObjectId
    order_id: ObjectId
    product_id: ObjectId
    issue: str
    image_url: str
    status: Literal["open", "rejected"]