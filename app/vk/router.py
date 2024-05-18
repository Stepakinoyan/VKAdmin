import asyncio
from datetime import datetime
import logging

import httpx
import redis.asyncio as redis
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from rich.console import Console
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.vk.dao import VkDAO
from app.vk.funcs import call, fetch_gos_page, save_accounts_to_xlsx, wall_get_data
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
        await redis_.set(f"access_token", auth)

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
        # Получаем все ID из таблицы accounts
        get_result = select(Account.id)
        result = await session.execute(get_result)
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

            if "response" in data and "groups" in data["response"]:
                for group in data["response"]["groups"]:
                    # Генерируем date_id
                    date_str = datetime.now().strftime("%Y%m%d")
                    date_id = f"{date_str}{group['id']}"

                    # Добавляем или обновляем значения в таблице статистики
                    stat = await session.get(Statistic, date_id)
                    if stat:
                        stat.members_count = group.get("members_count", 0)
                        stat.date_added = datetime.now()
                    else:
                        new_stat = Statistic(
                            date_id=date_id,
                            account_id=group["id"],
                            date_added=datetime.now(),
                            members_count=group.get("members_count", 0),
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
    # list = accounts[0:20]

    # for i, group_id in enumerate(accounts):
    #     wall = await wall_get(i, group_id, session)
    #     print(f"{i}-{group_id}: {wall}")

    tasks = [VkDAO.wall_get_data(group_id) for group_id in accounts]
    batch_results = await asyncio.gather(*tasks)

    # await session.commit()

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


@router.get("/group_info")
async def group_info(group_ids: str):

    auth = await redis_.get(f"access_token")

    data = await call(
        "groups.getById",
        {
            "group_ids": group_ids,
            "fields": "counters,members_count,activity,verified,cover,description,site,phone,city,place,contacts,addresses,menu",
            # "fields" : "counters,members_count,activity,ban_info,city,contacts,cover,description,fixed_post,links,place,site,verified,wiki_page"
        },
        auth,
    )

    data = data["response"]["groups"][0]

    print(data)

    data["has_avatar"] = bool(data.get("photo_50"))
    data["has_cover"] = bool(data.get("cover", {}).get("enabled", 0))
    data["has_description"] = bool(data.get("description"))
    data["has_widget"] = bool(data.get("menu"))
    data["widget_count"] = len(data.get("menu", {}).get("items", []))

    return data

# @router.get("/wall_get")
# async def wall_get(group_id: int):

#     result = await wall_get_data(group_id)
#     print(result)

#     return result

# @router.get("/xlsx", tags=["accounts"])
# async def download_accounts_xlsx(session: AsyncSession = Depends(get_session)):
#     file_path = "accounts_data.xlsx"
#     await save_accounts_to_xlsx(session=session, file_path=file_path)
#     return FileResponse(
#         file_path,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         filename="accounts_data.xlsx",
#     )
