from datetime import datetime

import pytz
from dateutil.relativedelta import MO, relativedelta

from app.organizations.schemas import SphereDTO
from app.organizations.types import SphereStr

amurtime = pytz.timezone("Asia/Yakutsk")


def get_last_monday():
    today = datetime.now(amurtime).today()
    return today + relativedelta(weekday=MO(-1))


def get_unique_spheres(items: list[SphereStr]) -> list[dict[SphereDTO]]:
    spheres = []
    for item in list(set(filter(lambda item: item is not None, items))):
        spheres.append({"sphere": item})

    return spheres
