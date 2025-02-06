from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.app.utils.limiter import limiter
from fastapi.requests import Request
from src.app.model.schemas.user_schemas import UserIn, UserOut
from src.app.config.database import mongodb_database
from src.app.model.schemas.user_schemas import TokenSchema
from src.app.controllers.auth_controller import AuthController
from src.app.utils.security import authorize
from src.app.utils.security import get_current_user
from typing import List

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/auth/register")
@limiter.limit("10/minute")
async def register_user(request: Request, userdata : UserIn, auth_controller = Depends(AuthController)):
    try:
        response = await auth_controller.registration_controller(userdata)
        return response
    except Exception:
        raise

@auth_router.post('/auth/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
@limiter.limit("10/minute")
async def user_login(request : Request, form_data: OAuth2PasswordRequestForm = Depends(), auth_controller = Depends(AuthController)):
    try:
        response = await auth_controller.login_controller(form_data)
        return response
    except Exception:
        raise
    
    
@auth_router.get("/users/me")
async def get_currently_authenticated_user(current_user = Depends(get_current_user), auth_controller = Depends(AuthController)):
    return await auth_controller.current_user_controller(current_user)

@auth_router.get("/usesrs")
@authorize(role=["admin"])
async def get_all_users(current_user = Depends(get_current_user), auth_controller = Depends(AuthController)) -> List[UserOut]:
    return await auth_controller.get_all_users_controller()

@auth_router.put("/users/{user_id}/role")
@authorize(role = ["admin"])
async def update_user_role(user_id : str, role, current_user = Depends(get_current_user), auth_controller = Depends(AuthController)):
    return await auth_controller.update_user_role_controller(user_id, role)
