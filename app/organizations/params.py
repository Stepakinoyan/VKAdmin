from datetime import date, datetime
from typing import Literal, Optional


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
        level: Literal[
            "",
            "Регион",
            "Министерство",
            "МО",
            "Ведомство",
            "Законодательный орган",
            "Другое",
            "ВУЗ",
        ] = None,
    ):
        self.level = level


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
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        self.level = level
        self.zone = zone
        self.founder = founder
        self.sphere = sphere
        self.name = name
        self.date_from = date_from
        self.date_to = date_to
