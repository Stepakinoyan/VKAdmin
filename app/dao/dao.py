from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session


class BaseDAO:
    model = None

    @classmethod
    async def find_user(cls, session: AsyncSession = get_session(), **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)

        return result.mappings().one_or_none()
