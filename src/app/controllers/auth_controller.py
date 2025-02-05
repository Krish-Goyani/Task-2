from typing import Any
from src.app.usecases.auth_usecase import AuthUseCases
from fastapi import Depends


class AuthController:
    def __init__(self, auth_usecases = Depends(AuthUseCases)) -> None:
        self.auth_usecases = auth_usecases
    
    async def registration_controller(self, userdata):
        return await self.auth_usecases.register_user_usecase(userdata)
    
    async def login_controller(self, form_data):
        return await self.auth_usecases.user_login_usecase(form_data)
    
    