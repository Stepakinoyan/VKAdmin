import asyncio
import json
import time
from datetime import datetime, timedelta

import httpx
import pytz
import redis.asyncio as redis
from rich.console import Console
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import settings
from app.database import engine
from app.organizations.models import Organizations
from fake_useragent import UserAgent
from app.organizations.types import OrganizationType
from app.vk.schemas import StatisticDTO
from app.vk.types import StatisticType
from typing import TypeAlias

redis_ = redis.from_url(
    settings.redis_url,
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


async def fetch_gos_page(url, organization_id) -> int | None:
    headers = {"Accept-Language": "ru-RU,ru;q=0.9", "User-Agent": UserAgent().random}
    async with semaphore:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            if (
                response.status_code == 200
                and "GovernmentCommunityBadge GovernmentCommunityBadge--tooltip"
                in response.text
            ):
                print(f"{organization_id}: {url}")
                return organization_id
            elif response.status_code in [400, 401, 403, 500]:
                print(f"[{response.status_code}] {organization_id}: {url}")
        return None


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


Percent: TypeAlias = int


def get_percentage_of_fulfillment_of_basic_requirements(
    organization: OrganizationType,
) -> Percent:
    percentage = 0

    # Подключение к компоненту «Госпаблики» (20 %)
    if organization.get("has_gos_badge") is True:
        percentage += 20
        print("has_gos_badge: +20%")

    # Оформление (20 %)
    if organization.get("has_avatar") is True:
        percentage += 5
        print("has_avatar: +5%")
    if organization.get("has_description") is True:
        percentage += 5
        print("has_description: +5%")
    if organization.get("has_cover") is True:
        percentage += 10
        print("has_cover: +10%")

    # Виджеты (10 %)
    widget_count = organization.get("widget_count")
    if widget_count is not None:
        if widget_count >= 2:
            percentage += 10
            print("widget_count >= 2: +10%")
        elif widget_count == 1:
            percentage += 5
            print("widget_count == 1: +5%")

    # Активность (30 %)
    posts_30d = organization.get("posts_30d")
    if posts_30d is not None and posts_30d >= 3:
        percentage += 30
        print("posts_30d >= 3: +30%")

    # Общий охват аудитории за неделю (10 %)
    members_count = organization.get("members_count")
    print(f"members_count: {members_count}")

    if members_count is not None and members_count > 0:
        total_views = organization.get("views_7d")
        if total_views is not None and total_views > 0:
            reach_percentage = (total_views / members_count) * 100

            if reach_percentage > 70:
                percentage += 10
                print("reach_percentage > 70: +10%")
            elif 50 <= reach_percentage <= 70:
                percentage += 5
                print("50 <= reach_percentage <= 70: +5%")
            elif 30 <= reach_percentage < 50:
                percentage += 2
                print("30 <= reach_percentage < 50: +2%")

    posts_7d = organization.get("posts_7d")
    posts = organization.get("posts")
    if (
        posts_7d is not None
        and posts is not None
        and posts_30d is not None
        and posts_30d > 0
        and members_count is not None
        and members_count > 0
    ):
        avg_reach_per_post = posts / posts_30d
        avg_reach_percentage = (avg_reach_per_post / members_count) * 100
        if avg_reach_percentage > 70:
            percentage += 10
            print("avg_reach_percentage > 70: +10%")

    print(
        f"Total percentage for organization {organization['channel_id']}: {percentage}%"
    )

    return percentage


def get_average_month_fulfillment_percentage(
    statistics: list[StatisticType],
) -> Percent:
    if not statistics:
        return 0

    # Извлечение процентов выполнения
    fulfillment_percentages = [stat.fulfillment_percentage for stat in statistics]
    average_fulfillment_percentage = round(
        sum(fulfillment_percentages) / len(fulfillment_percentages)
    )
    # Возвращаем среднее арифметическое всех процентов выполнения
    if average_fulfillment_percentage > 100:
        return 100
    return average_fulfillment_percentage


def get_week_fulfillment_percentage(statistics: list[StatisticDTO]) -> Percent:
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    fulfillment_percentages = []

    for item in statistics:
        if start_of_week.date() <= item.date_added.date() <= end_of_week.date():
            fulfillment_percentages.append(item.fulfillment_percentage)

    if fulfillment_percentages:
        average_week_fulfillment_percentage = round(
            sum(fulfillment_percentages) / len(fulfillment_percentages)
        )

        if average_week_fulfillment_percentage > 100:
            return 100

    return 0

async def filter_posts_by_current_week(group_id: int):
    # Получаем данные
    data = await call(
        "wall.get",
        {
            "owner_id": -group_id,
            "count": 100,
            "extended": 1,
            "filter": "owner",
            "fields": "counters,wall",
        },
        settings.VK_SERVICE_TOKEN,
    )

    # Проверка наличия данных
    if not data or not data.get("response") or not data["response"].get("items"):
        return 0

    # Устанавливаем временную зону на Asia/Yakutsk
    yakutsk_tz = pytz.timezone('Asia/Yakutsk')
    
    # Текущая дата и время в часовом поясе Asia/Yakutsk
    now_yakutsk = datetime.now(yakutsk_tz)
    
    # Начало недели (понедельник, 00:00 в часовом поясе Asia/Yakutsk)
    start_of_week = now_yakutsk - timedelta(
        days=now_yakutsk.weekday(),
        hours=now_yakutsk.hour,
        minutes=now_yakutsk.minute,
        seconds=now_yakutsk.second,
        microseconds=now_yakutsk.microsecond
    )
    
    # Конец недели (воскресенье, 23:59:59 в часовом поясе Asia/Yakutsk)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Переводим начало и конец недели в UTC для сравнения с Unix time
    start_of_week_utc = start_of_week.astimezone(pytz.utc)
    end_of_week_utc = end_of_week.astimezone(pytz.utc)

    # Фильтруем посты по дате и проверяем наличие ключа views
    filtered_views = [
        post.get("views", {}).get("count", 0)
        for post in data["response"]["items"]
        if start_of_week_utc.timestamp() <= post['date'] <= end_of_week_utc.timestamp()
    ]
    
    return sum(filtered_views)