import asyncio
import time
from datetime import datetime

import httpx
import redis.asyncio as redis
from openpyxl import Workbook
from rich.console import Console
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import settings
from app.database import engine
from app.organizations.models import Organizations
from fake_useragent import UserAgent
from app.vk.schemas import Organization
from typing import TypeAlias

redis_ = redis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_keepalive=True,
)
console = Console(color_system="truecolor", width=140)


async def call(method: str, params: dict, access_token: str, retries: int = 3):
    base_url = "https://api.vk.com/method/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }

    params["v"] = "5.217"

    async with httpx.AsyncClient(timeout=30.0, http2=True) as client:
        for _ in range(retries):  # Пытаемся выполнить запрос retries раз
            if retries < 3:
                console.rule(f"retries {retries}")
            response = await client.post(
                f"{base_url}{method}", params=params, headers=headers
            )

            # print(response.status_code)

            if response.status_code in [400, 403, 404, 500, 502]:
                console.rule(f"[red] ERROR {response.status_code}")
                return {"error": response.status_code}

            response_data = response.json()
            # Проверяем, содержит ли ответ ошибку "Too many requests per second"
            if (
                "error" in response_data
                and response_data["error"].get("error_code") == 6
            ):
                console.rule(f"[red] {response.url} Too many requests per second")
                # Если да, делаем паузу и пробуем ещё раз
                await asyncio.sleep(20)
            else:
                # Если нет ошибки, или это была последняя попытка, возвращаем результат
                return response_data
        return {"error": "Max retries exceeded"}


def load_vk_links(file_path: str) -> list:
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Remove any trailing or leading whitespace from each line
    lines = [line.strip() for line in lines]

    # Split the list into chunks of 500 items each
    chunks = [lines[i : i + 500] for i in range(0, len(lines), 500)]

    return chunks


async def fetch_gos_page(url, organization_id):
    headers = {
        "Accept-Language": "ru-RU,ru;q=0.9",
        "User-Agent": UserAgent().random,
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=80.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200 and "GovernmentCommunityBadge" in response.text:
            print(f"{organization_id}: {url}")
            return organization_id
        elif response.status_code in [400, 401, 403, 500]:
            print(f"[{response.status_code}] {organization_id}: {url}")
    return None


async def save_accounts_to_xlsx(file_path: str, session: AsyncSession):
    # 1. Fetch all data from the accounts table
    result = await session.execute(select(Organizations))
    organizations = result.scalars().all()

    # 2. Create a new XLSX workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Accounts"

    # Set headers for the sheet
    headers = [
        "id",
        "screen_name",
        "type",
        "name",
        "city",
        "activity",
        "verified",
        "has_avatar",
        "has_cover",
        "has_description",
        "has_gos_badge",
        "has_widget",
        "widget_count",
        "members_count",
        "site",
        "date_added",
        "posts",
        "posts_1d",
        "posts_7d",
        "posts_30d",
        "post_date",
    ]
    ws.append(headers)

    # Append account data to the sheet
    for organization in organizations:
        ws.append(
            [
                organization.id,
                organization.screen_name,
                organization.type,
                organization.name,
                organization.city,
                organization.activity,
                organization.verified,
                organization.has_avatar,
                organization.has_cover,
                organization.has_description,
                organization.has_gos_badge,
                organization.has_widget,
                organization.widget_count,
                organization.members_count,
                organization.site,
                organization.date_added,
                organization.posts,
                organization.posts_1d,
                organization.posts_7d,
                organization.posts_30d,
                organization.post_date,
            ]
        )

    # Save the workbook to the specified file path
    wb.save(file_path)


semaphore = asyncio.Semaphore(3)


async def wall_get_data(group_id: int):
    async with semaphore:
        data = await call(
            "wall.get",
            {
                # "domain": domain,
                "owner_id": -group_id,
                "count": 100,
                "extended": 1,
                "filter": "owner",
                "fields": "counters,wall",
                # "fields" : "counters,members_count,main_section,activity,ban_info,city,contacts,cover,description,fixed_post,links,place,site,verified,wiki_page,wall"
            },
            settings.VK_SERVICE_TOKEN,
        )

        # print(data)

        if "response" in data and data.get("response", {}).get("count") > 0:
            print(f">> {data['response']['count']}")

            # Получаем текущую дату в unix timestamp
            current_time = int(time.time())

            # Определяем интервалы в секундах
            one_day = 86400  # 24 * 60 * 60
            seven_days = 7 * one_day
            thirty_days = 30 * one_day

            # Инициализируем счетчики
            count_1_day = 0
            count_7_days = 0
            count_30_days = 0

            # Извлекаем даты всех элементов
            dates = [item["date"] for item in data["response"]["items"]]

            # Для каждой даты увеличиваем соответствующий счетчик
            for date in dates:
                if current_time - date < one_day:
                    count_1_day += 1
                if current_time - date < seven_days:
                    count_7_days += 1
                if current_time - date < thirty_days:
                    count_30_days += 1

            data["group_id"] = data["response"]["groups"][0]["id"]
            data["posts"] = data["response"]["count"]
            data["posts_1d"] = count_1_day
            data["posts_7d"] = count_7_days
            data["posts_30d"] = count_30_days
            data["first_item_date"] = dates[0]
            data["last_item_date"] = dates[-1]

            async_session = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )
            async with async_session() as session:
                async with session.begin():
                    db_item = await session.get(Organizations, group_id)
                    # print(db_item)
                    if db_item:
                        db_item.posts = data["posts"]
                        db_item.posts_1d = data["posts_1d"]
                        db_item.posts_7d = data["posts_7d"]
                        db_item.posts_30d = data["posts_30d"]
                        db_item.post_date = datetime.utcfromtimestamp(
                            data["first_item_date"]
                        )

                        print(f">>{data['group_id']}: {data['posts']}")

                        await session.commit()

                        return {data["group_id"]: "DB"}
                    else:
                        print(data)
                        return {data["group_id"]: data}

        else:
            print(f"{group_id}: NO DATA", data)

            return {group_id: "NO DATA"}

        return group_id


"""
Светофор базируется на процентах исполнения основных требований: 
            подключение — 10 %,
            госметка — 10 %,
            оформление 20 %,
            виджеты — 10 %,
            активность — 30 %,
            общий охват аудитории — 10 %,средний охват публикации — 5 %.
"""

Precent: TypeAlias = int | float


def get_percentage_of_fulfillment_of_basic_requirements(
    organization: Organization,
) -> Precent:
    percentage = 0

    # Подключение к компоненту «Госпаблики» (10 %)
    if organization.get("has_gos_badge") is True:
        percentage += 10

    # Госметка (10 %)
    if organization.get("verified") is True:
        percentage += 10

    # Оформление (20 %)
    if organization.get("has_avatar") is True:
        percentage += 5
    if organization.get("has_description") is True:
        percentage += 5
    if organization.get("has_cover") is True:
        percentage += 10

    # Виджеты (10 %)
    widget_count = organization.get("widget_count")
    if widget_count is not None:
        if widget_count >= 2:
            percentage += 10
        elif widget_count == 1:
            percentage += 5

    # Активность (30 %)
    posts_30d = organization.get("posts_30d")
    if posts_30d is not None and posts_30d >= 3:
        percentage += 30

    # Общий охват аудитории за неделю (10 %)
    members_count = organization.get("members_count")
    if members_count is not None and members_count > 0:
        reach_percentage = 0  # Предположим, что охват в процентах от количества подписчиков вычисляется извне
        if reach_percentage > 70:
            percentage += 10
        elif 50 <= reach_percentage <= 70:
            percentage += 7
        elif 30 <= reach_percentage < 50:
            percentage += 5

    posts_7d = organization.get("posts_30d")
    posts = organization.get("posts")
    if (
        posts_7d is not None
        and posts is not None
        and posts_7d > 0
        and members_count is not None
        and members_count > 0
    ):
        avg_reach_per_post = posts / posts_30d
        avg_reach_percentage = (avg_reach_per_post / members_count) * 100
        if avg_reach_percentage > 70:
            percentage += 5

    return percentage
