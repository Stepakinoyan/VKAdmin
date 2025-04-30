from app.exceptions import BaseHTTPException
from fastapi import status


class IncorrectEmailOrPasswordException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный логин или пароль"


class TokenExpiredException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class UserIsNotPresentException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователя не существует"


class IncorrectTokenFormatException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный токен"


class TokenAbsentException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не авторизованы"
