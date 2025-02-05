
from src.app.model.schemas.user_schemas import UserIn
from src.app.repositories.user_repository import UserRepository
from src.app.utils.security import get_hashed_password, verify_password, create_access_token
from fastapi import Depends
from src.app.config.database import mongodb_database


class AuthService:
    def __init__(self, auth_collection = Depends(mongodb_database.get_auth_collection), user_repository = Depends(UserRepository)) -> None:
        self.auth_collection = auth_collection
        self.user_repository = user_repository
    
    async def register_user_service(self, userdata : UserIn):
        user = await self.user_repository.find_user_by_email(userdata.email, self.auth_collection)
        if user:
            pass
        
        data = userdata.model_dump()
        data["password_hash"] = get_hashed_password(data["password"])
        
        insertion_result = await self.user_repository.insert_user(data, self.auth_collection)
        
        return str(insertion_result.inserted_id)
    
    async def login_user_service(self, form_data):
        user = await self.user_repository.find_user_by_email(form_data.username, self.auth_collection)
        if user is None:
            pass
        
        # Verify the password
        hashed_pass = user["password_hash"]
        if not verify_password(form_data.password, hashed_pass):
            pass
        
        # Create access and refresh tokens
        access_token = create_access_token(user['email'])

        return {
            "access_token": access_token,
        }
