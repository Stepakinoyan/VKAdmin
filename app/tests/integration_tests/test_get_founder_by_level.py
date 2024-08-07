import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("level", [("Регион"), ("ВУЗ"), ("Ведомство")])
async def test_get_founder_by_level(level: str, ac: AsyncClient):
    response = await ac.get("/filter/get_founders", params={"level": level})

    data = response.json()
    assert isinstance(data, list)
    assert response.status_code == 200
