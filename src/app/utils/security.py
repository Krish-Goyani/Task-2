from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from src.app.config.settings import settings
from functools import wraps
from fastapi import HTTPException

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


def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if user.role.value not in role:
                raise HTTPException(status_code=403, detail="User is not authorized to access")
            return await func(*args, **kwargs)
        return wrapper
    return decorator