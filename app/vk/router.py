import asyncio
import json
import logging
from datetime import datetime

import httpx
from pydantic import ValidationError
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from rich.console import Console
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.organizations.funcs import get_new_stats
from app.organizations.models import Organizations
from app.organizations.schemas import (
    OrganizationsDTO,
)
from app.vk.dao import VkDAO
from app.vk.schemas import StatisticDTO
from app.vk.funcs import (
    call,
    fetch_gos_page,
    get_average_month_fulfillment_percentage,
    get_week_fulfillment_percentage,
    get_percentage_of_fulfillment_of_basic_requirements,
)
from app.vk.models import Statistic
import pytz

router = APIRouter(prefix="/vk", tags=["VK"])
console = Console(color_system="truecolor", width=140)
redis_ = redis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_keepalive=True,
)


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
        await redis_.set("access_token", auth)

        groups = await call("groups.get", {"filter": "admin"}, auth)

        

        group_ids = ",".join(str(item) for item in groups["response"]["items"])

        url = f"https://oauth.vk.com/authorize?client_id={settings.CLIENT_ID}&display=page&redirect_uri={settings.REDIRECT_URI}&group_ids={group_ids}&scope=messages,stories,manage,app_widget&response_type=code&v=5.131&state=init_groups"

        return RedirectResponse(url, status_code=302)

    if state == "init_groups":
        groups = data["groups"]

        for group in groups:
            await redis_.set(f"access_token_{group['group_id']}", group["access_token"])

        return RedirectResponse("https://vk.apps.icdv.ru", status_code=302)

    return data


@router.post("/get_stat")
async def get_stat(session: AsyncSession = Depends(get_session)):
    try:
        amurtime = pytz.timezone("Asia/Yakutsk")

        # Получение списка организаций
        organizations_result = await session.execute(select(Organizations))
        organizations_list = organizations_result.scalars().all()

        if not organizations_list:
            return {"status": "No organizations found"}

        organizations = {
            org.channel_id: OrganizationsDTO.model_validate(
                org, from_attributes=True
            ).model_dump()
            for org in organizations_list
        }

        chunks = [
            organizations_list[i : i + 500]
            for i in range(0, len(organizations_list), 500)
        ]

        all_stats = []
        updated_organizations = []

        for chunk in chunks:
            group_ids = ",".join(str(org.channel_id) for org in chunk)
            auth = settings.VK_SERVICE_TOKEN
            fields = "members_count,city,status,description,cover,activity,menu"

            data = await call(
                "groups.getById", {"group_ids": group_ids, "fields": fields}, auth
            )

            if not isinstance(data, dict):
                raise TypeError(
                    f"Expected data to be a dictionary, got {type(data)} instead"
                )

            if "error" in data:
                raise ValueError(f"API error: {data['error']}")

            response = data.get("response", [])
            for group in response["groups"]:
                date_str = datetime.now(amurtime).strftime("%Y%m%d")
                date_id = f"{date_str}{group['id']}"

                organization = organizations.get(group["id"])

                if not organization:
                    continue

                organization.update(
                    {
                        "city": group.get("city", {}).get("title")
                        if isinstance(group.get("city"), dict)
                        else None,
                        "screen_name": group.get("screen_name"),
                        "status": group.get("status"),
                        "date_added": datetime.now(amurtime).date(),
                        "has_description": bool(group.get("description")),
                        "has_avatar": any(
                            group.get(f"photo_{size}") for size in (50, 100, 200)
                        ),
                        "activity": group.get("activity"),
                        "has_widget": bool(group.get("menu")),
                        "widget_count": len(group.get("menu", {}).get("items", [])),
                        "site": group.get("site"),
                        "type": group.get("type"),
                        "has_cover": group.get("cover", {}).get("enabled", False),
                        "members_count": group.get("members_count", 0),
                    }
                )

                updated_organizations.append(organization)

                stat = await session.get(Statistic, date_id)
                if stat:
                    stat.members_count = group.get("members_count", 0)
                    stat.date_added = datetime.now(amurtime).date()
                    stat.fulfillment_percentage = (
                        get_percentage_of_fulfillment_of_basic_requirements(
                            organization
                        )
                    )
                else:
                    new_stat = Statistic(
                        date_id=date_id,
                        organization_id=organization["id"],
                        date_added=datetime.now(amurtime).date(),
                        members_count=group.get("members_count", 0),
                        fulfillment_percentage=get_percentage_of_fulfillment_of_basic_requirements(
                            organization
                        ),
                    )
                    try:
                        validated_stat = StatisticDTO.model_validate(
                            new_stat, from_attributes=True
                        )
                        all_stats.append(validated_stat)
                    except ValidationError as e:
                        logging.error(f"Validation error: {e}")
                        continue

        for organization in updated_organizations:
            stmt = (
                insert(Organizations)
                .values(**organization)
                .on_conflict_do_update(index_elements=["channel_id"], set_=organization)
            )
            await session.execute(stmt)
        await session.commit()

        organizations = {
            org.id: OrganizationsDTO.model_validate(
                org, from_attributes=True
            ).model_dump()
            for org in organizations_list
        }

        for stat in all_stats:
            organization = organizations.get(stat.organization_id)
            if organization:
                stat.fulfillment_percentage = (
                    get_percentage_of_fulfillment_of_basic_requirements(organization)
                )
                add_stat = (
                    insert(Statistic)
                    .values(
                        StatisticDTO.model_validate(
                            stat, from_attributes=True
                        ).model_dump()
                    )
                    .on_conflict_do_update(
                        index_elements=["date_id"],
                        set_={
                            "members_count": stat.members_count,
                            "fulfillment_percentage": stat.fulfillment_percentage,
                            "date_added": stat.date_added,
                        },
                    )
                )
                await session.execute(add_stat)
        await session.commit()

        for organization in updated_organizations:
            statistics_result = await session.execute(
                select(Statistic).where(Statistic.organization_id == organization["id"])
            )
            statistics_list_raw = statistics_result.scalars().all()
            statistics_list = [
                StatisticDTO.model_validate(stat, from_attributes=True)
                for stat in statistics_list_raw
            ]

            new_stats = get_new_stats(statistics_list)

            if new_stats:
                average_month_fulfillment_percentage = get_average_month_fulfillment_percentage(
                    new_stats
                )
                average_week_fulfillment_percentage = get_week_fulfillment_percentage(
                    new_stats
                )

                try:
                    update_stmt = (
                        update(Organizations)
                        .where(Organizations.id == organization["id"])
                        .values(
                            average_week_fulfillment_percentage=average_week_fulfillment_percentage,
                            average_fulfillment_percentage=average_month_fulfillment_percentage
                        )
                    )
                    await session.execute(update_stmt)
                except Exception as e:
                    logging.error(
                        f"Error updating average fulfillment percentage for organization_id: {organization['id']} - {e}"
                    )
                    continue

        await session.commit()

        return {"status": "completed"}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await session.rollback()
        return {"status": "failed", "error": str(e)}
    finally:
        await session.close()




@router.post("/wall_get_all")
async def wall_get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Organizations.channel_id))
    organizations = result.scalars().all()

    tasks = [VkDAO.wall_get_data(group_id=group_id) for group_id in organizations]
    batch_results = await asyncio.gather(*tasks)

    return {"status": f"completed: {len(batch_results)}", "data": batch_results}


@router.post("/get_gos_bage")
async def get_gos_bage(session: AsyncSession = Depends(get_session)):
    batch_size = 50

    result = await session.execute(select(Organizations.id, Organizations.screen_name))
    accounts = result.all()

    for i in range(0, len(accounts), batch_size):
        batch = accounts[i : i + batch_size]
        print(batch)
        all_ids_in_batch = [account.id for account in batch]

        tasks = [
            fetch_gos_page(f"https://vk.com/{account.screen_name}", account.id)
            for account in batch
        ]
        batch_results = await asyncio.gather(*tasks)

        found_ids = [account_id for account_id in batch_results if account_id]
        not_found_ids = list(set(all_ids_in_batch) - set(found_ids))

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

    return {"updated_accounts": len(accounts)}
