from typing import Literal, Optional

from fastapi import Query


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
    ):
        self.level = level
        self.zone = zone
        self.founder = founder
        self.sphere = sphere
