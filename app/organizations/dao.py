import logging
from datetime import date, datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.dao import BaseDAO
from app.organizations.funcs import amurtime, get_last_monday, get_unique_spheres
from app.organizations.models import Organizations
from app.organizations.schemas import OrganizationsDTO
from app.statistic.funcs import get_stats_by_dates
from app.statistic.schemas import StatisticDTO


class OrganizationsDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def get_founders_by_level(self, level: str, session: AsyncSession):
        get_founders = (
            select(self.model.founder)
            .filter_by(level=level)
            .distinct(self.model.founder)
        )

        results = await session.execute(get_founders)

        return results.mappings().all()

    @classmethod
    async def get_spheres_by(self, level: str, founder: str, session: AsyncSession):
        get_spheres = (
            select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            .where(
                and_(
                    self.model.level.ilike(f"%{level}%") if level else True,
                    self.model.founder.ilike(f"%{founder}%") if founder else True,
                )
            )
            .distinct()
        )

        results = await session.execute(get_spheres)
        results = results.scalars().all()

        return get_unique_spheres(results)

    @classmethod
    async def filter_channels(
        self,
        level: str,
        founder: str,
        name: str,
        sphere: str,
        zone: str,
        date_from: Optional[date],
        date_to: Optional[date],
        session: AsyncSession,
    ):
        if not date_from:
            date_from = get_last_monday()

        if not date_to:
            date_to = datetime.now(amurtime).date()

        try:
            date_from_dt = datetime.combine(date_from, datetime.min.time())
            date_to_dt = datetime.combine(date_to, datetime.min.time())
            query = (
                select(self.model)
                .options(selectinload(self.model.statistic))
                .filter(
                    and_(
                        self.model.level.ilike(f"%{level}%"),
                        self.model.founder.ilike(f"%{founder}%"),
                        self.model.name.ilike(f"%{name}%"),
                        or_(
                            self.model.sphere_1.ilike(f"%{sphere}%"),
                            self.model.sphere_2.ilike(f"%{sphere}%"),
                            self.model.sphere_3.ilike(f"%{sphere}%"),
                        ),
                    )
                )
            )

            if zone == "90-100%":
                query = query.where(self.model.average_fulfillment_percentage >= 90)
            elif zone == "70-89%":
                query = query.where(
                    (Organizations.average_fulfillment_percentage >= 70)
                    & (Organizations.average_fulfillment_percentage < 90)
                )
            elif zone == "0-69%":
                query = query.where(self.model.average_fulfillment_percentage <= 69)

            results = await session.execute(query)
            organizations = results.scalars().all()

            stats_items = []

            for organization in organizations:
                organization_data = jsonable_encoder(organization)
                organization_data["statistic"] = get_stats_by_dates(
                    stats=[
                        StatisticDTO.model_validate(stat, from_attributes=True)
                        for stat in organization.statistic
                    ],
                    date_from=date_from_dt,
                    date_to=date_to_dt,
                )
                stats_items.append(OrganizationsDTO(**organization_data))

        except Exception as e:
            logging.error("Error executing filter_channels query", exc_info=True)
            raise e

        return stats_items
