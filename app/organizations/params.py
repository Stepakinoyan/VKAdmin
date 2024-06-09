from typing import Literal, Optional


class FilterFounderParams:
    def __init__(
        self,
        level: Literal[
            "Министерство", "МО", "Ведомство", "Законодательный орган", "Другое", "ВУЗ"
        ],
    ):
        self.level = level


class FilterChannelsParams:
    def __init__(
        self,
        level: Literal[
            "",
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
