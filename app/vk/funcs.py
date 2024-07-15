import asyncio
import time
from datetime import datetime, timedelta
from typing import TypeAlias

import httpx
import pytz
import redis.asyncio as redis
from rich.console import Console
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import settings
from app.database import engine
from app.organizations.models import Organizations
from app.organizations.types import OrganizationType
from app.statistic.schemas import Activity, StatisticDTO

redis_ = redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_keepalive=True,
)
console = Console(color_system="truecolor", width=140)
amurtime = pytz.timezone("Asia/Yakutsk")


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


semaphore = asyncio.Semaphore(3)


async def fetch_gos_page(url, organization_id) -> int | None:
    headers = {
        "Accept-Language": "ru-RU,ru;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }
    async with semaphore:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(url, headers=headers)

            if (
                response.status_code == 200
                and "GovernmentCommunityBadge GovernmentCommunityBadge--tooltip"
                in response.text
            ):
                print(f"Found badge for {organization_id}: {url}")
                return organization_id
            else:
                print(
                    f"Badge not found or error for {organization_id}: {url} with status {response.status_code}"
                )
        return None


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


async def get_percentage_of_fulfillment_of_basic_requirements(
    organization: OrganizationType,
) -> Percent:
    percentage = 0

    # Госметка (10 %)
    if organization.get("has_gos_badge"):
        percentage += 10
        print("has_gos_badge: +10%")

    # Оформление (20 %)
    if organization.get("has_avatar"):
        percentage += 5
        print("has_avatar: +5%")
    if organization.get("has_description"):
        percentage += 5
        print("has_description: +5%")
    if organization.get("has_cover"):
        percentage += 10
        print("has_cover: +10%")

    # Виджеты (10 %)
    widget_count = organization.get("widget_count", 0)
    if widget_count >= 2:
        percentage += 10
        print("widget_count >= 2: +10%")
    elif widget_count == 1:
        percentage += 5
        print("widget_count == 1: +5%")

    # Активность (40 %)
    posts_7d = organization.get("posts_7d", 0)
    if posts_7d >= 3:
        percentage += 40
        print("posts_7d >= 3: +40%")

    # Общий охват аудитории за неделю (10 %)
    members_count = organization.get("members_count", 0)
    weekly_audience_reach = organization.get("weekly_audience_reach", 0)
    if members_count > 0:
        reach_percentage = (weekly_audience_reach / members_count) * 100
        if reach_percentage > 70:
            percentage += 10
            print("reach_percentage > 70: +10%")
        elif 50 <= reach_percentage <= 70:
            percentage += 7
            print("50 <= reach_percentage <= 70: +7%")
        elif 30 <= reach_percentage < 50:
            percentage += 5
            print("30 <= reach_percentage < 50: +5%")

    print(
        f"Total percentage for organization {organization['channel_id']}: {percentage}%"
    )

    return percentage


def get_average_month_fulfillment_percentage(
    statistics: list[StatisticDTO],
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


def get_week_fulfillment_percentage(
    statistics: list[StatisticDTO], timezone: str = "Asia/Yakutsk"
) -> int:
    amurtime = pytz.timezone(timezone)
    today = datetime.now(amurtime)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    fulfillment_percentages = []

    for item in statistics:
        item_date = item.date_added.astimezone(amurtime)
        if start_of_week.date() <= item_date.date() <= end_of_week.date():
            fulfillment_percentages.append(item.fulfillment_percentage)

    if fulfillment_percentages:
        average_week_fulfillment_percentage = round(
            sum(fulfillment_percentages) / len(fulfillment_percentages)
        )
        return min(average_week_fulfillment_percentage, 100)

    return 0


async def get_activity(group_id: int) -> Activity | None:
    try:
        data = await call(
            "stats.get",
            {
                "access_token": settings.VK_ADMIN_TOKEN,
                "group_id": group_id,
                "interval": "week",
                "intervals_count": 1,
                "extended": 1,
            },
            settings.VK_ADMIN_TOKEN,
        )

        print(f"{group_id}: {data['response'][0].get('activity')}")
        return (
            Activity(**data["response"][0].get("activity")).model_dump()
            if data["response"][0].get("activity")
            else None
        )

    except KeyError:
        return None
