from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.app.utils.limiter import limiter
from fastapi.requests import Request
from src.app.model.schemas.user_schemas import UserIn
from src.app.config.database import mongodb_database
from src.app.model.schemas.user_schemas import TokenSchema
from src.app.controllers.auth_controller import AuthController
from src.app.utils.security import authorize

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
@limiter.limit("10/minute")
async def register_user(request: Request, userdata : UserIn, auth_controller = Depends(AuthController)):
    try:
        response = await auth_controller.registration_controller(userdata)
        return response
    except Exception:
        raise

@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
@limiter.limit("10/minute")
async def user_login(request : Request, form_data: OAuth2PasswordRequestForm = Depends(), auth_controller = Depends(AuthController)):
    try:
        response = await auth_controller.login_controller(form_data)
        return response
    except Exception:
        raise