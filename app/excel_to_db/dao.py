import json

import pandas
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import BaseDAO
from app.database import get_session
from app.excel_to_db.schemas import Item
from app.organizations.models import Organizations

db_columns = {
    "Уровень": "level",
    "Учредитель": "founder",
    "Наименование подведомственной организации": "name",
    "Официальная страница не ведется на основании": "reason",
    "ОГРН": "the_main_state_registration_number",
    "Сфера 1": "sphere_1",
    "Сфера 2": "sphere_2",
    "Сфера 3": "sphere_3",
    "Статус": "status",
    "ID госпаблика": "channel_id",
    "Ссылка на госпаблик ВК": "url",
    "Адрес, указанный в настройках страницы": "address",
    "Подключение к компоненту «Госпаблики» (да/нет)": "connected",
    "Госметка (да/нет)": "state_mark",
    "Оформление (%)": "decoration",
    "Виджеты (0/1/2)": "widgets",
    "Активность (%)": "activity",
    "Количество подписчиков": "followers",
    "Общий охват аудитории за неделю": "weekly_audience",
    "Средний охват одной публикации": "average_publication_coverage",
}


class ExcelToDBDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def excel_to_db(self, file: str, session: AsyncSession = get_session()):
        delete_data = delete(self.model)
        await session.execute(delete_data)
        await session.commit()

        excel_data_df = pandas.read_excel(file).rename(columns=db_columns)

        thisisjson = excel_data_df.to_json(orient="records")

        thisisjson_dict = json.loads(thisisjson)

        for column in thisisjson_dict:
            item = Item(**column)
            if item.channel_id != 0 and item.channel_id != None:
                add_data = insert(self.model).values(item.model_dump())
                await session.execute(add_data)
                await session.commit()
            else:
                pass
