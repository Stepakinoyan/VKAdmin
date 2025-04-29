from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.auth.dao import UserDAO
from app.config import settings
from app.exceptions import (
    IncorrectEmailOrPasswordException,
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.organizations.constants import AMURTIMEZONE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(AMURTIMEZONE) + expires_delta
    else:
        expire = datetime.now(AMURTIMEZONE) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_user(email=email)
    if not (user and verify_password(password, user.password)):
        raise IncorrectEmailOrPasswordException
    return user


def get_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_user(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
