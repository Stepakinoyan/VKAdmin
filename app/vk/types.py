from datetime import datetime
from typing import TypedDict


class StatisticType(TypedDict):
    date_id: str
    organization_id: int
    date_added: datetime
    members_count: int
    fulfillment_percentage: int
