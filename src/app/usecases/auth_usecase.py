from src.app.services.auth_service import AuthService
from fastapi import Depends


class AuthUseCases:
    def __init__(self, auth_service = Depends(AuthService)) -> None:
        self.auth_service =auth_service
    
    async def register_user_usecase(self, userdata):
        return await self.auth_service.register_user_service(userdata)
    
    
    async def user_login_usecase(self, form_data):
        return await self.auth_service.login_user_service(form_data)


