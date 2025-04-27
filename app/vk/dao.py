import asyncio
import time
from datetime import datetime

import httpx
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.dao.dao import BaseDAO
from app.database import async_session_maker, engine, get_session
from app.organizations.models import Organizations
from app.vk.funcs import call, fetch_group_data

semaphore = asyncio.Semaphore(3)


class VkDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def upsert_account(self, data: dict, session: AsyncSession = get_session()):
        try:
            organization = await session.get(self.model, data["id"])
            if organization:
                # Update the existing record
                organization.screen_name = data["screen_name"]
                organization.type = data["type"]
                organization.name = data["name"]
                organization.city = data.get("city", {}).get("title", "")
                organization.activity = data.get("activity", "")
                organization.has_avatar = bool(data.get("photo_50"))
                organization.has_cover = bool(data.get("cover", {}).get("enabled"))
                organization.has_description = bool(data.get("description"))
                organization.has_widget = bool(data.get("menu"))
                organization.widget_count = len(data.get("menu", {}).get("items", []))
                organization.members_count = data.get("members_count", 0)
                organization.site = data.get("site", "")
                organization.date_added = datetime.now()
            else:
                # Insert a new record
                organization = Organizations(
                    id=data["id"],
                    screen_name=data["screen_name"],
                    type=data["type"],
                    name=data["name"],
                    city=data.get("city", {}).get("title", ""),
                    activity=data.get("activity", ""),
                    has_avatar=bool(data.get("photo_50")),
                    has_cover=bool(data.get("cover", {}).get("enabled")),
                    has_description=bool(data.get("description")),
                    has_widget=bool(data.get("menu")),
                    widget_count=len(data.get("menu", {}).get("items", [])),
                    members_count=data.get("members_count", 0),
                    site=data.get("site", ""),
                    date_added=datetime.now(),
                )
                session.add(organization)
        except SQLAlchemyError:
            raise 
    @classmethod
    async def wall_get_data(self, group_id: int):
        async with semaphore:
            try:
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

                    async_session = sessionmaker(
                        engine, class_=AsyncSession, expire_on_commit=False
                    )
                    async with async_session() as session:
                        async with session.begin():
                            db_item = {}

                            db_item["posts"] = data["posts"]
                            db_item["posts_1d"] = data["posts_1d"]
                            db_item["posts_7d"] = data["posts_7d"]
                            db_item["posts_30d"] = data["posts_30d"]
                            print(f">>{data['group_id']}: {data['posts']}")

                            update_item = (
                                update(Organizations)
                                .where(Organizations.channel_id == group_id)
                                .values(**db_item)
                            )
                            await session.execute(update_item)
                            await session.commit()

                            return {data["group_id"]: "DB"}

                else:
                    print(f"{group_id}: NO DATA", data)

                    return {group_id: "NO DATA"}

                return group_id
            except httpx.ConnectError:
                return f"Failed to update wall's data for group_id {group_id}"

    @classmethod
    async def get_group_data(self, group_id: int):
        async with asyncio.Semaphore(1):
            try:
                data = await fetch_group_data(group_id=group_id)
                print(group_id)

                async with async_session_maker() as session:
                    update_vk_attributes = (
                        update(self.model)
                        .where(self.model.channel_id == group_id)
                        .values(
                            city=data.city.title if data.city else None,
                            screen_name=data.screen_name,
                            status=data.status,
                            date_added=data.date_added,
                            has_description=bool(data.description),
                            has_avatar=any(
                                [data.photo_50, data.photo_100, data.photo_200]
                            ),
                            activity=data.activity,
                            has_widget=bool(data.menu),
                            widget_count=len(data.menu.items)
                            if data.menu and data.menu.items
                            else 0,
                            type=data.type,
                            has_cover=bool(data.cover.enabled) if data.cover else False,
                            members_count=data.members_count,
                        )
                    )

                    await session.execute(update_vk_attributes)
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()
                await session.commit()
            except httpx.ConnectError:
                return f"Failed to update group's data for group_id {group_id}"

        return group_id

    @classmethod
    async def update_weekly_reach(self, group_id: int):
        async with asyncio.Semaphore(1):
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

                weekly_audience_reach = data["response"][0].get("reach").get("reach")
                print(f"{group_id}: {weekly_audience_reach}")
                async with async_session_maker() as session:
                    update_weekly_audience_reach = (
                        update(self.model)
                        .where(self.model.channel_id == group_id)
                        .values(weekly_audience_reach=weekly_audience_reach)
                    )

                    await session.execute(update_weekly_audience_reach)
                    await session.commit()

            except KeyError:
                print(f"Failed to update weekly reach for group_id {group_id}")
            except SQLAlchemyError:
                await session.rollback()