import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "founder",
    [
        ("РОИВ"),
        ("Архаринский"),
        ("Белогорск"),
    ],
)
async def test_get_sphere_by_founder(founder: str, ac: AsyncClient):
    response = await ac.get("/filter/get_spheres_by_founder", params={"founder": founder})

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
