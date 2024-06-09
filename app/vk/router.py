import asyncio
import logging
from datetime import datetime

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from rich.console import Console
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.organizations.models import Organizations
from app.organizations.schemas import (
    OrganizationsBase,
    OrganizationsForStatistic,
    StatisticBase,
)
from app.vk.dao import VkDAO
from app.vk.funcs import (
    call,
    fetch_gos_page,
    get_percentage_of_fulfillment_of_basic_requirements,
)
from app.vk.models import Statistic

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

    print(data)

    if state == "init":
        auth = data["access_token"]
        await redis_.set("access_token", auth)

        groups = await call("groups.get", {"filter": "admin"}, auth)

        print(groups)

        group_ids = ",".join(str(item) for item in groups["response"]["items"])

        print(group_ids)

        url = f"https://oauth.vk.com/authorize?client_id={settings.CLIENT_ID}&display=page&redirect_uri={settings.REDIRECT_URI}&group_ids={group_ids}&scope=messages,stories,manage,app_widget&response_type=code&v=5.131&state=init_groups"

        return RedirectResponse(url, status_code=302)

    if state == "init_groups":
        groups = data["groups"]

        print(groups)

        for group in groups:
            await redis_.set(f"access_token_{group['group_id']}", group["access_token"])

        return RedirectResponse("https://vk.apps.icdv.ru", status_code=302)

    return data


@router.get("/get_stat")
async def get_stat(session: AsyncSession = Depends(get_session)):
    try:
        organizations_result = await session.execute(select(Organizations))
        organizations_list = organizations_result.scalars().all()
        organizations = {
            org.channel_id: OrganizationsBase.model_validate(
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

            fields = (
                "members_count,city,status,verified,description,cover,activity,menu"
            )

            data = await call(
                "groups.getById", {"group_ids": group_ids, "fields": fields}, auth
            )
            logging.info(f"API response: {data}")

            if not isinstance(data, dict):
                raise TypeError(
                    f"Expected data to be a dictionary, got {type(data)} instead"
                )

            if "error" in data:
                raise ValueError(f"API error: {data['error']}")

            response = data["response"]

            for group in response["groups"]:
                date_str = datetime.now().strftime("%Y%m%d")
                date_id = f"{date_str}{group['id']}"

                organization = organizations.get(group["id"])

                if not organization:
                    continue

                organization["city"] = (
                    group.get("city", {}).get("title")
                    if isinstance(group.get("city"), dict)
                    else None
                )
                organization["screen_name"] = group.get("screen_name")
                organization["status"] = group.get("status")
                organization["verified"] = True if group.get("verified") else False
                organization["has_description"] = (
                    True if group.get("description") else False
                )
                organization["has_avatar"] = (
                    True
                    if group.get("photo_50")
                    or group.get("photo_100")
                    or group.get("photo_200")
                    else False
                )
                organization["activity"] = group.get("activity")
                organization["has_widget"] = bool(group.get("menu"))
                organization["widget_count"] = len(
                    group.get("menu", {}).get("items", [])
                )
                organization["site"] = group.get("site")
                organization["type"] = group.get("type")
                organization["has_cover"] = (
                    True if group.get("cover").get("enabled") else False
                )
                organization["members_count"] = group.get("members_count", 0)
                organization["has_gos_badge"] = organization["has_gos_badge"]
                organization["posts"] = organization["posts"]
                organization["posts_1d"] = organization["posts_1d"]
                organization["posts_7d"] = organization["posts_7d"]
                organization["posts_30d"] = organization["posts_30d"]

                updated_organizations.append(organization)

                stat = await session.get(Statistic, date_id)
                if stat:
                    stat.members_count = group.get("members_count", 0)
                    stat.date_added = datetime.now().date()
                    stat.fulfillment_percentage = get_percentage_of_fulfillment_of_basic_requirements(organization)
                else:
                    new_stat = Statistic(
                        date_id=date_id,
                        organization_id=organization["id"],
                        date_added=datetime.now().date(),
                        members_count=group.get("members_count", 0),
                        fulfillment_percentage=get_percentage_of_fulfillment_of_basic_requirements(organization),
                    )
                    validated_stat = StatisticBase.model_validate(
                        new_stat, from_attributes=True
                    )
                    all_stats.append(validated_stat)
                    logging.info(f"Added new_stat: {validated_stat}")

        for organization in updated_organizations:
            stmt = (
                insert(Organizations)
                .values(**organization)
                .on_conflict_do_update(index_elements=["id"], set_=organization)
            )
            await session.execute(stmt)
        await session.commit()

        organizations = {
            org.id: OrganizationsForStatistic.model_validate(
                org, from_attributes=True
            ).model_dump()
            for org in organizations_list
        }

        for stat in all_stats:
            organization = organizations.get(stat.organization_id)
            if organization:
                fulfillment_percentage = (
                    get_percentage_of_fulfillment_of_basic_requirements(organization)
                )
                stat.fulfillment_percentage = fulfillment_percentage

                add_stat = insert(Statistic).values(
                    StatisticBase.model_validate(
                        stat, from_attributes=True
                    ).model_dump()
                ).on_conflict_do_update(
                    index_elements=["date_id"],
                    set_={
                        "members_count": stat.members_count,
                        "fulfillment_percentage": stat.fulfillment_percentage,
                        "date_added": stat.date_added,
                    }
                )
                await session.execute(add_stat)

        await session.commit()
        return {"status": "completed"}


    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await session.rollback()
        return {"status": "failed", "error": str(e)}
    finally:
        await session.close()


@router.get("/wall_get_all")
async def wall_get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Organizations.id))
    organizations = result.scalars().all()

    tasks = [VkDAO.wall_get_data(group_id=group_id) for group_id in organizations]
    batch_results = await asyncio.gather(*tasks)

    return {"status": f"completed: {len(batch_results)}", "data": batch_results}


@router.get("/get_gos_bage")
async def get_gos_bage(session: AsyncSession = Depends(get_session)):
    batch_size = 50
    pause_duration = 5  # Время паузы в секундах между батчами

    result = await session.execute(select(Organizations.id, Organizations.screen_name))
    accounts = result.all()

    for i in range(0, len(accounts), batch_size):
        batch = accounts[i : i + batch_size]
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

        # Пауза между батчами
        await asyncio.sleep(pause_duration)

    return {"updated_accounts": len(accounts)}
