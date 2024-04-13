from typing import Optional
from pydantic import BaseModel


class Stats(BaseModel):
    count: int
    items: list


class Sphere(BaseModel):
    sphere: str
