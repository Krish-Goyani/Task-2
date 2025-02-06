import aiohttp
from src.app.config.settings import settings
from src.app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from src.app.config.database import mongodb_database
from src.app.model.schemas.product_schemas import Product

class ProductsService:
    def __init__(self, products_collection=Depends(mongodb_database.get_products_collection), user_repository=Depends(UserRepository)) -> None:
        self.products_collection = products_collection
        self.user_repository = user_repository

    async def fetch_products(self) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(settings.PRODUCTS_URL) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Failed to fetch products from external service"
                        )
                    # Await and return the JSON response
                    response_data = await response.json()
                    return response_data
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"External service error: {str(e)}")

    async def insert_product(self, product: Product):
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product data is required")
        try:
            return await self.user_repository.insert_product(product, self.products_collection)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to insert product: {str(e)}")

    async def fetch_all_products(self):
        try:
            products = await self.user_repository.fetch_all_products(self.products_collection)
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
            return products
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch products: {str(e)}")

    async def products_details_service(self, product_id):
        if not product_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
        try:
            product = await self.user_repository.fetch_product_details(product_id, self.products_collection)
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            return product
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch product details: {str(e)}")

    async def update_product_service(self, product_id, update_data):
        if not product_id or not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID and update data are required")
        try:
            update_result = await self.user_repository.update_product_details(product_id, update_data, self.products_collection)
            if not update_result.modified_count:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or no changes made")
            return {"message": "Product updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update product: {str(e)}")

    async def product_delete_service(self, product_id, product_collection):
        if not product_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
        try:
            delete_result = await self.user_repository.delete_product(product_id, product_collection)
            if not delete_result.deleted_count:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            return {"message": "Product deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete product: {str(e)}")
