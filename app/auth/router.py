import json
from fastapi import APIRouter, Depends
from app.auth.schema import UserAuth
from app.auth.users import authenticate_user, create_access_token
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Авторизация"])


def open_json(model: str):
    with open(f"app/tests/{model}.json", encoding="utf-8") as file:
        return json.load(file)


@router.post("/login")
async def login_user(user_data: UserAuth, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(
        session=session, email=user_data.email, password=user_data.password
    )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
