from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Users
from app.auth.users import get_current_user
from app.database import get_session
from app.organizations.dao import OrganizationsDAO
from app.organizations.exceptions import InvalidDatesException
from app.organizations.params import (
    FilterChannelsParams,
    FilterFounderParams,
    FilterSpheresParams,
)
from app.organizations.schemas import FounderDTO, OrganizationsDTO, SphereDTO
from app.organizations.service import service as organization_service


router = APIRouter(prefix="/filter", tags=["Фильтрация данных"])


@router.get("/get_levels")
async def get_levels(
    current_user: Annotated[Users, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    return await OrganizationsDAO.get_levels(user=current_user, session=session)


@router.get("/get_founders")
async def get_founders(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterfounderparams: FilterFounderParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[FounderDTO]:
    return await OrganizationsDAO.get_founders_by_level(
        level=filterfounderparams.level, user=current_user, session=session
    )


@router.get("/get_spheres_by")
async def get_spheres(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterspheresparams: FilterSpheresParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[SphereDTO]:
    return await OrganizationsDAO.get_spheres_by(
        level=filterspheresparams.level,
        user=current_user,
        session=session,
    )


@router.get("/get_stats", response_model_exclude_none=True)
async def get_stats(
    current_user: Annotated[Users, Depends(get_current_user)],
    filterchannelsparams: FilterChannelsParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[OrganizationsDTO]:
    if (
        filterchannelsparams.date_from
        and filterchannelsparams.date_to
        and filterchannelsparams.date_from > filterchannelsparams.date_to
    ):
        raise InvalidDatesException

    return await organization_service.filter_channels(
        level=filterchannelsparams.level,
        founder=filterchannelsparams.founder,
        name=filterchannelsparams.name,
        sphere=filterchannelsparams.sphere,
        zone=filterchannelsparams.zone,
        date_from=filterchannelsparams.date_from,
        date_to=filterchannelsparams.date_to,
        user=current_user,
        session=session,
    )
