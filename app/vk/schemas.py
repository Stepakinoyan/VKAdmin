from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class Activity(BaseModel):
    comments: int = Field(default=0)
    likes: int = Field(default=0)
    subscribed: int = Field(default=0)


class StatisticDTO(BaseModel):
    date_id: str
    organization_id: int
    date_added: datetime = Field(default=datetime.utcnow)
    fulfillment_percentage: int

    activity: Optional[Activity]


class City(BaseModel):
    id: int
    title: Optional[str]


class Image(BaseModel):
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]


class Cover(BaseModel):
    enabled: Optional[int] = Field(default=False)


class CoverItem(BaseModel):
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]


class Item(BaseModel):
    title: Optional[str]
    type: Optional[str]
    url: Optional[str]
    id: Optional[int]
    cover: Optional[list[CoverItem]] = Field(default=[])


class Menu(BaseModel):
    items: Optional[list[Item]]


class Group(BaseModel):
    city: Optional[City] = Field(default={})
    description: Optional[str]
    members_count: Optional[int] = Field(default=0)
    date_added: Optional[date]
    cover: Optional[Cover] = Field(default={})
    activity: Optional[str]
    status: Optional[str]
    menu: Optional[Menu] = Field(default={})
    name: Optional[str]
    screen_name: Optional[str]
    type: Optional[str]
    photo_50: Optional[str]
    photo_100: Optional[str]
    photo_200: Optional[str]

    date_added: date
