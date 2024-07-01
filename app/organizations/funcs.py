from app.organizations.types import SphereType
from datetime import datetime

from app.vk.schemas import StatisticDTO


def get_unique_spheres(items: list[SphereType]) -> list[SphereType]:
    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres


def get_new_stats(stats: list[StatisticDTO]) -> list[StatisticDTO]:
    new_stats = []
    now = datetime.now()
    for stat in stats:
        if stat.date_added.month == now.month and stat.date_added.year == now.year:
            new_stats.append(stat)
    return new_stats