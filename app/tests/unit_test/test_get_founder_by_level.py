import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("level", [("МО"), ("Регион"), ("Ведомство")])
async def test_get_founder_by_level(level: str, ac: AsyncClient):
    response = await ac.get("/filter/get_spheres_by_level", params={"level": level})

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
