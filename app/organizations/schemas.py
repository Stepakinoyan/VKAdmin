from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.vk.schemas import StatisticDTO


class OrganizationsDTO(BaseModel):
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

    average_fulfillment_percentage: Optional[int | float]


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

    statistic: Optional[list[StatisticDTO]]


    average_week_fulfillment_percentage: Optional[int]
    average_fulfillment_percentage: Optional[int]


class Stats(BaseModel):
    items: list[OrganizationResponse]
