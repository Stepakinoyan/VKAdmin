import logging

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.organizations.dao import OrganizationsDAO
from app.organizations.params import (
    FilterChannelsParams,
    FilterFounderParams,
    FilterSpheresParams,
)
from app.organizations.schemas import OrganizationsDTO

router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_all_stats", response_model=list[OrganizationsDTO])
@cache(expire=60)
async def get_all_stats(session: AsyncSession = Depends(get_session)):
    return await OrganizationsDAO.get_all_stats(session)


@router.get("/get_founders")
@cache(expire=60)
async def get_founders(
    filterfounderparams: FilterFounderParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.get_founders_by_level(
        level=filterfounderparams.level, session=session
    )


@router.get("/get_spheres_by")
async def get_spheres(
    filterspheresparams: FilterSpheresParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.get_spheres_by(
        founder=filterspheresparams.founder,
        level=filterspheresparams.level,
        session=session,
    )


@router.get("/get_stats")
@cache(expire=60)
async def get_stats(
    filterchannelsparams: FilterChannelsParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
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
