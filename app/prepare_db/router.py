import json
from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import Users
from app.database import get_session


router = APIRouter(prefix="/prepare", tags=["Добавление данных в БД"])


@router.post("/prepare_db")
async def prepare_db(session: AsyncSession = Depends(get_session)) -> None:
    def open_json(model: str):
        with open(f"app/tests/{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    users = open_json("users")

    for Model, values in [
        (Users, users),
    ]:
        query = insert(Model).values(values)
        await session.execute(query)

    await session.commit()