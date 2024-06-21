import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.dao import BaseDAO
from app.database import get_session
from app.organizations.funcs import get_unique_spheres, get_new_stats
from app.organizations.models import Organizations
from app.organizations.schemas import (
    OrganizationResponse,
    OrganizationsBase,
    StatisticBase,
    Stats,
    StatsData,
    Founder,
)


class OrganizationsDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def get_all_stats(
        self, session: AsyncSession = get_session()
    ) -> list[StatsData]:
        get_stats = select(self.model)

        results = await session.execute(get_stats)

        res = results.scalars().all()
        result = [
            OrganizationsBase.model_validate(row, from_attributes=True) for row in res
        ]

        return result

    @classmethod
    async def get_founders_by_level(
        self, level: str, session: AsyncSession = get_session()
    ) -> list[Founder]:
        get_founders = (
            select(self.model.founder)
            .filter_by(level=level)
            .distinct(self.model.founder)
        )

        results = await session.execute(get_founders)

        return results.mappings().all()

    @classmethod
    async def get_spheres_by(
        self, level: str, founder: str, session: AsyncSession = get_session()
    ):
        get_spheres = (
            select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            .where(
                and_(
                    self.model.level.ilike(f"%{level}%"),
                    self.model.founder.ilike(f"%{founder}%"),
                )
            )
            .distinct(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
        )

        results = await session.execute(get_spheres)
        results = results.scalars().all()
        return get_unique_spheres(results)

    @classmethod
    async def filter_channels(
        self,
        level: str,
        founder: str,
        sphere: str,
        zone: str,
        session: AsyncSession,
    ) -> list:
        try:
            # Основной запрос с подзапросом для фильтрации по последней статистике
            query = (
                select(self.model)
                .options(selectinload(self.model.statistic))
                .filter(
                    and_(
                        self.model.level.ilike(f"%{level}%"),
                        self.model.founder.ilike(f"%{founder}%"),
                        or_(
                            self.model.sphere_1.ilike(f"%{sphere}%"),
                            self.model.sphere_2.ilike(f"%{sphere}%"),
                            self.model.sphere_3.ilike(f"%{sphere}%"),
                        ),
                    )
                )
            )

            # Условие на основе зоны выполнения
            if zone == "90-100%":
                query = query.where(self.model.average_fulfillment_percentage >= 90)
            elif zone == "70-89%":
                query = query.where(
                    (self.model.average_fulfillment_percentage >= 70)
                    & (self.model.average_fulfillment_percentage < 90)
                )
            elif zone == "0-69%":
                query = query.where(self.model.average_fulfillment_percentage <= 69)

            # Выполнение запроса
            results = await session.execute(query)
            res = results.scalars().all()

            # Преобразование результатов в Pydantic объекты
            stats_items = []
            for item in res:
                organization_data = jsonable_encoder(item)
                organization_data["statistic"] = [
                    StatisticBase(**stat)
                    for stat in organization_data.get("statistic", [])
                ]
                stats_items.append(OrganizationResponse(**organization_data))

            stats = Stats(items=stats_items)

            for item in stats.items:
                if item.statistic:
                    item.statistic = get_new_stats(item.statistic)

        except Exception as e:
            logging.error("Error executing filter_channels query", exc_info=True)
            raise e

        return [stats]
