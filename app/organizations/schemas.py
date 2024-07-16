from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.statistic.schemas import StatisticDTO


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
    channel_id: int
    has_avatar: Optional[bool] = Field(default=False)
    has_cover: Optional[bool] = Field(default=False)
    has_description: Optional[bool] = Field(default=False)
    has_gos_badge: Optional[bool] = Field(default=False)
    has_widget: Optional[bool] = Field(default=False)
    widget_count: Optional[int] = Field(default=0)
    members_count: Optional[int] = 0
    url: Optional[str]
    site: Optional[str]
    date_added: Optional[datetime]
    posts: Optional[int] = Field(default=0)
    posts_1d: Optional[int] = Field(default=0)
    posts_7d: Optional[int] = Field(default=0)
    posts_30d: Optional[int] = Field(default=0)

    statistic: Optional[list[StatisticDTO]] = Field(default=[])

    average_week_fulfillment_percentage: int = Field(default=0)
    average_fulfillment_percentage: int = Field(default=0)
    weekly_audience_reach: int = Field(default=0)

    @field_validator("has_widget", mode="before")
    def validate_has_widget(cls, value):
        if not value:
            return cls.model_fields["has_widget"].default

        return value

    @field_validator("widget_count", mode="before")
    def validate_widget_count(cls, value):
        if not value:
            return cls.model_fields["widget_count"].default

        return value

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
