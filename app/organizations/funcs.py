from datetime import date, datetime

import pytz

from app.statistic.schemas import StatisticDTO
from dateutil.relativedelta import MO, relativedelta


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
    today = date.today()
    return today + relativedelta(weekday=MO(-1))