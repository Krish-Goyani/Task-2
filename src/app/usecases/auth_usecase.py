from src.app.services.auth_service import auth_service



class AuthUseCases:
    def __init__(self) -> None:
        pass
    
    async def register_user_usecase(self, userdata,auth_collection):
        return await auth_service.register_user_service(userdata,auth_collection)
    
    
    async def user_login_usecase(self, form_data, auth_collection):
        return await auth_service.login_user_service(form_data, auth_collection)


auth_usecases = AuthUseCases()