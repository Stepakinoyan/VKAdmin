from typing import Optional, Union

from pydantic import BaseModel, validator


class Item(BaseModel):
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
    url: Optional[Union[str, int]]
    address: Optional[str]
    connected: Optional[bool]
    state_mark: Optional[bool]
    decoration: Optional[bool]
    widgets: Optional[bool]
    activity: Optional[int]
    followers: Optional[int]
    weekly_audience: Optional[int]
    average_publication_coverage: Optional[int]

    @classmethod
    @validator(
        "url",
        "decoration",
        "channel_id",
        "the_main_state_registration_number" "widgets",
        "activity",
        "followers",
        "weekly_audience",
        "average_publication_coverage",
    )
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        else:
            return str(value)

    @validator("url", pre=True)
    def convert_url_to_string(cls, value) -> Optional[str]:
        if value is not None:
            return str(value)
        return None
