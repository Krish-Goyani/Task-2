import aiohttp
from src.app.config.settings import settings
from src.app.repositories.user_repository import UserRepository
from fastapi import Depends
from src.app.config.database import mongodb_database
from src.app.model.schemas.product_schemas import Product


class ProductsService:
    def __init__(self, products_collection=Depends(mongodb_database.get_products_collection), user_repository=Depends(UserRepository)) -> None:
        self.products_collection = products_collection
        self.user_repository = user_repository

    async def fetch_products(self) -> dict:

        async with aiohttp.ClientSession() as session:
            async with session.get(settings.PRODUCTS_URL) as response:
                # Await and return the JSON response
                response_data = await response.json()
                return response_data

    async def insert_product(self, product: Product):
        return await self.user_repository.insert_product(product, self.products_collection)

    async def fetch_all_products(self):
        return await self.user_repository.fetch_all_products(self.products_collection)
    
    async def products_details_service(self, product_id):
        return await self.user_repository.fetch_product_details(product_id, self.products_collection)
    
    async def update_product_service(self, product_id, update_data):
        return await self.user_repository.update_product_details(product_id, update_data, self.products_collection)
    
    async def product_delete_service(self, product_id, product_collection):
        return await self.user_repository.delete_product(product_id, product_collection)
    
