from src.app.services.cart_and_orders_service import CartOrderService
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from src.app.model.schemas.order_and_carts_schemas import Order
from typing import List
class CartOrdersUsecase:
    def __init__(self, cart_order_service=Depends(CartOrderService)) -> None:
        self.cart_order_service = cart_order_service

    async def add_item_in_cart_usecase(self, cart_item):
        return await self.cart_order_service.add_item_in_cart_service(cart_item)

    async def remove_from_cart(self,  current_user, product_id: str,) -> dict:
        # Delegate the removal operation to the service layer.
        removed = await self.cart_order_service.remove_from_cart(current_user["_id"], product_id)
        if not removed:
            # If the cart item was not found, raise a 404 error.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found in cart")
        return {"message": "Product removed from cart successfully"}
    
    async def get_cart_items(self, user_id):
        return await self.cart_order_service.get_cart_items(user_id)
    
    async def place_order_usecase(self, user_id, user_email):
        return await self.cart_order_service.place_order(user_id, user_email)
    
    async def get_orders(self, user_id: str) -> List[Order]:
        # Retrieve orders from the service layer.
        orders_data = await self.cart_order_service.get_orders(user_id)
        # Convert each order document into the Order Pydantic model.
        orders = []
        for order in orders_data:
            # Ensure ObjectIds are converted to strings.
            order["user_id"] = str(order.get("user_id"))
            for item in order.get("items", []):
                item["product_id"] = str(item.get("product_id"))
            orders.append(Order(**order))
        return orders
    
    async def get_order_detail(self, order_id : str):
        return await self.cart_order_service.get_order_detail(order_id)