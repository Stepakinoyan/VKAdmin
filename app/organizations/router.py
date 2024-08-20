import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Users
from app.auth.users import get_current_user
from app.database import get_session
from app.organizations.dao import OrganizationsDAO
from app.organizations.params import (
    FilterChannelsParams,
    FilterFounderParams,
    FilterSpheresParams,
)
from app.organizations.schemas import FounderDTO, SphereDTO, OrganizationsDTO

router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_founders")
async def get_founders(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterfounderparams: FilterFounderParams = Depends(),
    session: AsyncSession = Depends(get_session),
)  -> list[FounderDTO]:
    return await OrganizationsDAO.get_founders_by_level(
        level=filterfounderparams.level, session=session
    )


@router.get("/get_spheres_by")
async def get_spheres(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterspheresparams: FilterSpheresParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[SphereDTO]:
    return await OrganizationsDAO.get_spheres_by(
        founder=filterspheresparams.founder,
        level=filterspheresparams.level,
        session=session,
    )


@router.get("/get_stats")
@cache(expire=60)
async def get_stats(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterchannelsparams: FilterChannelsParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[OrganizationsDTO]:
    try:
        return await OrganizationsDAO.filter_channels(
            level=filterchannelsparams.level,
            founder=filterchannelsparams.founder,
            name=filterchannelsparams.name,
            sphere=filterchannelsparams.sphere,
            zone=filterchannelsparams.zone,
            date_from=filterchannelsparams.date_from,
            date_to=filterchannelsparams.date_to,
            session=session,
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
