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

    if not stats:
        return []

    if not date_from and not date_to:
        return sorted([stats[0], stats[-1]], key=lambda stat: stat.date_added)

    for item in stats:
        if date_to == item.date_added or date_from == item.date_added:
            zone_stats.append(item)

    return zone_stats[::-1] 