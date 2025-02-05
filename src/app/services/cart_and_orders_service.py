from fastapi import Depends
from src.app.repositories.items_repository import ItemsRepository
from src.app.config.database import mongodb_database


class CartOrderService:
    def __init__(self, items_repository=Depends(ItemsRepository), cart_orders_collection=Depends(mongodb_database.get_cart_and_orders_collection)) -> None:
        self.items_repository = items_repository
        self.cart_orders_collection = cart_orders_collection

    async def add_item_in_cart_service(self, cart_item):
        return await self.items_repository.insert_cart_item(cart_item, self.cart_orders_collection)

    async def remove_from_cart(self, user_id: str, product_id: str) -> bool:
        # Check if the cart item exists for the buyer.
        cart_item = await self.items_repository.get_cart_item(str(user_id), product_id, self.cart_orders_collection)
        if not cart_item:
            return False
        # Proceed to remove the cart item.
        await self.items_repository.remove_cart_item(str(user_id), product_id, self.cart_orders_collection)
        return True
