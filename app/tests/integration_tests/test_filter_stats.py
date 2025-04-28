import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "level,founder,sphere",
    [
        ("МО", "Благовещенск", "Школы"),
        ("МО", "Селемджинский", "Культура"),
    ],
)
async def test_get_founder_by_level(
    level: str, founder: str, sphere: str, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        "/filter/get_stats",
        params={"level": level, "founder": founder, "sphere": sphere},
    )

    data = response.json()


    assert isinstance(data, list)
    assert response.status_code == 200
