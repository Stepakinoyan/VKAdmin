from fastapi import APIRouter, Depends

from app.organizations.dao import OrganizationsDAO
from app.organizations.params import FilterChannelsParams, FilterFounderParams

router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_founders")
async def filter_channels(filterfounderparams: FilterFounderParams = Depends()):
    return await OrganizationsDAO.get_founders_by_level(filterfounderparams.level)


@router.get("/get_spheres")
async def get_stats(founder: str):
    return await OrganizationsDAO.get_sphere_by_founder(founder=founder)


@router.get("/get_stats")
async def get_stats(filterchannelsparams: FilterChannelsParams = Depends()):
    return await OrganizationsDAO.filter_channels(
        filterchannelsparams.level,
        filterchannelsparams.founder,
        filterchannelsparams.sphere,
        filterchannelsparams.sort,
    )
