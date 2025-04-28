import asyncio
from datetime import datetime

import httpx
import pytz
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from rich.console import Console
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_session
from app.organizations.constants import AMURTIMEZONE
from app.organizations.models import Organizations
from app.organizations.schemas import (
    OrganizationsDTO,
)
from app.statistic.models import Statistic
from app.vk.dao import VkDAO
from app.vk.funcs import (
    call,
    fetch_gos_page,
    get_activity,
    get_average_month_fulfillment_percentage,
    get_percentage_of_fulfillment_of_basic_requirements,
    get_week_fulfillment_percentage,
)

router = APIRouter(prefix="/vk", tags=["VK"])
console = Console(color_system="truecolor", width=140)


@router.get("/auth")
def auth(request: Request):
    # Формируем URL для авторизации в VK
    auth_url = f"https://oauth.vk.com/authorize?client_id={settings.CLIENT_ID}&display=page&redirect_uri={settings.REDIRECT_URI}&scope=friends,groups,stats,offline&response_type=code&v=5.131"
    return {"auth_url": auth_url}


@router.get("/init")
async def vk_init():
    url = f"https://oauth.vk.com/authorize?client_id={settings.CLIENT_ID}&display=page&redirect_uri={settings.REDIRECT_URI}&scope=friends,groups,stats,offline&response_type=code&v=5.131&state=init"

    return RedirectResponse(url, status_code=302)


@router.get("/callback")
async def callback(code: str, state: str = None):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth.vk.com/access_token",
            params={
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "redirect_uri": settings.REDIRECT_URI,
                "code": code,
            },
        )
    data = resp.json()

    if state == "init":
        auth = data["access_token"]

        groups = await call("groups.get", {"filter": "admin"}, auth)

        group_ids = ",".join(str(item) for item in groups["response"]["items"])

        url = f"https://oauth.vk.com/authorize?client_id={settings.CLIENT_ID}&display=page&redirect_uri={settings.REDIRECT_URI}&group_ids={group_ids}&scope=messages,stories,manage,app_widget&response_type=code&v=5.131&state=init_groups"

        return RedirectResponse(url, status_code=302)

    return data


@router.post("/get_stat")
async def get_stat(session: AsyncSession = Depends(get_session)):
    # Получаем все ID из таблицы accounts
    result = await session.execute(select(Organizations.channel_id))
    account_ids = result.scalars().all()

    # Разбиваем список по 500 значений
    chunks = [account_ids[i : i + 500] for i in range(0, len(account_ids), 500)]

    for chunk in chunks:
        # Преобразуем chunk к формату, подходящему для запроса
        group_ids = ",".join(str(item) for item in chunk)

        auth = settings.VK_SERVICE_TOKEN

        # Выполняем запрос, как в функции fgroup_info
        data = await call(
            "groups.getById", {"group_ids": group_ids, "fields": "members_count"}, auth
        )

        # Check if there is an error in the response
        if "error" in data:
            console.rule(f"[red] Error retrieving group data: {data['error']}")
            continue  # Skip this chunk or handle it as needed

        try:
            for group in data.get("response", {}).get("groups", []):
                # Генерируем date_id
                date_str = datetime.now(AMURTIMEZONE).strftime("%Y%m%d")
                date_id = f"{date_str}{group['id']}"

                # Добавляем или обновляем значения в таблице статистики
                stat = await session.get(Statistic, date_id)
                organization_stmt = (
                    select(Organizations)
                    .where(Organizations.channel_id == group["id"])
                    .options(selectinload(Organizations.statistic))
                )
                organization_result = await session.execute(organization_stmt)
                organization = organization_result.scalars().first()

                if not organization:
                    continue

                organization_dto = OrganizationsDTO.model_validate(
                    organization, from_attributes=True
                )

                if stat:
                    stat.members_count = group.get("members_count", 0)
                    stat.date_added = datetime.now(AMURTIMEZONE)
                    stat.fulfillment_percentage = (
                        await get_percentage_of_fulfillment_of_basic_requirements(
                            organization_dto.model_dump()
                        )
                    )
                    stat.activity = await get_activity(group["id"])
                else:
                    new_stat = Statistic(
                        date_id=date_id,
                        organization_id=organization.id,
                        date_added=datetime.now(AMURTIMEZONE),
                        fulfillment_percentage=await get_percentage_of_fulfillment_of_basic_requirements(
                            organization_dto.model_dump()
                        ),
                        members_count=group.get("members_count", 0),
                        activity=await get_activity(group["id"]),
                    )
                    session.add(new_stat)

            await session.commit()

            for group_id in chunk:
                organization_stmt = (
                    select(Organizations)
                    .where(Organizations.channel_id == group_id)
                    .options(selectinload(Organizations.statistic))
                )
                organization_result = await session.execute(organization_stmt)
                organization = organization_result.scalars().first()

                if not organization:
                    continue

                organization_dto = OrganizationsDTO.model_validate(
                    organization, from_attributes=True
                )
                week_percentage_of_fulfillment = get_week_fulfillment_percentage(
                    statistics=organization_dto.statistic
                )
                month_percentage_of_fulfillment = (
                    get_average_month_fulfillment_percentage(
                        statistics=organization_dto.statistic
                    )
                )

                update_stmt = (
                    update(Organizations)
                    .where(Organizations.channel_id == group_id)
                    .values(
                        average_week_fulfillment_percentage=week_percentage_of_fulfillment,
                        average_fulfillment_percentage=month_percentage_of_fulfillment,
                    )
                )
                await session.execute(update_stmt)

            await session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            await session.rollback()
        except httpx.ConnectError as e:
            print(f"Connection error: {e}")

    return {"status": "completed"}


@router.post("/get_group_data")
async def get_group_data(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Organizations.channel_id))
    organizations = result.scalars().all()

    tasks = [VkDAO.get_group_data(group_id=group_id) for group_id in organizations]

    batch_results = await asyncio.gather(*tasks)

    return {"status": f"completed: {len(batch_results)}", "data": batch_results}


@router.post("/wall_get_all")
async def wall_get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Organizations.channel_id))
    organizations = result.scalars().all()

    tasks = [VkDAO.wall_get_data(group_id=group_id) for group_id in organizations]
    batch_results = await asyncio.gather(*tasks)

    return {"status": f"completed: {len(batch_results)}", "data": batch_results}


@router.post("/get_weekly_audience_reach")
async def get_weekly_audience_reach(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Organizations.channel_id))
    organizations = result.scalars().all()

    tasks = [VkDAO.update_weekly_reach(group_id=group_id) for group_id in organizations]
    batch_results = await asyncio.gather(*tasks)
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail=f"completed: {len(batch_results)}"
    )


@router.post("/get_gos_bage")
async def get_gos_bage(session: AsyncSession = Depends(get_session)):
    batch_size = 50

    result = await session.execute(select(Organizations.id, Organizations.screen_name))
    organizations = result.all()

    for i in range(0, len(organizations), batch_size):
        batch = organizations[i : i + batch_size]
        all_ids_in_batch = [account.id for account in batch]

        tasks = [
            fetch_gos_page(
                f"https://vk.com/{organization.screen_name}", organization.id
            )
            for organization in batch
        ]
        batch_results = await asyncio.gather(*tasks)

        found_ids = [
            organization_id
            for organization_id in batch_results
            if organization_id is not None
        ]
        not_found_ids = list(set(all_ids_in_batch) - set(found_ids))

        print(f"Found IDs: {found_ids}")
        print(f"Not found IDs: {not_found_ids}")

        # Обновляем записи с найденным GovernmentCommunityBadge
        if found_ids:
            await session.execute(
                update(Organizations)
                .where(Organizations.id.in_(found_ids))
                .values(has_gos_badge=True)
            )

        # Обновляем записи без GovernmentCommunityBadge
        if not_found_ids:
            await session.execute(
                update(Organizations)
                .where(Organizations.id.in_(not_found_ids))
                .values(has_gos_badge=False)
            )

        await session.commit()

    return {"updated_accounts": len(organizations)}
