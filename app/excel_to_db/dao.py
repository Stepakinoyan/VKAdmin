import openpyxl
import pandas
import json
from sqlalchemy import delete, insert
from app.organizations.models import Organizations
from app.dao.dao import BaseDAO
from app.database import async_session_maker
from typing import Optional, Union
from pydantic import BaseModel, validator


class Item(BaseModel):
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    reason: Optional[str]
    the_main_state_registration_number: Optional[int]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    status: Optional[str]
    channel_id: Optional[int]
    url: Optional[Union[str, int]]
    address: Optional[str]
    connected: Optional[str]
    state_mark: Optional[bool]
    decoration: Optional[int]
    widgets: Optional[int]
    activity: Optional[int]
    followers: Optional[int]
    weekly_audience: Optional[int]
    average_publication_coverage: Optional[int]

    @classmethod
    @validator(
        "url",
        "decoration",
        "channel_id",
        "the_main_state_registration_number" "widgets",
        "activity",
        "followers",
        "weekly_audience",
        "average_publication_coverage",
    )
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        else:
            return str(value)

    @validator("url", pre=True)
    def convert_url_to_string(cls, value) -> Optional[str]:
        if value is not None:
            return str(value)
        return None


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
    async def excel_to_db(self, file: str):
        async with async_session_maker() as session:

            delete_data = delete(self.model)
            await session.execute(delete_data)
            await session.commit()

        async with async_session_maker() as session:

            excel_data_df = pandas.read_csv(file).rename(columns=db_columns)

            thisisjson = excel_data_df.to_json(orient="records")

            thisisjson_dict = json.loads(thisisjson)

            for column in thisisjson_dict:
                item = Item(**column)
                add_data = insert(self.model).values(item.model_dump())

                await session.execute(add_data)
                await session.commit()
