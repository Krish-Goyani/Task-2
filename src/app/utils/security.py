from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from src.app.config.settings import settings
from functools import wraps
from fastapi import HTTPException
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from src.app.config.database import mongodb_database
from src.app.model.schemas.user_schemas import User, TokenPayload
from fastapi import HTTPException, status
from jose import jwt
from pydantic import ValidationError
from datetime import datetime

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_URL,
    scheme_name="JWT"
)

password_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = expires_delta + datetime.utcnow()
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    enocoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return enocoded_jwt


async def get_current_user(token: str = Depends(reuseable_oauth), auth_collection = Depends(mongodb_database.get_auth_collection)):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials provided",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await auth_collection.find_one({"email": token_data.sub})
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if user["role"] not in role:
                raise HTTPException(status_code=403, detail="User is not authorized to access")
            return await func(*args, **kwargs)
        return wrapper
    return decorator