import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.auth.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_json(model: str):
        with open(f"app/tests/{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_json("users")

    async with async_session_maker() as session:
        for Model, values in [(Users, users)]:
            query = insert(Model).values(values)
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


from httpx import AsyncClient

files = {"file": ("dashboard.xlsx", open("dashboard.xlsx", "rb"), "text/plain")}


@pytest.fixture(scope="session", autouse=True)
async def test_excel_to_db(ac: AsyncClient):
    response = await ac.post("/excel/upload", files=files)

    assert response.status_code == 200
