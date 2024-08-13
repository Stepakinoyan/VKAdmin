from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Activity(BaseModel):
    comments: int = Field(default=0)
    likes: int = Field(default=0)
    subscribed: int = Field(default=0)
    widget_count: Optional[int] = Field(default=0)
    

class StatisticDTO(BaseModel):
    date_id: str
    organization_id: int
    date_added: datetime
    fulfillment_percentage: int

    activity: Optional[Activity]
