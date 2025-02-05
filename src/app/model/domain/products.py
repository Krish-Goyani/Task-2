from bson import ObjectId
from datetime import datetime
from typing import List


class Product:
    def __init__(
        self,
        title: str,
        description: str,
        category: str,
        price: float,
        rating: float,
        brand: str,
        images: List[str] | None = None,
        thumbnail: str | None = None,
        seller_id: ObjectId = ObjectId("000000000000000000000000")
    ):
        self._id = ObjectId()
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.rating = rating
        self.brand = brand
        self.images = images
        self.thumbnail = thumbnail
        self.seller_id = seller_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "brand": self.brand,
            "images": self.images,
            "thumbnail": self.thumbnail,
            "seller_id": str(self.seller_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
