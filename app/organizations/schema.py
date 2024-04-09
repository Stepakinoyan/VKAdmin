from pydantic import BaseModel


class Stats(BaseModel):
    count: int
    items: list
