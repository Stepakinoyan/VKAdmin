from datetime import datetime, date

import pytz

from app.organizations.types import SphereType
from app.statistic.schemas import StatisticDTO


def get_unique_spheres(items: list[SphereType]) -> list[SphereType]:
    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres


def get_new_stats(stats: list[StatisticDTO]) -> list[StatisticDTO]:
    amurtime = pytz.timezone("Asia/Yakutsk")
    new_stats = []
    now = datetime.now(amurtime)
    for stat in stats:
        if stat.date_added.month == now.month and stat.date_added.year == now.year:
            new_stats.append(stat)
    return new_stats


def get_stats_by_dates(stats: list[StatisticDTO], date_from: date, date_to: date) -> list[StatisticDTO]:
    return [item for item in stats if date_from <= item.date_added <= date_to]