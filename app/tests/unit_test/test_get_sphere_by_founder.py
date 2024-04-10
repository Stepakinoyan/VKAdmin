from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("founder", [("Козлов Александр Георгиевич"), ("Тимофеева Арина Артёмовна"), ("Бочаров Егор Маркович")])
async def test_get_sphere_by_founder(founder: str, ac: AsyncClient):
    response = await ac.get("/filter/get_spheres", params={"founder": founder})

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200