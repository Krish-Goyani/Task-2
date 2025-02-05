from typing import Any
from src.app.usecases.auth_usecase import auth_usecases


class AuthController:
    def __init__(self) -> None:
        pass
    
    async def registration_controller(self, userdata,auth_collection):
        return await auth_usecases.register_user_usecase(userdata, auth_collection)
    
    async def login_controller(self, form_data, auth_collection):
        return await auth_usecases.user_login_usecase(form_data, auth_collection)
    
    
auth_controller = AuthController()