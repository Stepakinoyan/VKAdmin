from datetime import datetime

from pydantic import BaseModel, Field


class AccountDTO(BaseModel):
    id: int
    screen_name: str
    type: str
    name: str
    city: str
    activity: str
    verified: bool
    has_avatar: bool
    has_cover: bool
    has_description: bool
    has_gos_badge: bool
    has_widget: bool
    widget_count: int
    members_count: int
    site: str
    date_added: datetime = Field(default=datetime.utcnow)
    posts: int
    posts_1d: int
    posts_7d: int
    posts_30d: int
    post_date: bool


class Statistic(BaseModel):
    date_id: str
    account_id: int
    date_added: datetime = Field(default=datetime.utcnow)
    members_count: int
