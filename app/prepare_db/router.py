from datetime import datetime
import json
from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import Users
from app.database import get_session
from app.organizations.models import Organizations
from app.vk.models import Account


router = APIRouter(prefix="/prepare", tags=["Добавление данных в БД"])


@router.post("/prepare_db")
async def prepare_db(session: AsyncSession = Depends(get_session)):
    def open_json(model: str):
        with open(f"app/tests/{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    users = open_json("users")
    organizations = open_json("organizations")
    accounts = open_json("accounts")
    # statistic = open_json("statistic")
    

    for account in accounts:
        account["date_added"] = datetime.fromisoformat(account["date_added"])
        account["post_date"] = datetime.fromisoformat(account["post_date"])

    # for stat in statistic:
    #     stat["date_added"] = datetime.fromisoformat(stat["date_added"])

    for Model, values in [
        (Users, users),
        (Organizations, organizations),
        (Account, accounts),
        # (Statistic, statistic),
    ]:
        query = insert(Model).values(values)
        await session.execute(query)

    await session.commit()