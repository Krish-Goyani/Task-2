from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from src.app.config.settings import settings

class MongoDB:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.mongodb_client = None

    def connect(self):
        try:
            self.mongodb_client = AsyncIOMotorClient(
                self.database_url, maxpoolsize=30, minpoolsize=5
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to connect to MongoDB: {str(e)}"
            )

    def get_mongo_client(self):
        if not self.mongodb_client:
            raise HTTPException(
                status_code=503,
                detail="MongoDB client is not connected."
            )
        return self.mongodb_client

    def get_auth_collection(self):
        try:
            if not self.mongodb_client:
                raise HTTPException(
                    status_code=503,
                    detail="MongoDB client is not connected."
                )
            return self.mongodb_client[settings.AUTH_DB_NAME][settings.AUTH_COLLECTION_NAME]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to access auth collection: {str(e)}"
            )
    def get_products_collection(self):
        try:
            if not self.mongodb_client:
                raise HTTPException(
                    status_code=503,
                    detail="MongoDB client is not connected."
                )
            return self.mongodb_client[settings.PRODUCTS_DB_NAME][settings.PRODUCTS_COLLECTION_NAME]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to access auth collection: {str(e)}"
            )
            
    def get_cart_collection(self):
        try:
            if not self.mongodb_client:
                raise HTTPException(
                    status_code=503,
                    detail="MongoDB client is not connected."
                )
            return self.mongodb_client[settings.CART_DB_NAME][settings.CARTCOLLECTION_NAME]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to access auth collection: {str(e)}"
            )
            
    def get_orders_collection(self):
        try:
            if not self.mongodb_client:
                raise HTTPException(
                    status_code=503,
                    detail="MongoDB client is not connected."
                )
            return self.mongodb_client[settings.ORDER_DB_NAME][settings.ORDER_COLLECTION_NAME]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to access auth collection: {str(e)}"
            )
            
            
    def get_complaint_collection(self):
        try:
            if not self.mongodb_client:
                raise HTTPException(
                    status_code=503,
                    detail="MongoDB client is not connected."
                )
            return self.mongodb_client[settings.COMPLAINT_DB_NAME][settings.COMPLAINT_COLLECTION_NAME]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to access auth collection: {str(e)}"
            )
            
    def disconnect(self):
        try:
            if self.mongodb_client:
                self.mongodb_client.close()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unable to close MongoDB connection: {str(e)}"
            )

# Instantiate the MongoDB class
mongodb_database = MongoDB(settings.MONGO_URI)
