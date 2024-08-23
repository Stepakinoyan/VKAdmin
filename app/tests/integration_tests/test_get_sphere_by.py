from typing import Optional

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "level,founder",
    [
        ("Министерство", None),
        (None, "Государственная жилищная инспекция области"),
        (None, None),
        pytest.param("ауцаццук", "feqwfewfew", marks=pytest.mark.xfail),
    ],
)
async def test_get_sphere_by(
    level: Optional[str], founder: Optional[str], authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        "/filter/get_spheres_by", params={"level": level, "founder": founder}
    )

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert isinstance(response.json(), list), "Response data is not a list"
