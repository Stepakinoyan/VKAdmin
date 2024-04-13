from fastapi import APIRouter
from app.auth.schema import UserAuth
from app.auth.users import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/login")
async def login_user(user_data: UserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
