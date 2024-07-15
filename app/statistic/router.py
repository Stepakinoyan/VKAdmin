from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.statistic.dao import StatisticDAO

router = APIRouter(prefix="/stat", tags=["Статистика"])


@router.get("/get_dates")
async def get_dates(
    session: AsyncSession = Depends(get_session),
):
    return await StatisticDAO.get_dates(
        session=session,
    )
