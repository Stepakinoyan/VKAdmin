from datetime import date, datetime

import pytz

from app.statistic.schemas import StatisticDTO
from dateutil.relativedelta import MO, relativedelta
from app.organizations.schemas import SphereDTO
from app.organizations.types import SphereStr

amurtime = pytz.timezone("Asia/Yakutsk")


def get_new_stats(stats: list[StatisticDTO]) -> list[StatisticDTO]:
    
    new_stats = []
    now = datetime.now(amurtime)
    for stat in stats:
        if stat.date_added.month == now.month and stat.date_added.year == now.year:
            new_stats.append(stat)
    return new_stats


def get_stats_by_dates(
    stats: list[StatisticDTO], date_from: date, date_to: date
) -> list[StatisticDTO]:
    return [item for item in stats if date_from <= item.date_added <= date_to]


def get_last_monday():
    today = datetime.now(amurtime).today()
    return today + relativedelta(weekday=MO(-1))

def get_unique_spheres(items: list[SphereStr]) -> list[SphereDTO]:
    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres