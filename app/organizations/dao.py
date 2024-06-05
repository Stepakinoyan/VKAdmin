import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.dao.dao import BaseDAO
from app.database import get_session
from app.organizations.funcs import get_unique_spheres, get_new_stats
from app.organizations.models import Organizations
from app.organizations.schemas import (
    OrganizationResponse,
    OrganizationsBase,
    Sphere,
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
    async def get_sphere_by_level(
        self, level: str, session: AsyncSession = get_session()
    ) -> list[Sphere]:
        get_founders = (
            select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            .filter_by(level=level)
            .distinct(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
        )

        results = await session.execute(get_founders)
        results = results.scalars().all()
        return get_unique_spheres(results)

    @classmethod
    async def get_sphere_by_founder(
        self, founder: str, session: AsyncSession = get_session()
    ) -> list[Sphere]:
        get_founders = (
            select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            .filter_by(founder=founder)
            .distinct(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
        )

        results = await session.execute(get_founders)
        results = results.scalars().all()

        return get_unique_spheres(results)

    @classmethod
    async def filter_channels(
        cls,
        level: str,
        founder: str,
        sphere: str,
        session: AsyncSession = None,
    ) -> list[StatsData]:
        try:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.statistic))
                .filter(
                    and_(
                        cls.model.level.ilike(f"%{level}%"),
                        cls.model.founder.ilike(f"%{founder}%"),
                        or_(
                            cls.model.sphere_1.ilike(f"%{sphere}%"),
                            cls.model.sphere_2.ilike(f"%{sphere}%"),
                            cls.model.sphere_3.ilike(f"%{sphere}%"),
                        ),
                    )
                )
            )


            logging.debug(f"Executing query: {query}")

            results = await session.execute(query)
            res = results.scalars().all()
            logging.debug(f"Query results: {res}")

            # Преобразуем результаты в объекты Pydantic
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

        return [stats.model_dump()]
