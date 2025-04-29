import calendar
from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.models import Users
from app.dao.dao import BaseDAO
from app.organizations.constants import AMURTIMEZONE
from app.organizations.models import Organizations
from app.statistic.models import Statistic
from fastapi.encoders import jsonable_encoder


class OrganizationsDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def get_levels(self, user: Users, session: AsyncSession):
        get_levels = (
            select(self.model.level)
            .filter(
                self.model.founder.ilike(f"%{user.founder}%") if user.founder else True,
            )
            .distinct()
        )

        results = await session.execute(get_levels)

        return results.mappings().all()

    @classmethod
    async def get_founders_by_level(
        self, level: str, user: Users, session: AsyncSession
    ):
        if user.role != "admin":
            raise HTTPException(
                detail="У вас недостаточно прав", status_code=status.HTTP_403_FORBIDDEN
            )

        get_founders = (
            select(self.model.founder)
            .filter(
                and_(
                    self.model.level == level,
                    self.model.founder.ilike(f"%{user.founder}%")
                    if user.founder
                    else True,
                )
            )
            .distinct(self.model.founder)
        )

        results = await session.execute(get_founders)

        return results.mappings().all()

    @classmethod
    async def get_spheres_by(self, level: str, user: Users, session: AsyncSession):
        sphere1_query = (
            select(self.model.sphere_1.label("sphere"))
            .where(
                and_(
                    self.model.level.ilike(f"%{level}%") if level else True,
                    self.model.founder.ilike(f"%{user.founder}%")
                    if user.founder
                    else True,
                )
            )
            .where(self.model.sphere_1 != None)
        )

        sphere2_query = (
            select(self.model.sphere_2.label("sphere"))
            .where(
                and_(
                    self.model.level.ilike(f"%{level}%") if level else True,
                    self.model.founder.ilike(f"%{user.founder}%")
                    if user.founder
                    else True,
                )
            )
            .where(self.model.sphere_2 != None)
        )

        sphere3_query = (
            select(self.model.sphere_3.label("sphere"))
            .where(
                and_(
                    self.model.level.ilike(f"%{level}%") if level else True,
                    self.model.founder.ilike(f"%{user.founder}%")
                    if user.founder
                    else True,
                )
            )
            .where(self.model.sphere_3 != None)
        )

        combined = union_all(sphere1_query, sphere2_query, sphere3_query).subquery()
        get_spheres = select(combined.c.sphere).distinct()

        results = await session.execute(get_spheres)
        return results.mappings().all()

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
        user: Users,
        session: AsyncSession,
    ):
        if not date_from:
            date_from = datetime.now(AMURTIMEZONE).today().date().replace(day=1)

        if not date_to:
            date_to = date(
                date_from.year,
                date_from.month,
                calendar.monthrange(date_from.year, date_from.month)[1],
            )

        query = select(self.model).filter(
            and_(
                self.model.level.ilike(f"%{level}%"),
                self.model.founder.ilike(f"%{founder}%"),
                self.model.name.ilike(f"%{name}%"),
                or_(
                    self.model.sphere_1.ilike(f"%{sphere}%"),
                    self.model.sphere_2.ilike(f"%{sphere}%"),
                    self.model.sphere_3.ilike(f"%{sphere}%"),
                ),
                self.model.founder.ilike(f"%{user.founder}%") if user.founder else True,
            )
        )

        if zone == "90-100%":
            query = query.options(
                selectinload(
                    self.model.statistic.and_(
                        Statistic.date_added.between(date_from, date_to)
                        & (self.model.average_fulfillment_percentage >= 90)
                    )
                )
            )

        elif zone == "70-89%":
            query = query.options(
                selectinload(
                    self.model.statistic.and_(
                        Statistic.date_added.between(date_from, date_to)
                        & (self.model.average_fulfillment_percentage >= 70)
                        & (self.model.average_fulfillment_percentage < 90)
                    )
                )
            )

        elif zone == "0-69%":
            query = query.options(
                selectinload(
                    self.model.statistic.and_(
                        Statistic.date_added.between(date_from, date_to)
                        & (self.model.average_fulfillment_percentage < 70)
                    )
                )
            )

        results = await session.execute(query)

        return jsonable_encoder(results.scalars().all())
