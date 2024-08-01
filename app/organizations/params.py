from datetime import date, datetime
from typing import Literal, Optional

import pytz
from dateutil.relativedelta import MO, relativedelta
from fastapi import Query

amurtime = pytz.timezone("Asia/Yakutsk")
now = datetime.now(amurtime)


class FilterFounderParams:
    def __init__(
        self,
        level: Literal[
            "Регион",
            "Министерство",
            "МО",
            "Ведомство",
            "Законодательный орган",
            "Другое",
            "ВУЗ",
        ],
    ):
        self.level = level


class FilterSpheresParams:
    def __init__(
        self,
        level: Optional[
            Literal[
                "",
                "Регион",
                "Министерство",
                "МО",
                "Ведомство",
                "Законодательный орган",
                "Другое",
                "ВУЗ",
            ]
        ] = "",
        founder: Optional[str] = None,
    ):
        self.level = level
        self.founder = founder


def get_last_monday():
    today = date.today()
    return today + relativedelta(weekday=MO(-1))


class FilterChannelsParams:
    def __init__(
        self,
        level: Literal[
            "",
            "Регион",
            "Министерство",
            "МО",
            "Ведомство",
            "Законодательный орган",
            "Другое",
            "ВУЗ",
        ] = "",
        zone: Literal["", "90-100%", "70-89%", "0-69%"] = "",
        founder: Optional[str] = "",
        sphere: Optional[str] = "",
        name: Optional[str] = "",
        date_from: Optional[date] = Query(default=get_last_monday()),
        date_to: Optional[date] = datetime.now().date(),
    ):
        self.level = level
        self.zone = zone
        self.founder = founder
        self.sphere = sphere
        self.name = name
        self.date_from = date_from
        self.date_to = date_to
