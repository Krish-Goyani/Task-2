from src.app.model.domain.items import CartItem
from fastapi.exceptions import HTTPException
from bson import ObjectId

class ItemsRepository:
    def __init__(self) -> None:
        pass
    
    
    async def insert_cart_item(self, cart_item, cart_orders_collection):
        cart_item = CartItem(user_id= cart_item.user_id,
                             product_id= cart_item.product_id,
                             quantity= cart_item.quantity,
                             price= cart_item.price)
        data = await cart_orders_collection.insert_one(cart_item.to_dict())

        return data
    
    
    async def get_cart_item(self, user_id: str, product_id: str, cart_orders_collection) -> dict:
        return await cart_orders_collection.find_one({"user_id": user_id, "product_id": product_id})

    async def remove_cart_item(self, user_id: str, product_id: str, cart_orders_collection):


        return await cart_orders_collection.delete_one({"user_id": user_id, "product_id": product_id})
            