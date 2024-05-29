import asyncio
import logging
from datetime import datetime

import httpx
import redis.asyncio as redis
from fastapi import (APIRouter, Depends, Request)
from fastapi.responses import RedirectResponse
from rich.console import Console
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.organizations.models import Organizations
from app.organizations.schemas import OrganizationsBase
from app.vk.dao import VkDAO
from app.vk.funcs import (call, fetch_gos_page,
                          get_percentage_of_fulfillment_of_basic_requirements)
from app.vk.models import Account, Statistic

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
        # Получаем все ID и channel_id из таблицы accounts
        get_result = select(
            Account.id,
            Account.channel_id,
            Account.has_avatar,
            Account.has_description,
            Account.has_cover,
            Account.widget_count,
            Account.posts_7d,
            Account.members_count,
        )
        result = await session.execute(get_result)
        accounts = result.all()
        account_map = {
            account[1]: account for account in accounts
        }  # channel_id -> account data tuple

        # Получаем все организации и создаем словарь для быстрого поиска по channel_id
        organizations_result = await session.execute(select(Organizations))
        organizations_list = organizations_result.scalars().all()
        organizations = {
            org.channel_id: OrganizationsBase.model_validate(
                org, from_attributes=True
            ).model_dump()
            for org in organizations_list
        }

        # Разбиваем список по 500 значений
        chunks = [accounts[i : i + 500] for i in range(0, len(accounts), 500)]

        for chunk in chunks:
            # Преобразуем chunk к формату, подходящему для запроса
            group_ids = ",".join(
                str(item[1]) for item in chunk
            )  # item[1] это channel_id
            auth = settings.VK_SERVICE_TOKEN

            # Выполняем запрос, как в функции fgroup_info
            data = await call(
                "groups.getById",
                {"group_ids": group_ids, "fields": "members_count"},
                auth,
            )

            print(data)

            if "response" in data and "groups" in data["response"]:
                for group in data["response"]["groups"]:
                    # Генерируем date_id
                    date_str = datetime.now().strftime("%Y%m%d")
                    date_id = f"{date_str}{group['id']}"

                    # Получаем account_id через channel_id
                    account_data = account_map.get(group["id"])
                    if not account_data:
                        continue  # Если account_data не найден, пропускаем эту группу

                    account_id = account_data[0]
                    account_dict: Account = {
                        "id": account_data[0],
                        "channel_id": account_data[1],
                        "screen_name": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "type": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "name": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "city": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "activity": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "verified": False,  # Заполните это поле, если у вас есть соответствующее значение
                        "has_avatar": account_data[2],
                        "has_cover": account_data[3],
                        "has_description": account_data[4],
                        "has_gos_badge": False,  # Заполните это поле, если у вас есть соответствующее значение
                        "has_widget": False,  # Заполните это поле, если у вас есть соответствующее значение
                        "widget_count": account_data[5],
                        "members_count": account_data[6],
                        "site": "",  # Заполните это поле, если у вас есть соответствующее значение
                        "date_added": None,  # Заполните это поле, если у вас есть соответствующее значение
                        "posts": 0,  # Заполните это поле, если у вас есть соответствующее значение
                        "posts_1d": 0,  # Заполните это поле, если у вас есть соответствующее значение
                        "posts_7d": account_data[7],
                        "posts_30d": 0,  # Заполните это поле, если у вас есть соответствующее значение
                        "post_date": None,  # Заполните это поле, если у вас есть соответствующее значение
                    }

                    # Получаем организацию для вычисления процента исполнения основных требований
                    organization = organizations.get(group["id"])
                    fulfillment_percentage = 0
                    if organization:
                        fulfillment_percentage = (
                            get_percentage_of_fulfillment_of_basic_requirements(
                                organization, account_dict
                            )
                        )

                    # Добавляем или обновляем значения в таблице статистики
                    stat = await session.get(Statistic, date_id)
                    if stat:
                        stat.members_count = group.get("members_count", 0)
                        stat.date_added = datetime.now().date
                        stat.fulfillment_percentage = fulfillment_percentage
                    else:
                        new_stat = Statistic(
                            date_id=date_id,
                            account_id=account_id,  # Используем account_id
                            date_added=datetime.now().date,
                            members_count=group.get("members_count", 0),
                            fulfillment_percentage=fulfillment_percentage,
                        )
                        session.add(new_stat)

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
    result = await session.execute(select(Account.id))
    accounts = result.scalars().all()

    tasks = [VkDAO.wall_get_data(group_id) for group_id in accounts]
    batch_results = await asyncio.gather(*tasks)

    return {"status": f"completed: {len(batch_results)}", "data": batch_results}


@router.get("/get_gos_bage")
async def get_gos_bage(session: AsyncSession = Depends(get_session)):
    batch_size = 50

    result = await session.execute(select(Account.id, Account.screen_name))
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
                update(Account)
                .where(Account.id.in_(found_ids))
                .values(has_gos_badge=True)
            )

        # Обновляем записи без GovernmentCommunityBadge
        if not_found_ids:
            await session.execute(
                update(Account)
                .where(Account.id.in_(not_found_ids))
                .values(has_gos_badge=False)
            )

        await session.commit()

    return {"updated_accounts": len(accounts)}
