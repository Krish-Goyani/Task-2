# app/use_cases/products_use_cases.py
from bson import ObjectId
from src.app.services.products_service import ProductsService
from src.app.repositories.user_repository import UserRepository
from fastapi import Depends, status
from src.app.config.database import mongodb_database
from src.app.model.schemas.product_schemas import Product
from fastapi.exceptions import HTTPException
from src.app.model.schemas.product_schemas import ProductUpdate
from datetime import datetime

class ProductsUseCases:
    def __init__(self, products_service = Depends(ProductsService), products_collection = Depends(mongodb_database.get_products_collection), user_repository = Depends(UserRepository)):
        self.products_service = products_service
        self.products_collection = products_collection
        self.user_repository = user_repository
        

    async def preload_products(self) -> str:
        # Fetch products data from DummyJSON asynchronously.
        products_data = await self.products_service.fetch_products()


        # Transform and filter the data to match our schema.
        # Our target Product schema:
        #    title, description, category, price, rating, brand, images, thumbnail, seller_id
        products = []
        for product in products_data.get("products", []):
            new_product = {
                "title": product.get("title"),
                "description": product.get("description"),
                "category": product.get("category"),
                "price": product.get("price"),
                "rating": product.get("rating"),
                "brand": product.get("brand"),
                "images": product.get("images"),
                "thumbnail": product.get("thumbnail"),
                "seller_id": "000000000000000000000000",
                "created_at": product.get("meta", {}).get("createdAt"),
                "updated_at": product.get("meta", {}).get("updatedAt")
            }
            products.append(new_product)

        # Use the repository to insert the products into MongoDB.
        await self.user_repository.insert_products(products, self.products_collection)
        return "data loaded"

    async def add_product_usecase(self, product : Product):
        await self.products_service.insert_product(product)
        return {"message" : "product uploaded"}
    
    async def fetch_all_products_usecase(self):
        return await self.products_service.fetch_all_products()
    
    async def products_details_usecase(self, product_id):
        return await self.products_service.products_details_service(product_id)
    
    async def update_product_usecase(self, product_id: str, product: ProductUpdate, current_user):
        # Retrieve the product by its id
        existing_product = await self.products_service.products_details_service(product_id)
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Check if the product belongs to the current seller
        if str(existing_product.get("seller_id")) != str(current_user["_id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")
        
        # Prepare the update payload; set updated_at timestamp.
        update_data = product.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Call the service to update the product.
        await self.products_service.update_product_service(product_id, update_data)
        return {"message" : "Product updated successfully"}
    
    async def delete_product_usecase(self, product_id, current_user):
        # Retrieve the product by its id
        existing_product = await self.products_service.products_details_service(product_id)
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        # Check if the product belongs to the current seller
        if str(existing_product.get("seller_id")) != str(current_user["_id"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")
        
        return await self.products_service.product_delete_service(product_id, self.products_collection)
    
    async def download_product(self, product_id: str):
        return await self.products_service.products_details_service(product_id)
    
    
    async def process_pdf_upload(self, file, current_user):
        product_data = await self.products_service.extract_product_from_pdf(file)
        
        # Set the seller_id (if not already set) to the current user's id.
        product_data["seller_id"] = current_user["_id"]
        # Insert the product into the database.
        await self.products_service.insert_product(product_data)
        return {"message": "Product details uploaded and processed successfully"}
        