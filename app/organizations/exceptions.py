from app.exceptions import BaseHTTPException
from fastapi import status


class InvalidDatesException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid dates"
