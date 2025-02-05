from fastapi import Depends
from src.app.usecases.products_usecase import ProductsUseCases
from src.app.model.schemas.product_schemas import Product


class ProductsController:
    def __init__(self, products_usecases = Depends(ProductsUseCases)):
        self.products_usecases = products_usecases

    async def preload_products(self) -> str:
        result = await self.products_usecases.preload_products()
        return result
    
    async def add_product(self, product : Product):
        return await self.products_usecases.add_product_usecase(product)
    
    async def fetch_all_products_controller(self):
        return await self.products_usecases.fetch_all_products_usecase()
    
    async def products_details_controller(self, product_id):
        return await self.products_usecases.products_details_usecase(product_id)