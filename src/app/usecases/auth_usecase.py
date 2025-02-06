from src.app.services.auth_service import AuthService
from fastapi import Depends
from src.app.model.schemas.user_schemas import UserOut


class AuthUseCases:
    def __init__(self, auth_service = Depends(AuthService)) -> None:
        self.auth_service =auth_service
    
    async def register_user_usecase(self, userdata):
        return await self.auth_service.register_user_service(userdata)
    
    
    async def user_login_usecase(self, form_data):
        return await self.auth_service.login_user_service(form_data)
    
    async def get_current_user(self, current_user):
        current_user["_id"] = str(current_user["_id"])
        return UserOut(**current_user)
    
    async def get_all_users(self):
        return await self.auth_service.get_all_users()


