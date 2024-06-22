import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "level,founder,sphere",
    [
        ("МО", "Архаринский", "Школы"),
        ("МО", "Архаринский", "Детские сады"),
    ],
)
async def test_get_founder_by_level(
    level: str, founder: str, sphere: str, ac: AsyncClient
):
    response = await ac.get(
        "/filter/get_stats",
        params={"level": level, "founder": founder, "sphere": sphere},
    )

    print(response.json())
    assert type(response.json()) == list
    assert response.status_code == 200
