from datetime import datetime

from pydantic import BaseModel, Field


class StatisticDTO(BaseModel):
    date_id: str
    organization_id: int
    date_added: datetime = Field(default=datetime.utcnow)
    members_count: int
    fulfillment_percentage: int
