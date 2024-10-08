import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("level", [("Регион"), ("ВУЗ"), ("Ведомство")])
async def test_get_founder_by_level(level: str, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get(
        "/filter/get_founders", params={"level": level}
    )

    assert isinstance(response.json(), list)
    assert response.status_code == 200
