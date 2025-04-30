from datetime import date
from typing import Optional
from fastapi.encoders import jsonable_encoder
from app.auth.models import Users
from app.organizations.dao import OrganizationsDAO
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationsService:
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
        organizations = await OrganizationsDAO.filter_channels(
            level=level,
            founder=founder,
            name=name,
            sphere=sphere,
            zone=zone,
            user=user,
            date_from=date_from,
            date_to=date_to,
            session=session,
        )
        return jsonable_encoder(organizations)


service = OrganizationsService()
