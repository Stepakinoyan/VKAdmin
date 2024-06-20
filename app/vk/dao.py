import asyncio
import json
import time
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.dao.dao import BaseDAO
from app.database import engine, get_session
from app.vk.funcs import call
from app.organizations.models import Organizations

semaphore = asyncio.Semaphore(3)


class VkDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def upsert_account(self, data: dict, session: AsyncSession = get_session()):
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

    @classmethod
    async def wall_get_data(self, group_id: int):
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

                async_session = sessionmaker(
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
