from fastapi import APIRouter, Depends
from src.app.utils.security import authorize
from src.app.controllers.cart_and_orders_controller import CartOrderController
from src.app.model.schemas.order_and_carts_schemas import CartItem
from src.app.utils.security import get_current_user

cart_and_orders_router = APIRouter( tags=["cart"])


@cart_and_orders_router.post("/cart/add")
@authorize(role= ["buyer", "admin"])
async def add_item_in_cart(cart_item : CartItem, current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):
    return await cart_orders_controller.add_item_in_cart_controller(cart_item)

@cart_and_orders_router.delete("/cart/remove/{product_id}")
@authorize(role= ["buyer", "admin"])
async def remove_item_from_cart(product_id : str, current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):
    return await cart_orders_controller.remove_from_cart_controller(current_user, product_id)

@cart_and_orders_router.get("/cart/")
@authorize(role=["buyer", "admin"])
async def get_whole_cart_content(current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):
    return await cart_orders_controller.get_cart_items_controller(current_user)

@cart_and_orders_router.post("/orders")
@authorize(role=["buyer", "admin"])
async def place_order(current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):

    return await cart_orders_controller.place_order_controller(current_user)

@cart_and_orders_router.get("/orders")
@authorize(role=["buyer", "admin"])
async def get_order(current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):
    return await cart_orders_controller.get_orders_controller(current_user)

@cart_and_orders_router.get("/orders/{order_id}")
@authorize(role = ["buyer", "admin"])
async def get_order_detail(order_id : str, current_user = Depends(get_current_user), cart_orders_controller = Depends(CartOrderController)):
    return await cart_orders_controller.get_order_detail_controller(order_id)

