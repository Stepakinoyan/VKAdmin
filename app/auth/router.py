from fastapi import APIRouter, Response
from app.auth.schema import UserAuth
from app.auth.users import authenticate_user, create_access_token

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_user(response: Response, user_data: UserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}