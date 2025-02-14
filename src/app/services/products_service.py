import aiohttp
from src.app.config.settings import settings
from src.app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from src.app.config.database import mongodb_database
from src.app.model.schemas.product_schemas import Product
from datetime import datetime
from PyPDF2 import PdfReader
from src.app.model.schemas.product_schemas import ProductLLM
from langchain_google_genai import GoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from src.app.config.settings import settings
import pymupdf4llm
import os
import tempfile
from src.app.utils.groq_client import ProductsDetailExtractor
class ProductsService:
    def __init__(self, products_collection=Depends(mongodb_database.get_products_collection), user_repository=Depends(UserRepository), groq_client = Depends(ProductsDetailExtractor)) -> None:
        self.products_collection = products_collection
        self.user_repository = user_repository
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",  
            google_api_key=settings.GEMINI_API_KEY
        )
        self.groq_client = groq_client

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
        
        return await self.user_repository.update_product_details(product_id, update_data, self.products_collection)

    async def product_delete_service(self, product_id, product_collection):
        if not product_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
        return await self.user_repository.delete_product(product_id, product_collection)
       
    async def extract_product_from_pdf(self, file) -> dict:
        """
        Process the uploaded PDF:
         1. Extract text using PyPDF2.
         2. Pass the text to a Gemini Flash model (via LangChain) using a structured output parser
            to extract product details in JSON format.
        """
        try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(await file.read())
                    tmp_path = tmp.name
                
                # Convert the PDF to Markdown using pymupdf4llm
                text = pymupdf4llm.to_markdown(tmp_path)
                
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
        try:
            # Invoke the model with the formatted prompt.
            result = self.groq_client.extract_details(ProductLLM, text)
            # The result is an instance of ProductLLM.
            product_data = result.model_dump()
        except Exception as e:
            raise Exception(f"Failed to extract product details using GROQ  LLM: {str(e)}")
        
        # --- Step 4: Add timestamps ---
        now = datetime.utcnow().isoformat()
        product_data["created_at"] = now
        product_data["updated_at"] = now
        
        return product_data

        
