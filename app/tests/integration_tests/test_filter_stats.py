import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "level,founder,sphere,date_from,date_to",
    [
        ("МО", "Благовещенск", "Школы", "2023-01-01", "2023-12-31"),
        ("МО", "Селемджинский", "Культура", "2023-01-01", "2023-12-31"),
    ],
)
async def test_get_stats(
    level: str, founder: str, sphere: str, date_from: str, date_to: str, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        "/filter/get_stats",
        params={
            "level": level,
            "founder": founder,
            "sphere": sphere,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    data = response.json()
    assert isinstance(data, list)
    assert response.status_code == 200