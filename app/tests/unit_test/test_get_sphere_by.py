from typing import Optional
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "level,founder",
    [
        ("Министерство", None),
        (None, "Государственная жилищная инспекция области"),
        (None, None),
        ("МО", "gregergr"),
    ],
)
async def test_get_sphere_by(
    level: Optional[str], founder: Optional[str], ac: AsyncClient
):
    response = await ac.get(
        "/filter/get_spheres_by", params={"level": level, "founder": founder}
    )

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
