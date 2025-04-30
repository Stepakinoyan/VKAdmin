import json

import pandas
from openpyxl import Workbook
from sqlalchemy import insert, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Users
from app.auth.schema import UserDTO
from app.dao.dao import BaseDAO
from app.excel_to_db.schemas import Connection, Item
from app.organizations.models import Organizations
from app.organizations.schemas import OrganizationsDTO

db_columns = {
    "Уровень": "level",
    "Учредитель": "founder",
    "Наименование подведомственной организации": "name",
    "ОГРН": "the_main_state_registration_number",
    "Сфера 1": "sphere_1",
    "Сфера 2": "sphere_2",
    "Сфера 3": "sphere_3",
    "Статус": "status",
    "ID госпаблика": "channel_id",
    "Ссылка на госпаблик ВК": "url",
}

connection = {"ID госпаблика": "channel_id", "Подключение": "connected"}

emails = {"Учредитель": "founder", "Доступ": "email"}


class ExcelDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def excel_to_db(self, file: str, session: AsyncSession):
        try:
            excel_df = pandas.read_excel(file).rename(columns=db_columns)

            excel_df_json = excel_df.to_json(orient="records")

            convert_to_json = json.loads(excel_df_json)
            convert_to_json[4]["level"] = "Регион"
            convert_to_json[4]["founder"] = "Правительство Амурской области"

            for column in convert_to_json:
                item = Item(**column)
                if item.channel_id != 0 and item.channel_id != None:
                    add_data = insert(self.model).values(item.model_dump())
                    await session.execute(add_data)
                else:
                    pass
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            await session.commit()

    @classmethod
    async def add_connection(self, file: str, session: AsyncSession):
        try:
            excel_df = pandas.read_excel(file).rename(columns=connection)

            excel_df_json = excel_df.to_json(orient="records")

            convert_to_json = json.loads(excel_df_json)

            for column in convert_to_json:
                connection_schema = Connection(**column)
                if connection_schema.channel_id:
                    add_data = (
                        update(self.model)
                        .where(self.model.channel_id == connection_schema.channel_id)
                        .values(connected=connection_schema.connected)
                    )
                    await session.execute(add_data)
                else:
                    pass
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            await session.commit()

    @classmethod
    async def add_users(self, session: AsyncSession):
        with open("app/excel_to_db/organizations.json", "r") as file:
            users = json.load(file)

        for user in users:
            user = UserDTO(**user).model_dump()
            add_user = insert(Users).values(**user)

            await session.execute(add_user)

        await session.commit()

    @classmethod
    async def save_accounts_to_xlsx(cls, stats: list):
        stats = sorted(stats, key=lambda s: s.get("id", 0))

        wb = Workbook()
        ws = wb.active
        ws.title = "Organizations"

        headers = [
            "id",
            "screen_name",
            "comments",
            "likes",
            "subscribed",
            "type",
            "name",
            "city",
            "activity",
            "channel_id",
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
            "average_week_fulfillment_percentage",
            "average_fulfillment_percentage",
            "weekly_audience_reach",
        ]
        ws.append(headers)

        for stat in stats:
            statistic = stat.get("statistic", [])
            last_activity = statistic[-1].get("activity") if statistic and isinstance(statistic[-1], dict) else {}

            row = [
                stat.get("id"),
                stat.get("screen_name"),
                last_activity.get("comments", 0) if last_activity else 0,
                last_activity.get("likes", 0) if last_activity else 0,
                last_activity.get("subscribed", 0) if last_activity else 0,
                stat.get("type"),
                stat.get("name"),
                stat.get("city"),
                stat.get("activity"),
                str(stat.get("channel_id", "")),
                "ДА" if stat.get("has_avatar") else "НЕТ",
                "ДА" if stat.get("has_cover") else "НЕТ",
                "ДА" if stat.get("has_description") else "НЕТ",
                "ДА" if stat.get("has_gos_badge") else "НЕТ",
                "ДА" if stat.get("has_widget") else "НЕТ",
                stat.get("widget_count", 0),
                str(stat.get("members_count", "")),
                stat.get("site", ""),
                str(stat.get("date_added", "")),
                stat.get("posts", 0),
                stat.get("posts_1d", 0),
                stat.get("posts_7d", 0),
                stat.get("posts_30d", 0),
                stat.get("average_week_fulfillment_percentage", 0),
                stat.get("average_fulfillment_percentage", 0),
                stat.get("weekly_audience_reach", 0),
            ]

            ws.append(row)

        wb.save(filename="organizations.xlsx")