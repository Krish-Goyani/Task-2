from fastapi import Depends
from src.app.usecases.products_usecase import ProductsUseCases


class ProductsController:
    def __init__(self, products_usecases = Depends(ProductsUseCases)):
        self.products_usecases = products_usecases

    async def preload_products(self) -> str:
        result = await self.products_usecases.preload_products()
        return result