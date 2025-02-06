from src.app.model.domain.items import CartItem
from fastapi.exceptions import HTTPException
from bson import ObjectId
from typing import Dict, List


class ItemsRepository:
    def __init__(self) -> None:
        pass

    async def insert_cart_item(self, cart_item, cart_collection):
        if not cart_item:
            raise HTTPException(status_code=400, detail="Cart item data is required")
        cart_item = CartItem(
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.price
        )
        data = await cart_collection.insert_one(cart_item.to_dict())
        if not data.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert cart item")
        return data

    async def get_cart_item(self, user_id: str, product_id: str, cart_collection) -> dict:
        if not user_id or not product_id:
            raise HTTPException(status_code=400, detail="User ID and Product ID are required")
        cart_item = await cart_collection.find_one({"user_id": user_id, "product_id": product_id})
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        return cart_item

    async def remove_cart_item(self, user_id: str, product_id: str, cart_collection):
        if not user_id or not product_id:
            raise HTTPException(status_code=400, detail="User ID and Product ID are required")
        delete_result = await cart_collection.delete_one({"user_id": user_id, "product_id": product_id})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Cart item not found or already removed")
        return {"message": "Cart item removed successfully"}

    async def get_cart_items(self, user_id: str, cart_collection) -> List[dict]:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        cursor = await cart_collection.find({"user_id": str(user_id)}).to_list()
        if not cursor:
            raise HTTPException(status_code=404, detail="No cart items found for the user")
        cart_items = []
        for document in cursor:
            document["_id"] = str(document.get("_id"))
            document["user_id"] = str(document.get("user_id"))
            document["product_id"] = str(document.get("product_id"))
            cart_items.append(document)
        return cart_items

    async def clear_cart(self, user_id: str, collection):
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        delete_result = await collection.delete_many({"user_id": str(user_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No cart items found to delete")
        return {"message": "Cart cleared successfully"}

    async def insert_order(self, order: dict, collection):
        if not order:
            raise HTTPException(status_code=400, detail="Order data is required")
        insert_result = await collection.insert_one(order)
        if not insert_result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert order")
        return insert_result

    async def get_orders(self, user_id: str, collection) -> List[dict]:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        try:
            user_oid = ObjectId(user_id)
        except Exception:
            user_oid = user_id
        cursor = await collection.find({"user_id": user_oid}).to_list()
        if not cursor:
            raise HTTPException(status_code=404, detail="No orders found for the user")
        orders = []
        for order in cursor:
            order["_id"] = str(order.get("_id"))
            order["user_id"] = str(order.get("user_id"))
            orders.append(order)
        return orders

    async def get_order_detail(self, order_id, collection):
        if not order_id:
            raise HTTPException(status_code=400, detail="Order ID is required")
        try:
            order_id = ObjectId(order_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Order ID format")
        order_details = await collection.find_one({"_id": order_id})
        if not order_details:
            raise HTTPException(status_code=404, detail="Order not found")
        order_details["_id"] = str(order_details["_id"])
        order_details["user_id"] = str(order_details["user_id"])
        return order_details
