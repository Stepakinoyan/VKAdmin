from fastapi import APIRouter, Response

from app.auth.schema import UserAuth
from app.auth.users import authenticate_user, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/login")
async def login(user_data: UserAuth, response: Response):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    access_token = create_access_token({"sub": str(user.id)})

    if settings.MODE == "TEST":
        response.set_cookie(key="token", value=access_token, httponly=True)
    else:
        response.set_cookie(key="token", value=access_token)

    return {"access_token": access_token}
