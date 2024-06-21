import json

import pandas
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import BaseDAO
from app.database import get_session
from app.excel_to_db.schemas import Item
from app.organizations.models import Organizations

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


class ExcelToDBDAO(BaseDAO):
    model = Organizations

    @classmethod
    async def excel_to_db(self, file: str, session: AsyncSession = get_session()):

        excel_df = pandas.read_excel(file).rename(columns=db_columns)

        excel_df_json = excel_df.to_json(orient="records")

        convert_to_json = json.loads(excel_df_json)
        print(convert_to_json[4])
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


# from sqlalchemy.ext.asyncio import AsyncSession
# from app.dao.dao import BaseDAO
# from app.database import get_session
# from app.excel_to_db.schemas import Item
# from app.organizations.models import Organizations
# from sqlalchemy import insert, select, update
# import pandas as pd
# import json

# db_columns = {
#     "Уровень": "level",
#     "Учредитель": "founder",
#     "Наименование подведомственной организации": "name",
#     "ОГРН": "the_main_state_registration_number",
#     "Сфера 1": "sphere_1",
#     "Сфера 2": "sphere_2",
#     "Сфера 3": "sphere_3",
#     "Статус": "status",
#     "ID госпаблика": "channel_id",
#     "Ссылка на госпаблик ВК": "url",
# }


# class ExcelToDBDAO(BaseDAO):
#     model = Organizations

#     @classmethod
#     async def excel_to_db(cls, file: str, session: AsyncSession = get_session()):
#         excel_df = pd.read_excel(file).rename(columns=db_columns)
#         convert_to_json = json.loads(excel_df.to_json(orient="records"))

#         # Обработка данных перед вставкой
#         for column in convert_to_json:
#             item = Item(**column)
#             if item.channel_id and item.channel_id != 0:
#                 query = select(cls.model).filter_by(channel_id=item.channel_id)
#                 result = await session.execute(query)
#                 existing_item = result.scalars().first()

#                 if existing_item:
#                     # Обновляем существующую запись
#                     update_data = {key: value for key, value in item.model_dump().items() if value is not None}
#                     await session.execute(
#                         update(Organizations).where(cls.model.channel_id == item.channel_id).values(**update_data)
#                     )
#                 else:
#                     # Добавляем новую запись
#                     add_data = insert(cls.model).values(item.model_dump())
#                     await session.execute(add_data)
#         try:
#             await session.commit()
#         except sqlalchemy.exc.IntegrityError as e:
#             print(f"IntegrityError: {e}")
#             await session.rollback()