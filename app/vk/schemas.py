from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, Field


class Organization(TypedDict):
    id: int
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    reason: Optional[str]
    the_main_state_registration_number: Optional[int]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    status: Optional[str]
    channel_id: Optional[int]
    url: Optional[str]
    address: Optional[str]
    connected: Optional[str]
    state_mark: Optional[bool]
    decoration: Optional[str]
    widgets: Optional[str]
    activity: Optional[str]
    followers: Optional[str]
    weekly_audience: Optional[str]
    average_publication_coverage: Optional[str]


class Account(TypedDict):
    id: int
    channel_id: int
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
    date_added: Optional[datetime]
    posts: int
    posts_1d: int
    posts_7d: int
    posts_30d: int
    post_date: Optional[datetime]

class Statistic(BaseModel):
    date_id: str
    account_id: int
    date_added: datetime = Field(default=datetime.utcnow)
    members_count: int

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



