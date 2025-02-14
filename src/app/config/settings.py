from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI : str
    AUTH_DB_NAME : str
    AUTH_COLLECTION_NAME : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    ALGORITHM : str
    JWT_SECRET_KEY : str
    TOKEN_URL : str
    PRODUCTS_URL : str
    PRODUCTS_DB_NAME : str
    PRODUCTS_COLLECTION_NAME : str
    CART_DB_NAME: str
    CARTCOLLECTION_NAME : str
    ORDER_DB_NAME : str
    ORDER_COLLECTION_NAME  : str
    SERVICE_ACCOUNT_JSON : str
    BUCKET_NAME : str
    GEMINI_API_KEY : str
    DELEGATE_EMAIL : str
    COMPLAINT_DB_NAME : str
    COMPLAINT_COLLECTION_NAME  : str
    GROQ_API_KEY : str
    GROQ_MODEL_NAME : str
        

    class Config:
        env_file = "src/.env"


settings = Settings()