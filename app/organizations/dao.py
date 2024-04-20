from sqlalchemy import and_, or_, select
from app.dao.dao import BaseDAO
from app.organizations.models import Organizations
from app.database import async_session_maker
from app.organizations.schema import Sphere, Stats


class OrganizationsDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def get_all_stats(self):
        async with async_session_maker() as session:
            get_stats = select(self.model.__table__.columns)

            results = await session.execute(get_stats)

            return results.mappings().all()

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
    async def get_sphere_by_level(self, level: str) -> list:
        spheres = []
        async with async_session_maker() as session:
            get_founders = (
                select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
                .filter_by(level=level)
                .distinct(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            )

            results = await session.execute(get_founders)

            for item in list(
                set(filter(lambda item: item is not None, results.scalars().all()))
            ):
                sphere = Sphere(sphere=item).model_dump()
                spheres.append(sphere)

        return spheres

    @classmethod
    async def get_sphere_by_founder(self, founder: str) -> list:
        spheres = []
        async with async_session_maker() as session:
            get_founders = (
                select(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
                .filter_by(founder=founder)
                .distinct(self.model.sphere_1, self.model.sphere_2, self.model.sphere_3)
            )

            results = await session.execute(get_founders)

            for item in list(
                set(filter(lambda item: item is not None, results.scalars().all()))
            ):
                sphere = Sphere(sphere=item).model_dump()
                spheres.append(sphere)

        return spheres

    @classmethod
    async def filter_channels(
        self, level: str, founder: str, sphere: str, sort: bool
    ) -> list:
        async with async_session_maker() as session:
            if sort:
                get_channels = (
                    select(
                        self.model.name,
                        self.model.channel_id,
                        self.model.url,
                        self.model.address,
                        self.model.connected,
                        self.model.state_mark,
                        self.model.decoration,
                        self.model.widgets,
                        self.model.activity,
                        self.model.followers,
                        self.model.weekly_audience,
                        self.model.average_publication_coverage,
                    )
                    .filter(
                        and_(
                            self.model.level.like(f"%{level}%"),
                            self.model.founder.like(f"%{founder}%"),
                            or_(
                                self.model.sphere_1.like(f"%{sphere}%"),
                                self.model.sphere_2.like(f"%{sphere}%"),
                                self.model.sphere_3.like(f"%{sphere}%"),
                            ),
                        )
                    )
                    .order_by(self.model.followers.desc())
                )

            else:
                get_channels = select(
                    self.model.name,
                    self.model.channel_id,
                    self.model.url,
                    self.model.address,
                    self.model.connected,
                    self.model.state_mark,
                    self.model.decoration,
                    self.model.widgets,
                    self.model.activity,
                    self.model.followers,
                    self.model.weekly_audience,
                    self.model.average_publication_coverage,
                ).filter(
                    and_(
                        self.model.level.like(f"%{level}%"),
                        self.model.founder.like(f"%{founder}%"),
                        or_(
                            self.model.sphere_1.like(f"%{sphere}%"),
                            self.model.sphere_2.like(f"%{sphere}%"),
                            self.model.sphere_3.like(f"%{sphere}%"),
                        ),
                    )
                )

            results = await session.execute(get_channels)
            mapping_result = results.mappings().all()

            stats = [
                Stats(count=len(mapping_result), items=mapping_result).model_dump()
            ]

            return stats
