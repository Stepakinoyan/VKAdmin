from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    level: Optional[str]
    founder: Optional[str]
    name: Optional[str]
    the_main_state_registration_number: Optional[int]
    sphere_1: Optional[str]
    sphere_2: Optional[str]
    sphere_3: Optional[str]
    channel_id: Optional[int]
    url: Optional[str | int]


class Connection(BaseModel):
    channel_id: Optional[int]
    connected: Optional[bool] = Field(default=False)

    @field_validator("connected", mode="before")
    @classmethod
    def connected_validate(cls, value: int):
        if value:
            return True
