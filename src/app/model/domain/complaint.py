from bson import ObjectId
from datetime import datetime

class Complaint:
    def __init__(self, user_id: str, order_id: str, product_id: str, issue : str, image_url : str, status :  str):
        self.user_id: str = user_id
        self.order_id: str =order_id
        self.product_id: str = product_id
        self.issue: str = issue
        self.image_url: str = image_url
        self.status: str = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "issue": self.issue,
            "image_url": self.image_url,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
