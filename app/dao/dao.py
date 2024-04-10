import json
from sqlalchemy import insert, select
from app.auth.models import Users
from app.database import Base, async_session_maker, engine
from app.organizations.models import Organizations


class BaseDAO:
    model = None

    @classmethod
    async def find_user(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)

            return result.mappings().one_or_none()

    @classmethod
    async def prepare_database(cls):

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        def open_json(model: str):
            with open(f"app/{model}.json", encoding="utf-8") as file:
                return json.load(file)

        users = open_json("users")
        organizations = open_json("stats")

        async with async_session_maker() as session:
            for Model, values in [(Users, users), (Organizations, organizations)]:
                query = insert(Model).values(values)
                await session.execute(query)

            await session.commit()