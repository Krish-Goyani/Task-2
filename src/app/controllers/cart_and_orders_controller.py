
from src.app.usecases.cart_and_orders_usecases import CartOrdersUsecase
from fastapi import Depends

class CartOrderController:
    def __init__(self, cart_order_usecase = Depends(CartOrdersUsecase)) -> None:
        self.cart_order_usecase =cart_order_usecase
    
    
    async def add_item_in_cart_controller(self, cart_item):
        if await self.cart_order_usecase.add_item_in_cart_usecase(cart_item):
            return {"message" : "item added in the cart"}
        
    async def remove_from_cart_controller(self, current_user, product_id: str):
        result = await self.cart_order_usecase.remove_from_cart(current_user, product_id)
        return result