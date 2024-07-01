import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.organizations.dao import OrganizationsDAO
from app.organizations.params import (
    FilterChannelsParams,
    FilterFounderParams,
    FilterSpheresParams,
)
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_all_stats")
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
@cache(expire=60)
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
async def get_stats(
    filterchannelsparams: FilterChannelsParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await OrganizationsDAO.filter_channels(
            level=filterchannelsparams.level,
            founder=filterchannelsparams.founder,
            sphere=filterchannelsparams.sphere,
            zone=filterchannelsparams.zone,
            session=session,
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
