from fastapi import Depends, status
from src.app.repositories.items_repository import ItemsRepository
from src.app.config.database import mongodb_database
from fastapi.exceptions import HTTPException
from src.app.repositories.user_repository import UserRepository
from datetime import datetime

class CartOrderService:
    def __init__(self, items_repository=Depends(ItemsRepository), cart_collection=Depends(mongodb_database.get_cart_collection),
                 user_repository = Depends(UserRepository),
                 products_collection = Depends(mongodb_database.get_products_collection),
                 orders_collection = Depends(mongodb_database.get_orders_collection)) -> None:
        self.items_repository = items_repository
        self.cart_collection = cart_collection
        self.user_repository = user_repository
        self.orders_collection = orders_collection
        self.products_collection = products_collection
        
    async def add_item_in_cart_service(self, cart_item):
        return await self.items_repository.insert_cart_item(cart_item, self.cart_collection)

    async def remove_from_cart(self, user_id: str, product_id: str) -> bool:
        # Check if the cart item exists for the buyer.
        cart_item = await self.items_repository.get_cart_item(str(user_id), product_id, self.cart_collection)
        if not cart_item:
            return False
        # Proceed to remove the cart item.
        await self.items_repository.remove_cart_item(str(user_id), product_id, self.cart_collection)
        return True
    
    async def get_cart_items(self, user_id):
        return await self.items_repository.get_cart_items(user_id, self.cart_collection)
    
    async def place_order(self, user_id: str):
        # 1. Retrieve the buyer's cart items.
        cart_items = await self.items_repository.get_cart_items(user_id, self.cart_collection)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        order_items = []
        total_amount = 0.0

        # 2. For each cart item, look up the product to get its price.
        for item in cart_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            product = await self.user_repository.fetch_product_details(product_id, self.products_collection)
            if not product:
                # Optionally, you can choose to skip or fail if a product is missing.
                continue
            price = product.get("price", 0.0)
            order_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "price": price
            })
            total_amount += price * quantity

        # 3. Create the order document.
        order_doc = {
            "user_id": user_id,
            "items": order_items,
            "total_amount": total_amount,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # 4. Insert the order into the "orders" collection.
        await self.items_repository.insert_order(order_doc, self.orders_collection)
        # 5. Clear the buyer's cart.
        await self.items_repository.clear_cart(user_id, self.cart_collection)

        return {"message" : "Order placed successfully"}
    
    async def get_orders(self, user_id : str):
        return await self.items_repository.get_orders(user_id, self.orders_collection)
    