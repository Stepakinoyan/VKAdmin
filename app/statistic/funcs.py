from datetime import date, datetime
from typing import Optional

from app.organizations.funcs import amurtime
from app.statistic.schemas import StatisticDTO


def get_new_stats(stats: list[StatisticDTO]) -> list[StatisticDTO]:
    new_stats = []
    now = datetime.now(amurtime)
    for stat in stats:
        if stat.date_added.month == now.month and stat.date_added.year == now.year:
            new_stats.append(stat)
    return new_stats


def get_stats_by_dates(
    stats: list[StatisticDTO], date_from: Optional[date], date_to: Optional[date]
) -> list[StatisticDTO]:
    zone_stats = []
    today = date.today()

    if not stats:
        return []
    
    if not date_from:
        date_from = today.replace(day=1)
    else:
        date_from = date_from.date()

    if not date_to:
        date_to = today
    else:
        date_to = date_to.date()
    

    for item in stats:
        if date_from == item.date_added.date() or date_to == item.date_added.date():
            zone_stats.append(item)

    return sorted(zone_stats, key=lambda stat: stat.date_added)