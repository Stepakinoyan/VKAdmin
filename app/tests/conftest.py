import json
import pytest
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.auth.models import Users
from app.config import settings
from app.database import Base, engine, async_session_maker
from app.main import app as fastapi_app
from app.organizations.models import Organizations
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_json(model: str):
        with open(f"app/tests/{model}.json", encoding="utf-8") as file:
            return json.load(file)

    organizations = open_json("organizations")
    users = open_json("users")

    for organization in organizations:
        organization["date_added"] = datetime.fromisoformat(organization["date_added"])

    async with async_session_maker() as session:
        for Model, values in [
            (Users, users),
            (Organizations, organizations),
        ]:
            for i in range(0, len(values), 1000):  # Разбиваем на батчи по 1000 записей
                batch = values[i : i + 1000]
                query = pg_insert(Model).values(batch)
                await session.execute(query)
        await session.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "test",
            },
        )
        assert ac.cookies["access_token"]
