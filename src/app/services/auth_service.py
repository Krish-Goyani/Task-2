
from src.app.model.schemas.user_schemas import UserIn
from src.app.repositories.user_repository import user_repository
from src.app.utils.security import get_hashed_password, verify_password, create_access_token

class AuthService:
    def __init__(self) -> None:
        pass
    
    async def register_user_service(self, userdata : UserIn, auth_collection):
        user = await user_repository.find_user_by_email(userdata.email, auth_collection)
        if user:
            pass
        
        data = userdata.model_dump()
        data["password_hash"] = get_hashed_password(data["password"])
        
        await user_repository.insert_user(data, auth_collection)
        
        return data
    
    async def login_user_service(self, form_data, auth_collection):
        user = await user_repository.find_user_by_email(form_data.username, auth_collection)
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

auth_service = AuthService()