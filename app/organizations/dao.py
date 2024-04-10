from sqlalchemy import select
from app.dao.dao import BaseDAO
from app.organizations.models import Organizations
from app.database import async_session_maker
from app.organizations.schema import Stats


class OrganizationsDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def get_founders_by_level(self, level: str) -> list:
        async with async_session_maker() as session:
            get_founders = (
                select(self.model.founder)
                .filter_by(level=level)
                .distinct(self.model.founder)
            )

            results = await session.execute(get_founders)

            return results.mappings().all()

    @classmethod
    async def get_sphere_by_founder(self, founder: str) -> list:
        async with async_session_maker() as session:
            get_founders = (
                select(self.model.sphere)
                .filter_by(founder=founder)
                .distinct(self.model.sphere)
            )

            results = await session.execute(get_founders)

            return results.mappings().all()

    @classmethod
    async def filter_channels(
        self, level: str, founder: str, sphere: str, sort: bool
    ) -> list:
        async with async_session_maker() as session:
            if sort:
                get_channels = (
                    select(self.model.__table__.columns)
                    .filter_by(level=level, founder=founder, sphere=sphere)
                    .order_by(self.model.total.desc())
                )
            else:
                get_channels = select(self.model.__table__.columns).filter_by(
                    level=level, founder=founder, sphere=sphere
                )

            results = await session.execute(get_channels)
            mapping_result = results.mappings().all()

            stats = [
                Stats(count=len(mapping_result), items=mapping_result).model_dump()
            ]

            return stats
