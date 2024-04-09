from typing import Literal, Union


class FilterFounderParams:
    def __init__(
        self,
        level: Literal["Министерство", "МО", "Ведомство", "Узкоспециальные", "Регион"],
    ):
        self.level = level


class FilterChannelsParams:
    def __init__(
        self,
        level: Literal["Министерство", "МО", "Ведомство", "Узкоспециальные", "Регион"],
        founder: str,
        sphere: Literal[
            "Спорт",
            "Культура",
            "Образование",
            "Здравоохранение",
            "Администрации",
            "ЖКХ",
            "Социальная защита",
        ],
        sort: bool = False,
    ):
        self.level = level
        self.founder = founder
        self.sphere = sphere
        self.sort = sort
