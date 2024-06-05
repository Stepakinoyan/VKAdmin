from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel


class StatisticBase(BaseModel):
    date_id: str
    organization_id: int
    date_added: datetime
    members_count: int
    fulfillment_percentage: int


class OrganizationsBase(BaseModel):
    id: int
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    the_main_state_registration_number: int
    screen_name: Optional[str]
    type: Optional[str]
    city: Optional[str]
    status: Optional[str]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    activity: Optional[str]
    verified: Optional[bool]
    channel_id: Optional[int]
    has_avatar: Optional[bool]
    has_cover: Optional[bool]
    has_description: Optional[bool]
    has_gos_badge: Optional[bool]
    has_widget: Optional[bool]
    widget_count: Optional[int]
    members_count: Optional[int]
    url: Optional[str]
    site: Optional[str]
    date_added: Optional[datetime]
    posts: Optional[int]
    posts_1d: Optional[int]
    posts_7d: Optional[int]
    posts_30d: Optional[int]
    post_date: Optional[datetime]

class OrganizationsForStatistic(BaseModel):
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    the_main_state_registration_number: int
    screen_name: Optional[str]
    type: Optional[str]
    city: Optional[str]
    status: Optional[str]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    activity: Optional[str]
    verified: Optional[bool]
    channel_id: Optional[int]
    has_avatar: Optional[bool]
    has_cover: Optional[bool]
    has_description: Optional[bool]
    has_gos_badge: Optional[bool]
    has_widget: Optional[bool]
    widget_count: Optional[int]
    members_count: Optional[int]
    url: Optional[str]
    site: Optional[str]
    date_added: Optional[datetime]
    posts: Optional[int]
    posts_1d: Optional[int]
    posts_7d: Optional[int]
    posts_30d: Optional[int]
    post_date: Optional[datetime]


class OrganizationResponse(BaseModel):
    id: int
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    the_main_state_registration_number: int
    screen_name: Optional[str]
    type: Optional[str]
    city: Optional[str]
    status: Optional[str]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    activity: Optional[str]
    verified: Optional[bool]
    channel_id: Optional[int]
    has_avatar: Optional[bool]
    has_cover: Optional[bool]
    has_description: Optional[bool]
    has_gos_badge: Optional[bool]
    has_widget: Optional[bool]
    widget_count: Optional[int]
    members_count: Optional[int]
    url: Optional[str]
    site: Optional[str]
    date_added: Optional[datetime]
    posts: Optional[int]
    posts_1d: Optional[int]
    posts_7d: Optional[int]
    posts_30d: Optional[int]
    post_date: Optional[datetime]

    statistic: Optional[list[StatisticBase]]


class Stats(BaseModel):
    items: list[OrganizationResponse]


"""   Подсказки типов   """


class Sphere(TypedDict):
    sphere: str


class Founder(TypedDict):
    founder: str


class StatisticData(TypedDict):
    date_id: str
    organization_id: int
    date_added: Optional[datetime]
    members_count: int
    fulfillment_percentage: int


class StatsData(TypedDict):
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    reason: Optional[str]
    the_main_state_registration_number: Optional[int]
    status: Optional[str]
    channel_id: Optional[int]
    url: Optional[str]
    address: Optional[str]
    connected: Optional[bool]
    state_mark: Optional[bool]

    statistic: Optional[StatisticBase]
