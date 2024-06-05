from typing import Optional

from pydantic import BaseModel


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
