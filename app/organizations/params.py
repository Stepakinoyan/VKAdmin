from typing import Optional, Literal


class FilterFounderParams:
    def __init__(
        self,
        level: Literal["Министерство", "МО", "Ведомство", "Узкоспециальные", "Регион"],
    ):
        self.level = level


class FilterChannelsParams:
    def __init__(
        self,
        level: Literal[
            "", "Министерство", "МО", "Ведомство", "Узкоспециальные", "Регион"
        ] = "",
        founder: Optional[str] = "",
        sphere: Optional[str] = "",
        sort: bool = False,
    ):
        self.level = level
        self.founder = founder
        self.sphere = sphere
        self.sort = sort
