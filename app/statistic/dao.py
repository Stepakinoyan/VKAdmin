from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import BaseDAO
from app.statistic.models import Statistic


class StatisticDAO(BaseDAO):
    model = Statistic

    @classmethod
    async def get_dates(self, session: AsyncSession):
        dates = select(self.model.__table__.columns.date_added).distinct(
            self.model.date_added
        )

        result = await session.execute(dates)

        return result.mappings().all()
