import json

import pandas
from openpyxl import Workbook
from sqlalchemy import insert, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def add_users(self, file: str, session: AsyncSession):
        users = []
        excel_df = pandas.read_excel(file).rename(columns=emails)
        excel_df_json = excel_df.to_json(orient="records")
        convert_to_json = json.loads(excel_df_json)

        for i in convert_to_json:
            if i.get("email"):
                users.append({"founder": i.get("founder"), "email": i.get("email")})

        with open("organizations.json", 'w') as file:
            json.dump(users, file, indent=4)

    @classmethod
    async def save_accounts_to_xlsx(self, stats: list):
        stats = sorted(stats, key=lambda id: id["id"])
        # 2. Create a new XLSX workbook and sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Organizations"

        # Set headers for the sheet
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

        # Append account data to the sheet
        for stat in stats:
            stat = OrganizationsDTO(**stat)
            activity = (
                stat.statistic[-1].activity
                if stat.statistic and stat.statistic[-1].activity is not None
                else {}
            )
            if activity:
                ws.append(
                    [
                        stat.id,
                        stat.screen_name,
                        activity.comments,
                        activity.likes,
                        activity.subscribed,
                        stat.type,
                        stat.name,
                        stat.city,
                        stat.activity,
                        str(stat.channel_id),
                        "ДА" if stat.has_avatar else "НЕТ",
                        "ДА" if stat.has_cover else "НЕТ",
                        "ДА" if stat.has_description else "НЕТ",
                        "ДА" if stat.has_gos_badge else "НЕТ",
                        "ДА" if stat.has_widget else "НЕТ",
                        stat.widget_count,
                        str(stat.members_count),
                        stat.site,
                        str(stat.date_added),
                        stat.posts,
                        stat.posts_1d,
                        stat.posts_7d,
                        stat.posts_30d,
                        stat.average_week_fulfillment_percentage,
                        stat.average_fulfillment_percentage,
                        stat.weekly_audience_reach,
                    ]
                )
            else:
                ws.append(
                    [
                        stat.id,
                        stat.screen_name,
                        0,
                        0,
                        0,
                        stat.type,
                        stat.name,
                        stat.city,
                        stat.activity,
                        str(stat.channel_id),
                        "ДА" if stat.has_avatar else "НЕТ",
                        "ДА" if stat.has_cover else "НЕТ",
                        "ДА" if stat.has_description else "НЕТ",
                        "ДА" if stat.has_gos_badge else "НЕТ",
                        "ДА" if stat.has_widget else "НЕТ",
                        stat.widget_count,
                        str(stat.members_count),
                        stat.site,
                        str(stat.date_added),
                        stat.posts,
                        stat.posts_1d,
                        stat.posts_7d,
                        stat.posts_30d,
                        stat.average_week_fulfillment_percentage,
                        stat.average_fulfillment_percentage,
                        stat.weekly_audience_reach,
                    ]
                )

        # Save the workbook to the specified file path
        wb.save(filename="organizations.xlsx")
