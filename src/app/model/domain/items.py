from bson import ObjectId
from datetime import datetime

class CartItem:
    def __init__(self, user_id: str, product_id: str, quantity: int, price: float):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
