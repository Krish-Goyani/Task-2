from fastapi import Depends
from src.app.usecases.products_usecase import ProductsUseCases
from src.app.model.schemas.product_schemas import Product
from fastapi.exceptions import HTTPException
import io
import json
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import StreamingResponse

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
    
    async def update_product_details_controller(self, product_id, update_data, current_user):
        return await self.products_usecases.update_product_usecase(product_id, update_data, current_user)
    
    async def delete_product_controller(self, product_id, current_user):
        return await self.products_usecases.delete_product_usecase(product_id, current_user)
    
    async def download_product_controller(self, product_id: str) -> StreamingResponse:
        
        product = await self.products_usecases.download_product(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        # Convert the product dictionary into a formatted JSON string and then into bytes.
        file_content = json.dumps(product, indent=4, default=str).encode("utf-8")
        file_like = io.BytesIO(file_content)
        
        # Set headers so the file is downloaded with a meaningful filename.
        headers = {"Content-Disposition": f"attachment; filename=product_{product_id}.json"}
        
        return StreamingResponse(file_like, media_type="application/json", headers=headers)

    async def upload_pdf(self, file, current_user):
        # Delegate processing of the PDF to the use case.
        result = await self.products_usecases.process_pdf_upload(file, current_user)
        return result