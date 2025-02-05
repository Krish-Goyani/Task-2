
from src.app.config.database import mongodb_database
from src.app.model.domain.user import User
from fastapi import Depends

class UserRepository:
    def __init__(self, ) -> None:
        pass
    
    async def find_user_by_email(self, email: str, auth_collection):
        return await auth_collection.find_one({"email": email})
        
        
    async def insert_user(self, user_data, auth_collection):
        user = User(name= user_data["name"],
                    email= user_data["email"],
                    password_hash= user_data["password_hash"],
                    role= user_data["role"])
        
        return await auth_collection.insert_one(user.to_dict())
    
    async def insert_products(self, products, products_collection):
        return await products_collection.insert_many(products)
        
        
        