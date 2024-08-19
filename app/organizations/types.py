from datetime import datetime
from typing import Optional, TypedDict
from pydantic import BaseModel


class OrganizationType(TypedDict):
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
    channel_id: int
    has_avatar: bool
    has_cover: bool
    has_description: bool
    has_gos_badge: bool
    has_widget: bool
    connected: bool
    widget_count: int
    members_count: int
    url: str
    site: Optional[str]
    date_added: datetime
    posts: int
    posts_1d: int
    posts_7d: int
    posts_30d: int


class SphereDTO(BaseModel):
    sphere: str


class FounderDTO(BaseModel):
    founder: str
