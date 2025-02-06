from src.app.model.domain.items import CartItem
from fastapi.exceptions import HTTPException
from bson import ObjectId
from typing import Dict, List

class ItemsRepository:
    def __init__(self) -> None:
        pass
    
    
    async def insert_cart_item(self, cart_item, cart_collection):
        cart_item = CartItem(user_id= cart_item.user_id,
                             product_id= cart_item.product_id,
                             quantity= cart_item.quantity,
                             price= cart_item.price)
        data = await cart_collection.insert_one(cart_item.to_dict())

        return data
    
    
    async def get_cart_item(self, user_id: str, product_id: str, cart_collection) -> dict:
        return await cart_collection.find_one({"user_id": user_id, "product_id": product_id})

    async def remove_cart_item(self, user_id: str, product_id: str, cart_collection):

        return await cart_collection.delete_one({"user_id": user_id, "product_id": product_id})
    
    async def get_cart_items(self,user_id: str, cart_collection) -> List[dict]:
        try:
            user_oid = str(user_id)
        except Exception:
            return []
        # Find all documents in the "carts" collection matching the given user_id.
        cursor = await cart_collection.find({"user_id": user_oid}).to_list()
        cart_items = []
        for document in cursor:
            # Convert ObjectIds to string
            document["_id"] = str(document.get("_id"))
            document["user_id"] = str(document.get("user_id"))
            document["product_id"] = str(document.get("product_id"))
            cart_items.append(document)
        return cart_items
                        
    async def clear_cart(self, user_id: str, collection):
        return await collection.delete_many({"user_id": str(user_id)})
        
    async def insert_order(self, order: dict, collection):
        return await collection.insert_one(order)
        
        
    async def get_orders(self, user_id: str, collection) -> List[dict]:
        try:
            # Convert user_id to ObjectId for the query if necessary.
            user_oid = ObjectId(user_id)
        except Exception:
            # If conversion fails, assume user_id is stored as a string.
            user_oid = user_id

        cursor = await collection.find({"user_id": user_oid}).to_list()
        orders = []
        for order in cursor:
            order["_id"] = str(order.get("_id"))
            order["user_id"] = str(order.get("user_id"))
            orders.append(order)
        return orders
    
    async def get_order_detail(self, order_id,collection):
        order_details = await collection.find_one({"_id" : ObjectId(order_id)})
        order_details["_id"] = str(order_details["_id"])
        order_details["user_id"] = str(order_details["user_id"])
        return order_details
        