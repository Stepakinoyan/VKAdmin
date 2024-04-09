from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


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
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Токен отсутствует"
