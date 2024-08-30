from typing import Optional
from pydantic import BaseModel


class UserAuth(BaseModel):
    email: str
    password: str


class UserDTO(BaseModel):
    email: str
    role: str
    password: str
    founder: Optional[str]

class Role(BaseModel):
    role: str