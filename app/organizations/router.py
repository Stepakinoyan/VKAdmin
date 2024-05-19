from fastapi import APIRouter, Depends
from app.database import get_session
from app.organizations.dao import OrganizationsDAO
from app.organizations.params import FilterChannelsParams, FilterFounderParams
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_all_stats")
async def get_all_stats(session: AsyncSession = Depends(get_session)):
    return await OrganizationsDAO.get_all_stats(session)


@router.get("/get_founders")
async def filter_channels(
    filterfounderparams: FilterFounderParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.get_founders_by_level(
        level=filterfounderparams.level, session=session
    )


@router.get("/get_spheres_by_level")
async def get_stats(
    filterfounderparams: FilterFounderParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.get_sphere_by_level(
        level=filterfounderparams.level, session=session
    )


@router.get("/get_spheres_by_founder")
async def get_stats(founder: str, session: AsyncSession = Depends(get_session)):
    return await OrganizationsDAO.get_sphere_by_founder(
        founder=founder, session=session
    )


@router.get("/get_stats")
async def get_stats(
    filterchannelsparams: FilterChannelsParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.filter_channels(
        level=filterchannelsparams.level,
        founder=filterchannelsparams.founder,
        sphere=filterchannelsparams.sphere,
        sort=filterchannelsparams.sort,
        session=session,
    )
