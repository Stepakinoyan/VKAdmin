from app.organizations.schemas import Sphere, StatisticBase
from datetime import datetime

from app.vk.schemas import SchemaStatistic


def get_unique_spheres(items: list[Sphere]) -> list[Sphere]:
    """

    Возвращает список уникальных объектов типа Sphere.

    """

    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres


def get_new_stats(
    stats: list[SchemaStatistic] | list[StatisticBase],
) -> list[SchemaStatistic] | list[StatisticBase]:
    """
    Возвращает список со статистикой на текущий месяц и год.
    """
    new_stats = []
    now = datetime.now()
    for stat in stats:
        if stat.date_added.month == now.month and stat.date_added.year == now.year:
            new_stats.append(stat)
    return new_stats
