from fastapi import APIRouter, Request, Depends
from src.app.controllers.products_controller import ProductsController
from src.app.utils.limiter import limiter
from src.app.utils.security import authorize
products_router = APIRouter(prefix="/products", tags=["Products"])



@products_router.post("/preload-products/")
@limiter.limit("10/minute")
async def preload_products(request: Request, products_controller = Depends(ProductsController)):
    result = await products_controller.preload_products()
    return {"message": result}
