from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.auth.models import Users
from app.auth.schema import Role, UserAuth
from app.auth.users import authenticate_user, create_access_token, get_current_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/login")
async def login(user_data: UserAuth, response: Response):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    access_token = create_access_token({"sub": str(user.id)}, )


    response.set_cookie(key="token", value=access_token, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES, httponly=True, secure=True)

    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")


@router.get("/me", response_model=Role)
async def me(current_user: Annotated[Users, Depends(get_current_user)]):
    return current_user
